
from decouple import config
from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
from datetime import date, datetime
from flask_cors import CORS, cross_origin

app = Flask(__name__)

app.config['MYSQL_HOST'] = config("mysql_hostname")
app.config['MYSQL_USER'] = config("mysql_user")
app.config['MYSQL_PASSWORD'] = config("mysql_password")
app.config['MYSQL_DB'] = config("mysql_db")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

CORS(app)

def get(dic, key, default):
    x = dic[key] if key in dic or not default else default[key]
    if isinstance(x, date):
        x = x.strftime(format= "%Y-%m-%d")
    return x

def prepDict(dic):
    if isinstance(dic,  list) or isinstance(dic, tuple):
        dic = list(dic)
        for i in range(len(dic)):
            dic[i] = prepDict(dic[i])
        return dic
    elif isinstance(dic, dict):
        for key in dic:
            if isinstance(dic[key], date):
                dic[key] = dic[key].strftime(format= "%Y-%m-%d")
        return dic

    else :
        return dic

@app.route("/")
def index():
    return jsonify({"status": "running", "time": str(datetime.now())})

def to_val(x):

    if x is None:
        return "null"

    if isinstance(x, int):
        return str(x)
    
    return f"'{x}'"

@app.route('/login', methods=['POST'])
@cross_origin()
def login():

    content = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute(f"""select email as uid from user where email='{content['email']}' and pass = sha1('{content['password']}')""")

    rv = cursor.fetchone()

    if not rv:
        return jsonify("Wrong email/password"), 403

    return jsonify(content['email']), 200
    



@app.route("/users/<string:email>", methods=['GET', 'POST'])
@cross_origin()
def user(email):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute(f"""select email as uid, fname as first_name, 
                           lname as last_name, dob as birth_date, 
                           linked_in as linkedin, website, phone, gender
                           from User where email='{email}'""")
        rv = cursor.fetchone()

        if request.method == "GET":

            cursor.close()

            if rv:

                return jsonify(prepDict(rv)), 200

            else:
                return jsonify("No user found"), 404

        else:


            content = request.get_json()

            first_name = get(content,"first_name", rv)
            last_name = get(content,"last_name", rv)
            birth_date = get(content,"birth_date", rv)
            linkedin = get(content,"linkedin", rv)
            website = get(content,"website", rv)
            phone =get(content,"phone", rv)
            gender = get(content,"gender", rv)

                # add or update a user
            if rv:
                # update user
                update_user_cmd = f"""update User
                                 set fname='{first_name}', lname='{last_name}', 
                                 linked_in='{linkedin}', phone='{phone}', dob='{birth_date}', 
                                 website='{website}', gender='{gender}'
                                 where email='{email}'"""
                cursor.execute(update_user_cmd)
                mysql.connection.commit()
                cursor.close()
                return jsonify('User updated successfully.'), 200

            else:

                insert_user_cmd = f"""INSERT INTO User(email,pass, fname, lname, dob, linked_in, website, phone, gender)
                                    VALUES('{email}', sha1('{content['password']}'), '{first_name}', '{last_name}',
                            '{birth_date}','{linkedin}', '{website}', '{phone}', '{gender}')"""
                cursor.execute(insert_user_cmd)
                mysql.connection.commit()
                cursor.close()

                return jsonify('User added successfully.'), 200

                


    except Exception as e:
        return str(e), 500

## TODO: ceeate alumni only views and student only views or views for types only
def _getUserType(email):
        cursor = mysql.connection.cursor()
        cursor.execute(f"select uemail from ALUMNUS where uemail='{email}'")
        rv = cursor.fetchone()
        cursor.close()

        if rv != None:
            return "M"
        else:

            cursor = mysql.connection.cursor()
            cursor.execute(f"select uemail from student where uemail='{email}'")
            rv = cursor.fetchone()
            cursor.close()

            if rv == None:
                return None
            return "S"

@app.route("/users/<string:email>/type")
@cross_origin()
def getUserType(email):

    try:
        return jsonify(_getUserType(email)),200

    except Exception as e:
        return str(e), 500


@app.route("/users/<string:email>/education", methods = ["GET"])
def educations(email):
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute(f"""select id, major, inst_email as org_id,  oname as org_name, 
                                score, start_date as start_at, end_date as end_at
                        from Complete_Program
                        join organization_name on inst_email = oemail
                        where uemail = '{email}'
                        order by start_date desc, end_date desc""")
        rv = cursor.fetchall()

        for educ in rv:

            educ['accomplishments'] = []
            cursor.execute(f"""select title, content 
                                from prg_accomplishments
                                where prg_id = '{educ['id']}'""")

            resp = cursor.fetchall()

            for acc in resp:
                educ['accomplishments'].append(acc["content"])

        return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
        return str(e), 500


@app.route("/users/<string:email>/education/<int:eid>", methods = ["DELETE", "POST"])
def education(email,eid):
    try:

        if request.method == "DELETE":
            cursor = mysql.connection.cursor()
            cursor.execute(f"select id from complete_program where uemail = '{email}' and id='{eid}'")
            
            rv = cursor.fetchone()

            if not rv:
                return jsonify("Not allowed to delete program"), 405
            
            cursor.execute(f"delete from complete_program where id = '{eid}'")
            mysql.connection.commit()
            return jsonify('Prog deleted successfully.'), 200

        else:
            # add or update
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select id, major, inst_email as org_id, 
                                score, start_date as start_at, end_date as end_at, major, uemail
                                from Complete_Program
                                where id={eid}""")
            rv = cursor.fetchone()

            content = request.get_json()

            major =get(content, "major", rv)
            org_id = get(content, "org_id", rv)
            score = get(content, "score", rv)
            start_at = get(content, "start_at", rv)
            end_at = get(content, "end_at", rv)

            if rv and rv['uemail'] == email:
                # can update

                update_user_cmd = f"""update complete_program
                                 set major='{major}', inst_email='{org_id}', score='{score}', start_date='{start_at}', end_date='{end_at}'
                                 where id={eid}"""
                cursor.execute(update_user_cmd)
                mysql.connection.commit()

                if "accomplishments" in content:
                    cursor.execute(f"""delete from prg_accomplishments where prg_id='{eid}'""")
                    for i, acc in enumerate(content["accomplishments"]):
                        cursor.execute(f"""INSERT INTO prg_accomplishments (prg_id, title, content) 
                                            values ('{eid}', '{f"Acc-{i}"}','{acc}')""")
                
                mysql.connection.commit()


                return jsonify('User updated successfully.'), 200


            elif not rv:
                # can create
                insert_user_cmd = f"""INSERT INTO complete_program(major, inst_email, score, start_date, end_date, uemail)
                                    VALUES('{major}', '{org_id}', '{score}', "{start_at}", '{end_at}', '{email}')"""
                cursor.execute(insert_user_cmd)
                mysql.connection.commit()

                cursor.execute(f"""select id from complete_program where uemail='{email}' order by id desc""")

                latest = cursor.fetchone()
                
                if "accomplishments" in content:
                    for i, acc in enumerate(content["accomplishments"]):
                        cursor.execute(f"""INSERT INTO prg_accomplishments (prg_id, title, content) 
                                            values ('{latest['id']}', '{f"Acc-{i}"}', '{acc}')""")
                    

                mysql.connection.commit()
                return jsonify('User added successfully.'), 200
            

            
            else:
                #not allowed
                return jsonify("Not allowed to edit"), 405


        

    except Exception as e:
        raise(e)
        return jsonify('Failed to delete prog. '+str(e)), 500

@app.route("/mentors/<string:email>", methods = ['GET', 'POST'])
def mentor(email):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute(
                f"""select a.position as position, oname as org_name, oemail as org_id 
                    from Alumnus a join organization_name on oemail = work_email
                    where uemail = '{email}'""")

        rv = cursor.fetchone()

        if request.method == 'GET':
            if rv:
                cursor.close()
                return jsonify(prepDict(rv))

            else:
                return jsonify("Mentor not found"), 404

        elif request.method == "POST":

            content = request.get_json()
            org_id = get(content, 'org_id', rv)
            position = get(content, 'position', rv)

            if rv:
                #update 
                update_user_cmd = f"""update Alumnus
                                 set work_email='{org_id}', position='{position}'
                                 where uemail='{email}'"""
                cursor.execute(update_user_cmd)
                mysql.connection.commit()
                return jsonify('User updated successfully.'), 200

            else:
                
                if _getUserType(email) == "S":
                    return jsonify("Already seeker"), 405
                
                #create
                insert_user_cmd = f"""INSERT INTO Alumnus(uemail, work_email, position)
                                    VALUES({to_val(email)}, {to_val(org_id)}, {to_val(position)})"""
                print(insert_user_cmd)
                cursor.execute(insert_user_cmd, ())
                mysql.connection.commit()
                return jsonify('User added successfully.'), 200

    except Exception as e:
        print(e)
        return jsonify(str(e)), 500

@app.route("/mentors/<string:email>/experience", methods = ["GET"])
def experiences(email):
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute(f"""select id, position, start_date as start_at, end_date as end_at,
                                  work_email as org_id, oname as org_name
                        from experience
                        join organization_name on work_email = oemail
                        where alemail = '{email}'
                        order by start_date desc, end_date desc""")
        rv = cursor.fetchall()

        for educ in rv:

            educ['accomplishments'] = []
            cursor.execute(f"""select title, content 
                                from exp_accomplishments
                                where ex_id = '{educ['id']}'""")

            resp = cursor.fetchall()

            for acc in resp:
                educ['accomplishments'].append(acc["content"])

        return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
        return str(e), 500


@app.route("/mentors/<string:email>/experience/<int:eid>", methods = ["DELETE", "POST"])
def experience(email,eid):
    try:

        if request.method == "DELETE":
            cursor = mysql.connection.cursor()
            cursor.execute(f"select id from experience where alemail = '{email}' and id='{eid}'")
            
            rv = cursor.fetchone()

            if not rv:
                return jsonify("Not allowed to delete exprience"), 405
            
            cursor.execute(f"delete from experience where id = '{eid}'")
            mysql.connection.commit()
            return jsonify('Exp deleted successfully.'), 200

        else:
            # add or update
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select id, position, start_date as start_at, end_date as end_at,
                                  work_email as org_id, alemail
                        from experience
                        where id = '{eid}'""")
            rv = cursor.fetchone()

            content = request.get_json()

            position =get(content, "position", rv)
            org_id = get(content, "org_id", rv)
            start_at = get(content, "start_at", rv)
            end_at = get(content, "end_at", rv)

            if rv and rv['alemail'] == email:
                # can update

                update_user_cmd = f"""update experience
                                 set position='{position}', work_email='{org_id}', start_date='{start_at}', end_date='{end_at}'
                                 where id={eid}"""
                cursor.execute(update_user_cmd)
                mysql.connection.commit()

                if "accomplishments" in content:
                    cursor.execute(f"""delete from exp_accomplishments where ex_id='{eid}'""")
                    for i, acc in enumerate(content["accomplishments"]):
                        cursor.execute(f"""INSERT INTO exp_accomplishments (ex_id, title, content) 
                                            values ('{eid}', '{f"Acc-{i}"}','{acc}')""")
                
                mysql.connection.commit()


                return jsonify('User updated successfully.'), 200


            elif not rv:
                # can create
                insert_user_cmd = f"""INSERT INTO experience(position, work_email, start_date, end_date, alemail)
                                    VALUES('{position}', '{org_id}', "{start_at}", '{end_at}', '{email}')"""
                cursor.execute(insert_user_cmd)
                mysql.connection.commit()

                cursor.execute(f"""select id from experience where alemail='{email}' order by id desc""")

                latest = cursor.fetchone()
                
                if "accomplishments" in content:
                    for i, acc in enumerate(content["accomplishments"]):
                        cursor.execute(f"""INSERT INTO exp_accomplishments (ex_id, title, content) 
                                            values ('{latest['id']}', '{f"Acc-{i}"}', '{acc}')""")
                    

                mysql.connection.commit()
                return jsonify('User added successfully.'), 200
            

            
            else:
                #not allowed
                return jsonify("Not allowed to edit"), 405


        

    except Exception as e:
        raise(e)
        return jsonify('Failed to delete prog. '+str(e)), 500

@app.route("/seekers/<string:email>", methods = ['GET', 'POST'])
def seeker(email):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute(
            f"""select sop, is_open_work as open_to_work 
                from Student 
                where uemail='{email}'""")
        rv = cursor.fetchone()

        if request.method == 'GET':

            if rv:
                return jsonify(prepDict(rv)), 200
            else:
                return jsonify("Seeker does not exist"), 404

        else:

            content = request.get_json()

            print(content)

            sop = get(content, "sop", rv)
            open_to_work = 1 if get(content, "open_to_work", rv) else 0

            if not rv:

                if _getUserType(email) == "M":
                    return jsonify("Already mentor"), 405

                insert_user_cmd = f"""INSERT INTO Student(uemail, sop, is_open_work)
                                        VALUES('{email}','{sop}', {open_to_work})"""
                
                print(insert_user_cmd)
                cursor.execute(insert_user_cmd)
                mysql.connection.commit()
                return jsonify(
                    message='User added successfully.'), 200

            else:
                update_user_cmd = f"""update Student
                                    set sop='{sop}', is_open_work={open_to_work}
                                    where uemail='{email}'"""
                
                cursor.execute(update_user_cmd)
                mysql.connection.commit()
                return jsonify('User updated successfully.'), 200


    except Exception as e:
        print(e)
        return str(e), 500


@app.route("/seekers/<string:email>/projects", methods = ["GET", "POST"])
def projects(email):
    try:

        if request.method == "GET":
        
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select date, name, description
                            from projects
                            where semail = '{email}'
                            order by date desc""")
            rv = cursor.fetchall()

            return jsonify(prepDict(rv))

        if request.method == "POST":

            content = request.get_json()
            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select name from projects 
                                where date='{content['date']}' 
                                and semail='{email}'""")

            rv = cursor.fetchone()

            description = get(content, 'description', rv)
            name = get(content, 'name', rv)

            if rv:
                cursor.execute(f"""update projects 
                                    set description='{description}', name='{name}'
                                    where date='{content['date']}' 
                                    and semail='{email}'""")

                
                mysql.connection.commit()

                return jsonify("Updated successfully"), 200
            else:

                query = f"""insert into projects ( description, name, date, semail)
                                    values ('{description}','{name}','{content['date']}','{email}')"""
                
                cursor.execute(query)
                mysql.connection.commit()

                return jsonify("Created successfully"), 200
    except Exception as e:
        print(e)
        return str(e), 500


@app.route("/seekers/<string:email>/projects/delete/<string:date>", methods=['DELETE'])
def deleteProject(email, date):
    
    print(email, date)

    cursor = mysql.connection.cursor()
    query = f"""select name from projects 
                        where date='{date}' 
                        and semail='{email}'"""

    cursor.execute(query)
    rv = cursor.fetchone()

    if not rv:
        return jsonify("Cannot delete"), 405

    cursor.execute(f"""delete from projects 
                        where date='{date}' 
                        and semail='{email}'""")
    mysql.connection.commit()
    return jsonify("deleted successfully"), 200


@app.route("/seekers/<string:email>/certifications", methods = ["GET", "POST"])
def certifications(email):
    try:

        if request.method == "GET":
        
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select date, name, url
                            from certifications
                            where semail = '{email}'
                            order by date desc""")
            rv = cursor.fetchall()

            return jsonify(prepDict(rv))

        if request.method == "POST":

            content = request.get_json()
            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select name from certifications 
                                where url='{content['url']}' 
                                and semail='{email}'""")

            rv = cursor.fetchone()

            url = get(content, 'url', rv)
            name = get(content, 'name', rv)
            date = get(content, 'date', rv)

            if rv:
                cursor.execute(f"""update certifications 
                                    set name='{name}', date = '{date}'

                                    where url='{url}' 
                                    and semail='{email}'""")
                
                mysql.connection.commit()

                return jsonify("Updated successfully"), 200
            else:

                query = f"""insert into certifications ( url, name, date, semail)
                                    values ('{url}','{name}','{content['date']}','{email}')"""
                
                cursor.execute(query)
                mysql.connection.commit()

                return jsonify("Created successfully"), 200
    except Exception as e:
        print(e)
        return str(e), 500

@app.route("/seekers/<string:email>/certifications/delete", methods = ["DELETE"])
def deleteCertification(email):

    url = request.args['url']
    cursor = mysql.connection.cursor()
    cursor.execute(f"""select name from certifications 
                        where url='{url}' 
                        and semail='{email}'""")

    rv = cursor.fetchone()

    if not rv:
        return jsonify("Cannot delete"), 405

    cursor.execute(f"""delete from certifications 
                        where url='{url}' 
                        and semail='{email}'""")
    mysql.connection.commit()
    return jsonify("deleted successfully"), 200

@app.route("/seekers/<string:email>/skills", methods = ["GET", "POST"])
def skills(email):
    try:

        if request.method == "GET":
        
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select skill
                            from skills
                            where semail = '{email}'
                            order by skill asc""")
            rv = cursor.fetchall()

            rv = [x['skill'] for x in rv]

            return jsonify(prepDict(rv))

        if request.method == "POST":

            content = request.get_json()
            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""delete from skills  
                                where semail='{email}'""")

            mysql.connection.commit()


            for skill in content:
                query = f"""insert into skills ( skill, semail)
                                    values ('{skill}','{email}')"""
                
                cursor.execute(query)
            
            mysql.connection.commit()

            return jsonify("Updated successfully"), 200
    except Exception as e:
        print(e)
        return str(e), 500

@app.route("/delete/<int:_id>")
def deleteUser(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute('delete from User where id = %s', _id)
        mysql.connection.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to delete user.')
        response.status_code = 500



# maybe make it a view
@app.route("/fields", methods=['GET'])
def getFields():
    try:

        cursor = mysql.connection.cursor()
        content = request.args

        match_name_segment = "f.ofname like '%{}%'"
        match_description_segment = "f.description like '%{}%'"

        where_list = []
        sort_by = ""

        if 'search' in content:
            where_list.append(f"({match_name_segment.format(content['search'])} or {match_description_segment.format(content['search'])})")

        if 'sort_by' in content:
            if content['sort_by'] == 'name':
                sort_by = "order by name asc"
            elif content['sort_by'] == 'seekers':
                sort_by = "order by n_seekers desc"
            elif content['sort_by'] == "opp":
                sort_by = "order by n_opportunities desc"

        
        where_segment = ""

        if len(where_list):
            where_segment = f"where {' and '.join(where_list)}"

        query = f"""select f.ofname as id, f.ofname as name, 
                        f.description as description,
                        count(distinct(w.semail)) as n_seekers, count(distinct(o.id)) as n_opportunities
                        
                from opportunity_field f 
                    natural left join will_to_work w
                    left join opportunity o on o.opp_field = f.ofname
                {where_segment}
                group by f.ofname
                {sort_by}"""

        if "follower_id" in content:
            query = f"""
            select * from ({query}) Q
            where id in (
                select w.ofname from will_to_work w 
                where w.semail='{content['follower_id']}')
            {sort_by}
            """

        cursor.execute(query)
        rv = cursor.fetchall()
        return jsonify(prepDict(rv))
    except Exception as e:
        raise(e)


@app.route("/fields/follow", methods=['DELETE', 'POST'])
def followField():
    try:
        if request.method == "DELETE":
            content = request.get_json()
            cursor = mysql.connection.cursor()
            query = f'delete from will_to_work where ofname="{content["name"]}" and semail ="{content["uid"]}"'
            
            cursor.execute(query)
            mysql.connection.commit()
            return jsonify('unfollowed'), 200

        else:
            content = request.get_json()
            cursor = mysql.connection.cursor()
            query = f'select * from will_to_work where ofname="{content["name"]}" and semail ="{content["uid"]}"'
            cursor.execute(query)
            
            rv = cursor.fetchone()

            if rv:
                return jsonify("Already followed"), 200

            
            query = f'insert into will_to_work(ofname, semail) values ("{content["name"]}" ,"{content["uid"]}")'
            cursor.execute(query)
            mysql.connection.commit()
            return jsonify('followed'), 200
    except Exception as e:
        print(e)
        return jsonify('Failed to follow. '+str(e)), 500

@app.route("/fields/unfollow", methods=[ 'POST'])
def unfollowField():
    try:
        content = request.get_json()
        cursor = mysql.connection.cursor()
        query = f'delete from will_to_work where ofname="{content["name"]}" and semail ="{content["uid"]}"'
        
        cursor.execute(query)
        mysql.connection.commit()
        return jsonify('unfollowed'), 200

    except Exception as e:
        print(e)
        return jsonify('Failed to follow. '+str(e)), 500


@app.route("/fields/field", methods=['GET', 'POST', 'PATCH', 'DELETE' ])
def field():
    try:

        
        
        if request.method == "GET":
            content = request.args
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select ofname as id, ofname as name, description
                            from opportunity_field
                            where ofname = '{content['name']}'""")
            rv = cursor.fetchone()

            return jsonify(prepDict(rv)), 200

        
        content = request.get_json()

        if request.method == "POST":
            # add new field
            cursor = mysql.connection.cursor()
            cursor.execute(f"""insert into opportunity_field (ofname, description) values('{content['name']}', '{content['description']}')""")
            mysql.connection.commit()

            return jsonify("Added"), 200

        if request.method == "PATCH":
            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""update opportunity_field set ofname='{content['name']}', description='{content['description']}' where ofname='{content['id']}'""")
            mysql.connection.commit()

        if request.method == "DELETE":
            cursor = mysql.connection.cursor()
            cursor.execute(f"""delete from opportunity_field where ofname='{content['id']}'""")
            mysql.connection.commit()

            return jsonify("Deleted"), 200
            

            return jsonify("Edited"), 200

        

    except MySQLdb._exceptions.IntegrityError as e:
        return jsonify('Already exists'), 405

    except Exception as e:
        return jsonify('Failed to get. '+str(e)), 500


@app.route("/organizations", methods=['GET'])
def getOrganizations():
    try:

        cursor = mysql.connection.cursor()
        content = request.args

        match_search = [
            "org.oname like '%{}%'",
            "org.olocation like '%{}%'",
            "org.website like '%{}%'",
        ]

        where_list = []
        join_segment = ""
        sort_by = ""

        if 'search' in content:
            where_list.append(f"({' or '.join([x.format(content['search']) for x in match_search])})")

        if 'location' in content:
            where_list.append(f"org.olocation='{content['location']}'")

        if 'sort_by' in content:
            if content['sort_by'] == 'name':
                sort_by = "order by name asc"
            elif content['sort_by'] == 'mentors':
                sort_by = "order by n_seekers desc"
            elif content['sort_by'] == "opp":
                sort_by = "order by n_opportunities desc"
            elif content['sort_by'] == "comp":
                sort_by = "order by avg_compensation desc"

        
        where_segment = ""

        if len(where_list):
            where_segment = f"where {' and '.join(where_list)}"

        query = f"""select org.oemail as id,org.oname as name, 
                        org.oemail as email, org.website as website,
                        org.olocation as location, org.is_educational as is_educational,
						CASE when n_mentors is null then 0 else n_mentors end as n_mentors, 
                        n_opportunities, 
                        max_compensation, 
                        min_compensation, 
                        avg_compensation
                from organization org
                    natural left join (
                        select work_email as oemail, count(uemail)as n_mentors from alumnus
                        group by work_email
                        ) W
                        
					natural left join (
						select hosting_email as oemail, count(id) as n_opportunities,
                        max(comp_amount) as max_compensation, min(comp_amount) as min_compensation, 
                        avg(comp_amount) as avg_compensation
                        from opportunity
                        group by hosting_email
                        
					) O
                {where_segment}
                {sort_by}"""

        
        cursor.execute(query)
        rv = cursor.fetchall()
        return jsonify(prepDict(rv))
    except Exception as e:
        raise(e)


@app.route("/organizations/<string:oemail>", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def organization(oemail):
    try:

        if request.method=='GET':
            cursor = mysql.connection.cursor()
            
            query = f"""select org.oemail as id,org.oname as name, 
                            org.oemail as email, org.website as website,
                            org.olocation as location, org.is_educational as is_educational,
                            CASE when n_mentors is null then 0 else n_mentors end as n_mentors, 
                            n_opportunities, 
                            max_compensation, 
                            min_compensation, 
                            avg_compensation
                    from organization org
                        natural left join (
                            select work_email as oemail, count(uemail)as n_mentors from alumnus
                            group by work_email
                            ) W
                            
                        natural left join (
                            select hosting_email as oemail, count(id) as n_opportunities,
                            max(comp_amount) as max_compensation, min(comp_amount) as min_compensation, 
                            avg(comp_amount) as avg_compensation
                            from opportunity
                            group by hosting_email
                            
                        ) O
                    where org.oemail = '{oemail}'
                    """

            
            cursor.execute(query)
            rv = cursor.fetchone()

            if not rv: return jsonify("Not found"), 404

            return jsonify(prepDict(rv))

        if request.method == "POST":
            cursor = mysql.connection.cursor()
            content = request.get_json()
            name = content['name']
            website = content['website']
            location = content['location']
            is_educational = 1 if content['is_educational'] else 0
            insert_user_cmd = """INSERT INTO organization(oname, oemail,website,olocation,is_educational, oscore, is_workplace)
                                    VALUES('{}', '{}', '{}', '{}', '{}', 0, 1)"""
            cursor.execute(insert_user_cmd.format(name, oemail,
                        website, location, is_educational))
            mysql.connection.commit()

            
            return jsonify("Added"),200

        if request.method == "PATCH":

            cursor = mysql.connection.cursor()
            content = request.get_json()

            query = f"""
                select oname as name, oemail as email,
                         website, olocation as location, is_educational
                from organization 
                where oemail = '{oemail}'
            """
            cursor.execute(query)

            rv = cursor.fetchone()

            if not rv:
                return jsonify("not found"), 404

            name = get(content, 'name', rv)
            website = get(content, 'website', rv)
            email = get(content, 'email', rv)
            location = get(content, 'location', rv)
            is_educational = 1 if get(content, 'is_educational', rv) else 0
            insert_user_cmd = """Update organization set oname='{}',website='{}',olocation='{}',is_educational='{}', oemail='{}' where oemail='{}'"""
            cursor.execute(insert_user_cmd.format(name,
                        website, location, is_educational,email , oemail))
            mysql.connection.commit()

            
            return jsonify("Added"),200

        if request.method == "DELETE":
            cursor = mysql.connection.cursor()
            insert_user_cmd = """delete from organization where oemail='{}'"""
            cursor.execute(insert_user_cmd.format(oemail))
            mysql.connection.commit()

            return jsonify('deleted'), 200

    except Exception as e:
        raise(e)


# TODO : add a view for organizations names because it is used in many requests
@app.route("/organizations/names")
def organizationNames():
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute("select oemail as org_id, oname as org_name from Organization_name order by oname")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        print(e)
        return str(e), 500


# TODO: make view

@app.route("/opportunities/posted/<string:email>")
def getPostedOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            query = f"""
            select o.* from summary_opportunity o
            where o.poster_email = '{email}'
            """

            cursor.execute(query)
            rv = cursor.fetchall()

            return jsonify(prepDict(rv)), 200
    except Exception as e:
            print(e)
            return str(e), 500


@app.route("/opportunities/associated/<string:email>")
def getAssociateOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            query = f"""
            select o.*, ao.alemail from summary_opportunity o
            join associate ao on ao.opp_id = o.id
            where ao.alemail = '{email}'
            """

            cursor.execute(query)
            rv = cursor.fetchall()

            return jsonify(prepDict(rv)), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/opportunities/matchedSeeker/<string:email>")
def getMatchedSeekerOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            query = f"""
            select distinct o.*, m.mentee_email as seeker_id, concat(u.fname, " ", u.lname) as seeker_name
            from summary_opportunity o
            join apply ap on ap.opp_id = o.id
            join associate ao on ao.opp_id = o.id
            join mentor m on m.mentee_email = ap.semail
            join user u on u.email = m.mentee_email
            where m.mentor_email = '{email}' and (o.poster_email = '{email}' or ao.alemail = '{email}')
            """

            cursor.execute(query)
            rv = cursor.fetchall()

            return jsonify(prepDict(rv)), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()


@app.route("/opportunities/applied/<string:email>")
def getAppliedOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            query = f"""
            select o.* from summary_opportunity o
            join apply ap on ap.opp_id = o.id
            where ap.semail = '{email}'
            """

            cursor.execute(query)
            rv = cursor.fetchall()

            return jsonify(prepDict(rv)), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/opportunities/matchedMentor/<string:email>")
def getMatchedMentorOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            query =  f"""
            select distinct o.*, m.mentor_email as mentor_id, concat(u.fname, " ", u.lname) as mentor_name
            from summary_opportunity o
            join apply ap on ap.opp_id = o.id
            join associate ao on ao.opp_id = o.id
            join mentor m on m.mentee_email = ap.semail
            join user u on u.email = m.mentor_email
            where m.mentee_email = '{email}' and ap.semail = '{email}' and m.status='ongoing'
            """

            cursor.execute(query)
            rv = cursor.fetchall()

            return jsonify(prepDict(rv)), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()



@app.route("/opportunities")
def getOpportunities():
    try:

            content = request.args

            match_search = [
            "o.name like '%{}%'",
            "ox.description like '%{}%'"
            ]

            where_list = []
            join_segment = ""
            sort_by = ""

            if 'search' in content:
                where_list.append(f"({' or '.join([x.format(content['search']) for x in match_search])})")

            if 'uid' in content:
                where_list.append(f"o.poster_email='{content['uid']}'")

            if 'org_id' in content:
                where_list.append(f"o.org_id='{content['org_id']}'")
            
            if 'field_id' in content:
                where_list.append(f"ox.opp_field='{content['field_id']}'")

            if 'start_after' in content:
                where_list.append(f"ox.start_time>'{content['start_after']}'")

            if 'end_before' in content:
                where_list.append(f"ox.end_time<'{content['end_before']}'") 

            if 'sort_by' in content:
                if content['sort_by'] == 'compensation':
                    sort_by = "order by comp_amount desc"
                elif content['sort_by'] == 'seekers':
                    sort_by = "order by o.n_seekers desc"
                elif content['sort_by'] == "mentors":
                    sort_by = "order by o.n_mentors desc"
                elif content['sort_by'] == "deadline":
                    sort_by = "order by app_deadline desc"

            
            where_segment = ""

            if len(where_list):
                where_segment = f"where {' and '.join(where_list)}"

            cursor = mysql.connection.cursor()
            query =  f"""
            
            select  
            o.id as id,
            o.name as name,
            o.org_id as org_id,
            o.org_name as org_name,
            o.location as location,
            ox.end_time as end_date,
            o.poster_email as poster_id,
            o.poster_name as poster_name,
            o.n_seekers as n_seekers,
            o.n_mentors as n_mentors,
            ox.start_time as start_date,
            ox.app_deadline as deadline_date,
            ox.comp_amount as compensation,
            ox.comp_type as compensation_type,
            ox.opp_field as field_id
            from summary_opportunity o
            right outer join opportunity ox on ox.id = o.id
            {where_segment}
            {sort_by}
            """
            cursor.execute(query)
            rv = cursor.fetchall()

            for opp in rv:
                opp['benefits'] = []
                cursor.execute(f"""select benefit
                                    from benefits
                                    where opp_id = '{opp['id']}'""")

                resp = cursor.fetchall()

                for acc in resp:
                    opp['benefits'].append(acc["benefit"])

            return jsonify(prepDict(rv)), 200
    except Exception as e:
            print(e)
            return jsonify(str(e)), 500


@app.route("/opportunities/<int:opp_id>", methods=['GET', 'POST', 'PATCH', "DELETE"])
def opportunity(opp_id):

    if request.method == "GET":
            cursor = mysql.connection.cursor()
            query =  f"""
            
            select  
            o.id as id,
            o.name as name,
            o.org_id as org_id,
            o.org_name as org_name,
            o.location as location,
            ox.end_time as end_date,
            o.poster_email as poster_id,
            o.poster_name as poster_name,
            o.n_seekers as n_seekers,
            o.n_mentors as n_mentors,
            ox.start_time as start_date,
            ox.app_deadline as deadline_date,
            ox.comp_amount as compensation,
            ox.comp_type as compensation_type,
            ox.opp_field as field_id,
            ox.app_portal as application_portal_url,
            ox.description as description
            from summary_opportunity o
            right outer join opportunity ox on ox.id = o.id
            where ox.id = '{opp_id}'
            """

            cursor.execute(query)
            rv = cursor.fetchone()

            rv['benefits'] = []
            cursor.execute(f"""select benefit
                                from benefits
                                where opp_id = '{rv['id']}'""")

            resp = cursor.fetchall()

            for acc in resp:
                rv['benefits'].append(acc["benefit"])

            return jsonify(prepDict(rv)), 200

    elif request.method == "POST":
            cursor = mysql.connection.cursor()
            content = request.get_json()
            query =  f"""

                insert into opportunity (name, alemail, hosting_email, location, end_time, start_time, app_deadline, comp_amount, comp_type, opp_field, app_portal, description)
                values('{content['name']}','{content['poster_id']}','{content['org_id']}',
                '{content['location']}','{content['end_date']}','{content['start_date']}',
                '{content['deadline_date']}','{content['compensation']}','{content['compensation_type']}',
                '{content['field_id']}','{content['application_portal_url']}','{content['description']}')
            
            """
            cursor.execute(query)
            mysql.connection.commit()

            cursor.execute(f"""select id from benefits order by id desc""")

            latest = cursor.fetchone()
        

            if "benefits" in content:
                    
                    for i, acc in enumerate(content["benefits"]):
                        cursor.execute(f"""INSERT INTO benefits (opp_id, benefit) 
                                            values ('{latest['id']}', '{acc}')""")
                        
            mysql.connection.commit()

            return jsonify('User added successfully.'), 200

    elif request.method == "PATCH":
            cursor = mysql.connection.cursor()
            content = request.get_json()

            query =  f"""
            
            select  
            o.id as id,
            o.name as name,
            o.org_id as org_id,
            o.org_name as org_name,
            o.location as location,
            ox.end_time as end_date,
            o.poster_email as poster_id,
            o.poster_name as poster_name,
            o.n_seekers as n_seekers,
            o.n_mentors as n_mentors,
            ox.start_time as start_date,
            ox.app_deadline as deadline_date,
            ox.comp_amount as compensation,
            ox.comp_type as compensation_type,
            ox.opp_field as field_id,
            ox.app_portal as application_portal_url
            from summary_opportunity o
            join opportunity ox on ox.id = o.id
            where ox.id = '{opp_id}'
            """

            cursor.execute(query)
            rv = cursor.fetchone()

            name = get(content, 'name', rv)
            poster_id = get(content, 'poster_id', rv)
            org_id = get(content, 'org_id', rv)
            location = get(content, 'location', rv)
            end_date = get(content, 'end_date', rv)
            start_date = get(content, 'start_date', rv)
            deadline_date = get(content, 'deadline_date', rv)
            compensation = get(content, 'compensation', rv)
            compensation_type = get(content, 'compensation_type', rv)
            field_id = get(content, 'field_id', rv)
            application_portal_url = get(content, 'application_portal_url', rv)
            description = get(content, 'description', rv)

            query =  f"""

                update opportunity set 
                name='{name}', 
                alemail='{poster_id}', 
                hosting_email='{org_id}',
                location='{location}', 
                end_time='{end_date}', 
                start_time='{start_date}', 
                app_deadline='{deadline_date}', 
                comp_amount='{compensation}', 
                comp_type='{compensation_type}', 
                opp_field='{field_id}', 
                app_portal='{application_portal_url}', 
                description='{description}'
                where id = '{opp_id}'
            """

            cursor.execute(query)
            mysql.connection.commit()

            print(content)

            if "benefits" in content:
                    cursor.execute(f"""delete from benefits where opp_id='{opp_id}'""")
                    print(f"""delete from benefits where opp_id='{opp_id}'""")
                    mysql.connection.commit()

                    for i, acc in enumerate(content["benefits"]):
                        cursor.execute(f"""INSERT INTO benefits (opp_id, benefit) 
                                            values ('{opp_id}', '{acc}')""")

            mysql.connection.commit()
            return jsonify('User added successfully.'), 200



    else:
            query =  f"""

                    delete from opportunity
                    where id = '{opp_id}'
                """

            cursor.execute(query)
            mysql.connection.commit()
            return jsonify('User added successfully.'), 200


@app.route("/opportunities/<string:email>/apply/<int:opp_id>", methods=['POST'])
def applyToOpportunity(email, opp_id):
    try:
            cursor = mysql.connection.cursor()
            insert_user_cmd = f"""INSERT INTO apply(semail, opp_id) 
                                VALUES('{email}', {opp_id})"""
            cursor.execute(insert_user_cmd)
            mysql.connection.commit()
            return jsonify('User added successfully.'), 200
    except Exception as e:
            print(e)
            return jsonify('Failed to add user.'), 400 


@app.route("/opportunities/<string:email>/cancel/<string:opp_id>", methods= ["DELETE"])
def cancelApplytoOpportunity(email, opp_id):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""delete from apply where semail = '{email}' and opp_id = '{opp_id}'""")
            mysql.connection.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            return(response)


def _getOpportunityRelation(email,opp_id):
    cursor = mysql.connection.cursor()

    cursor.execute(f"""
        select * from 
        ((select mentor_email, mentee_email, opp_id, status
        from mentor
        join associate ao on mentor_email = ao.alemail)
        union
        (select mentor_email, mentee_email, id, status
        from mentor
        join opportunity ao on mentor_email = ao.alemail)) Q
        where mentor_email = '{email}' and opp_id = {opp_id} and Q.status='ongoing'
    """)

    rv = cursor.fetchone()

    if rv:
        return {
                "rel": "matchedSeeker",
                "uid": rv['mentee_email']
            }
    
    
    cursor.execute(f"""
        select o.id
        from opportunity o
        join associate ao on ao.opp_id = o.id
        where (o.alemail = '{email}' or ao.alemail = '{email}') and o.id = {opp_id}
    """)

    rv = cursor.fetchone()

    if rv:
        return {
                "rel": "associated",
                "uid": None
            }

    cursor.execute(f"""
        select * from 
        ((select mentor_email, mentee_email, opp_id, status
        from mentor
        join associate ao on mentor_email = ao.alemail)
        union
        (select mentor_email, mentee_email, id, status
        from mentor
        join opportunity ao on mentor_email = ao.alemail)) Q
        where mentee_email = '{email}' and opp_id = {opp_id} and Q.status='ongoing'
    """)

    rv = cursor.fetchone()

    if rv:
        return {
                "rel": "matchedMentor",
                "uid": rv['mentor_email']
            }
    

    cursor.execute(f"""
        select o.id
        from opportunity o
        join apply ao on ao.opp_id = o.id
        where ao.semail = '{email}' and o.id = {opp_id}
    """)

    rv = cursor.fetchone()

    if rv:
        return {
                "rel": "applied",
                "uid": None
            }

    return {
                "rel": "no_rel",
                "uid": None
            }


@app.route("/opportunities/<string:email>/rel/<int:opp_id>")
def getOpportunityRelation(email,opp_id):
    try:
            
            return jsonify(_getOpportunityRelation(email, opp_id)), 200

    except Exception as e:
            print(e)
            return jsonify(str(e)), 500


@app.route("/opportunities/<string:opp_id>/benefits", methods=['GET','POST', 'PATCH'])
def getOpportunityBenefits(opp_id):
    try:

            if request.method  == 'GET':
                cursor = mysql.connection.cursor()
                cursor.execute(f"""select opp_id, benefit from benefits where opp_id = '{opp_id}'""")           
                rv = cursor.fetchall()
                return jsonify(prepDict(rv)), 200
            
            if request.method == "POST":
                cursor = mysql.connection.cursor()
                content = request.get_json()
                benefit = content["benefit"]
                insert_user_cmd = f"""INSERT INTO benefits(opp_id, benefit) 
                                    VALUES('{opp_id}', '{benefit}')"""
                cursor.execute(insert_user_cmd)
                mysql.connection.commit()
                return jsonify("Success"), 200

            if request.method == "PATCH":
                cursor = mysql.connection.cursor()
                content = request.get_json()

                benefit = content["benefit"]
                update_user_cmd = f"""update benefits
                                    set benefit='{benefit}'
                                    where opp_id= '{opp_id}' and benefit='{content['id']}'"""
                
                print(update_user_cmd)
                cursor.execute(update_user_cmd)
                mysql.connection.commit()

                return jsonify("Success"), 200

    except Exception as e:
            print(e)
            return jsonify(str(e)), 500


@app.route("/opportunities/<string:opp_id>/benefits/delete", methods=['POST'])
def deleteOpportunityBenefit(opp_id):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""delete from opp_comp_benefits where opp_id = '{opp_id}' and benefit = '{request.get_json()['benefit']}'""")
            mysql.connection.commit()
            return jsonify("Success"), 200
    except Exception as e:
            print(e)
            return jsonify(str(e)), 500

@app.route("/opportunities/<string:email>/associate/<int:opp_id>", methods=['POST', 'DELETE'])
def associateOpportunity(email,opp_id):
    try:

            if request.method== 'POST':
                cursor = mysql.connection.cursor()
                cursor.execute(f"""insert into associate(alemail, opp_id) values ('{email}', '{opp_id}') """)            
                mysql.connection.commit()
                return jsonify("Success"), 200
            else:
                cursor = mysql.connection.cursor()
                cursor.execute(f"""delete from associate where alemail='{email}' and opp_id= '{opp_id}'""")            
                mysql.connection.commit()
                return jsonify("Success"), 200
    except Exception as e:
            print(e)

@app.route("/opportunities/<int:opp_id>/<string:mentor_email>/mentor/<string:seeker_email>", methods=['POST'])
def matchMentoring(mentor_email, seeker_email, opp_id):
    try:
            #aaliyah.brooks@gmail.com
            #ariana.reyes@gmail.com


            relMentor = _getOpportunityRelation(mentor_email, opp_id)
            relSeeker = _getOpportunityRelation(seeker_email, opp_id)
            
            if not (relMentor['rel'] == "associated" and relSeeker['rel'] == "applied"):
                return jsonify("cannot mentor"), 403

            cursor = mysql.connection.cursor()
            
            cursor.execute(f"""
                delete from mentor 
                where mentor_email = '{mentor_email}' and mentee_email='{seeker_email}'
            """)

            mysql.connection.commit()

            insert_user_cmd = f"""INSERT INTO mentor (mentor_email,mentee_email, status, start_date, rating) 
                                VALUES('{mentor_email}', '{seeker_email}', 'ongoing', '{date.today().strftime('%Y-%m-%d')}', 0) 
                                """
            
            cursor.execute(insert_user_cmd)
            mysql.connection.commit()

            return jsonify("Success"), 200
            
    except Exception as e:
            print(e)
            return jsonify(str(e)), 500


@app.route("/opportunities/<int:opp_id>/<string:mentor_email>/finishMentoring/<string:seeker_email>", methods=['POST'])
def finishMentoring(opp_id, mentor_email, seeker_email):
    try:
            
            cursor = mysql.connection.cursor()
            content = request.get_json()
            rating = content["rating"]
            print(content)
            update_user_cmd = f"""update mentor
                                 set rating='{rating}', status="finished"
                                 where mentor_email='{mentor_email}' and mentee_email='{seeker_email}' and status='ongoing'"""
            cursor.execute(update_user_cmd)
            mysql.connection.commit()
            return jsonify("Success"), 200
    except Exception as e:
            print(e)
            return jsonify("Error"), 500

@app.route("/opportunities/<int:opp_id>/<string:mentor_email>/cancelMentoring/<string:seeker_email>", methods=['POST'])
def cancelMentoring(opp_id, mentor_email, seeker_email):
    try:
            
            cursor = mysql.connection.cursor()

            update_user_cmd = f"""update mentor
                                 set status="canceled"
                                 where mentor_email='{mentor_email}' and mentee_email='{seeker_email}' and status='ongoing'"""
            
            print(update_user_cmd)
            
            cursor.execute(update_user_cmd)
            mysql.connection.commit()
            return jsonify("Success"), 200
    except Exception as e:
            print(e)
            return jsonify("Error"), 500

@app.route("/messages/<string:sender>/message/<string:receiver>", methods=['GET','POST'])
def message(sender, receiver):
    try:

            if request.method == "POST":
                cursor = mysql.connection.cursor()
                content = request.get_json()
                message = content['message']
                insert_user_cmd = f"""INSERT INTO message(sender_email, receiver_email, content, timestamp) 
                                    VALUES('{sender}', '{receiver}', '{message}', '{(str(datetime.now()))}')"""

                print(insert_user_cmd)
                cursor.execute(insert_user_cmd)
                mysql.connection.commit()
                return jsonify("Success"), 200

            if request.method == "GET":

                cursor = mysql.connection.cursor()
                insert_user_cmd = f"""select * from message where 
                (sender_email = '{sender}' and receiver_email = '{receiver}') or
                (sender_email = '{receiver}' and receiver_email = '{sender}')
                order by timestamp asc """
                cursor.execute(insert_user_cmd)

                rv = cursor.fetchall()

                messages = []

                for message in rv:

                    if message['sender_email'] == sender:
                        messages.append({
                            'type':'sent',
                            'message': message['content'],
                            'timestamp': message['timestamp']
                        })
                    
                    else:
                        messages.append({
                            'type':'received',
                            'message': message['content'],
                            'timestamp': message['timestamp']
                        })

                return jsonify(messages), 200
                
    except Exception as e:
            raise(e)
            


@app.route("/users")
def getUsers():
    try:

            query = request.args
            cursor = mysql.connection.cursor()

            where_list = []
            if 'search' in query:
                where_list.append("concat(fname, \" \", lname) like '%"+query['search']+"%'")

        
            if 'type' in query:

                if query['type'] == "M":
                    where_list.append("email in (select uemail from alumnus)")

                else:
                    where_list.append("email in (select uemail from student)")
            
            where_segment = ""

            if len(where_list):
                where_segment = "where "+" and ".join(where_list)

            x = f"""select concat(fname, \' \', lname) as name, email as id 
            from user
            {where_segment}
            order by fname, lname
            """
            print(x)
            cursor.execute(x)
            rv = cursor.fetchall()
            return jsonify(prepDict(rv)),200
    except Exception as e:
            print(e)
            return jsonify(str(e)),500

@app.route("/mentors/<int:opp_id>")
def getMentors(opp_id):
    
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""(select concat(fname, " ", lname) as name, email as id, avg(m.rating) as score 
                                from associate
                                join user on alemail = email
                                left join mentor m on mentor_email = alemail
                                where opp_id = '{opp_id}'
                                group by email)
                               union
                               (
                                select concat(fname, " ", lname) as name, email as id, avg(m.rating) as score 
                                from opportunity o
                                join user on alemail = email
                                left join mentor m on mentor_email = alemail
                                where o.id = '{opp_id}'
                                group by email
                               )""")
            rv = cursor.fetchall()
            return jsonify(prepDict(rv)),200
    except Exception as e:
            print(e)
            return jsonify(str(e)),500


@app.route("/seekers/<int:opp_id>")
def getSeekers(opp_id):
    try:
            query = request.args

            where_segment = f"where ao.opp_id='{opp_id}'"

            if 'pending' in query:
                where_segment += f""" and user.email not in (
                        select distinct mentee_email 
                        from mentor 
                        join associate ac on ac.alemail = mentor_email
                        where ac.opp_id = '{opp_id}' and (status='ongoing' or status='finished')
                    )
                    """

            cursor = mysql.connection.cursor()
            cursor.execute(f"""select distinct concat(fname, " ", lname) as name, email as id 
                               from user
                               join apply ao on ao.semail = user.email
                                {where_segment}
                               """)
            rv = cursor.fetchall()
            return jsonify(prepDict(rv)),200
    except Exception as e:
            print(e)
            return jsonify(str(e)),500

@app.route("/mentoringMentors/<string:email>")
def getMentoringmentors(email):
    try:
            query = request.args

            where = ""
            if 'opp_id' in query:
                opp_id = query['opp_id']
                where = f""" and m.mentor_email in (
                        (select alemail from associate where opp_id = '{opp_id}')
                        union
                        (select alemail from opportunity where id  = '{opp_id}')
                    )
                    """

            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select distinct concat(fname, " ", lname) as name, email as id 
                               from user
                               join mentor m on m.mentor_email = user.email
                               where m.mentee_email = '{email}' and status= 'ongoing' {where}
                               """)
            
            rv = cursor.fetchall()
            return jsonify(prepDict(rv)),200
    except Exception as e:
            print(e)
            return jsonify(str(e)),500


@app.route("/mentoredSeekers/<string:email>")
def getMentoredSeekers(email):
    try:
            query = request.args

            where = ""
            if 'opp_id' in query:
                opp_id = query['opp_id']
                where = f""" and m.mentee_email in (
                        select semail from apply where opp_id = '{opp_id}'
                    )
                    """

            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select distinct concat(fname, " ", lname) as name, email as id 
                               from user
                               join mentor m on m.mentee_email = user.email
                               where m.mentor_email = '{email}' and status='ongoing' {where}
                               """)
            
            rv = cursor.fetchall()
            return jsonify(prepDict(rv)),200
    except Exception as e:
            print(e)
            return jsonify(str(e)),500



app.run(debug=True)
