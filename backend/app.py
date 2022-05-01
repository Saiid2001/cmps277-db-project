
from decouple import config
from flask import Flask, request, jsonify, session
from flask_session import Session
from flask_mysqldb import MySQL, MySQLdb
from datetime import date, datetime

app = Flask(__name__)

app.config['MYSQL_HOST'] = config("mysql_hostname")
app.config['MYSQL_USER'] = config("mysql_user")
app.config['MYSQL_PASSWORD'] = config("mysql_password")
app.config['MYSQL_DB'] = config("mysql_db")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

SESSION_TYPE = 'memcashed'
app.config.from_object(__name__)
Session(app)


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


@app.route('/login', methods=['POST'])
def login():

    content = request.form
    cursor = mysql.connection.cursor()
    cursor.execute(f"""select email as uid from user where email='{content['email']}' and pass=sha1('{content['password']}') """)

    rv = cursor.fetchone()

    if not rv:
        return jsonify("Wrong email/password"), 403

    session['user'] = content['email'] 
    return jsonify("Logged in"), 200
    



@app.route("/users/<string:email>", methods=['GET', 'POST'])
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

                insert_user_cmd = f"""INSERT INTO User(email, fname, lname, dob, linked_in, website, phone, gender)
                                    VALUES('{email}', '{first_name}', '{last_name}',
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

        if rv == None:
            return "S"
        else:

            cursor = mysql.connection.cursor()
            cursor.execute(f"select uemail from student where uemail='{email}'")
            rv = cursor.fetchone()
            cursor.close()

            if rv == None:
                return None
            return "M"

@app.route("/users/<string:email>/type")
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
                                    VALUES('{email}', '{org_id}', '{position}')"""
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
                return jsonify(rv), 200
            else:
                return jsonify("Seeker does not exist"), 404

        else:

            content = request.get_json()

            sop = get(content, "sop", rv)
            open_to_work = get(content, "open_to_work", rv)

            if not rv:

                if _getUserType(email) == "M":
                    return jsonify("Already mentor"), 405

                insert_user_cmd = f"""INSERT INTO Student(sop, is_open_work)
                                        VALUES({sop}, {open_to_work})"""
                cursor.execute(insert_user_cmd)
                mysql.connection.commit()
                return jsonify(
                    message='User added successfully.'), 200

            else:
                update_user_cmd = """update Student
                                    set sop='{sop}', is_open_work='{open_to_work}'
                                    where uemail='{email}'"""
                cursor.execute(update_user_cmd)
                mysql.connection.commit()
                return jsonify('User updated successfully.'), 200


    except Exception as e:
        print(e)
        return str(e), 500


@app.route("/seekers/<string:email>/projects", methods = ["GET", "POST", "DELETE"])
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

        if request.method == "DELETE":
            content = request.get_json()
            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select name from projects 
                                where date='{content['date']}' 
                                and semail='{email}'""")

            rv = cursor.fetchone()

            if not rv:
                return jsonify("Cannot delete"), 405

            cursor.execute(f"""delete from projects 
                                where date='{content['date']}' 
                                and semail='{email}'""")
            mysql.connection.commit()
            return jsonify("deleted successfully"), 200

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


@app.route("/seekers/<string:email>/certifications", methods = ["GET", "POST", "DELETE"])
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

        if request.method == "DELETE":
            content = request.get_json()
            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select name from certifications 
                                where url='{content['url']}' 
                                and semail='{email}'""")

            rv = cursor.fetchone()

            if not rv:
                return jsonify("Cannot delete"), 405

            cursor.execute(f"""delete from certifications 
                                where url='{content['url']}' 
                                and semail='{email}'""")
            mysql.connection.commit()
            return jsonify("deleted successfully"), 200

        if request.method == "POST":

            content = request.get_json()
            
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select name from certifications 
                                where url='{content['url']}' 
                                and semail='{email}'""")

            rv = cursor.fetchone()

            url = get(content, 'url', rv)
            name = get(content, 'name', rv)

            if rv:
                cursor.execute(f"""update certifications 
                                    set name='{name}'
                                    where url='{content['url']}' 
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
        content = request.get_json()

        match_name_segment = "f.ofname like '%{}%'"
        match_description_segment = "f.description like '%{}%'"

        where_list = []
        join_segment = ""
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


@app.route("/fields/field", methods=['GET', 'POST', 'PATCH', 'DELETE' ])
def field():
    try:

        
        content = request.get_json()
        
        if request.method == "GET":
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select ofname as id, ofname as name, description
                            from opportunity_field
                            where ofname = '{content['id']}'""")
            rv = cursor.fetchone()

            return jsonify(prepDict(rv)), 200

        if request.method == "POST":
            # add new field
            cursor = mysql.connection.cursor()
            cursor.execute(f"""insert into opportunity_field (ofname, description) values('{content['name']}', '{content['description']}')""")
            mysql.connection.commit()

            return jsonify("Added"), 200

        if request.method == "PATCH":
            cursor = mysql.connection.cursor()
            cursor.execute(f"""update opportunity_field set description='{content['description']}' where ofname='{content['id']}'""")
            mysql.connection.commit()

            return jsonify("Edited"), 200

        if request.method == "DELETE":
            cursor = mysql.connection.cursor()
            cursor.execute(f"""delete from opportunity_field where ofname='{content['id']}'""")
            mysql.connection.commit()

            return jsonify("Deleted"), 200

    except MySQLdb._exceptions.IntegrityError as e:
        return jsonify('Already exists'), 405

    except Exception as e:
        return jsonify('Failed to get. '+str(e)), 500


@app.route("/organizations", methods=['GET'])
def getOrganizations():
    try:

        cursor = mysql.connection.cursor()
        #content = request.get_json()
        content = {
            'search': "Croatia"

        }

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
            location = get(content, 'location', rv)
            is_educational = 1 if get(content, 'is_educational', rv) else 0
            insert_user_cmd = """Update organization set oname='{}',website='{}',olocation='{}',is_educational='{}' where oemail='{}'"""
            cursor.execute(insert_user_cmd.format(name,
                        website, location, is_educational, oemail))
            mysql.connection.commit()

            
            return jsonify("Added"),200

        if request.method == "DELETE":
            insert_user_cmd = """delete from organization where oemail='{}'"""
            cursor.execute(insert_user_cmd.format(oemail))

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


app.run(debug=True)