import re
from decouple import config
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import date, datetime
import json
import pymysql

app = Flask(__name__)

app.config['MYSQL_HOST'] = config("mysql_hostname")
app.config['MYSQL_USER'] = config("mysql_user")
app.config['MYSQL_PASSWORD'] = config("mysql_password")
app.config['MYSQL_DB'] = config("mysql_db")
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)


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

@app.route("/")
def index():
    return jsonify({"status": "running", "time": str(datetime.now())})


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


@app.route("/users/<string:email>/education", methods = ["GET", "DELETE"])
def educations(email):
    try:
        
        cursor = mysql.connection.cursor()
        cursor.execute(f"""select id, major, inst_email as org_id,  oname as org_name, 
                                score, start_date as start_at, end_date as end_at, major
                        from Complete_Program
                        join organization_name on inst_email = oemail
                        where uemail = '{email}'""")
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
        
# TODO : add a view for organizations names because it is used in many requests
@app.route("/organizations/names")
def organizationNames():
    try:

        cursor = mysql.connection.cursor()
        cursor.execute("select oemail as org_id, oname as org_name from Organization_name sort by oname")
        rows = cursor.fetchall()
        return jsonify(rows), 200
    except Exception as e:
        print(e)
        return str(e), 500
      

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
     


@app.route("/display/experiences/<int:id>")
def getExperience(id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute(
            "select org_id, start_date, end_date, position, accomplishments, org_name from Alum_Experience_Org a, Organization o where a.org_id = o.id and a.id=%s ", id)
        # row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchone()
        # json_data=[dict(zip(row_headers,rv))]
        # for result in rv:
        #   json_data.append(dict(zip(row_headers,result)))
        return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
      


@app.route("/set/Experience", methods=['GET', 'POST'])
def setExperience(_id):
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        _id = content['uid']
        position = content['position']
        org_id = content['org_id']
        org_name = content['org_name']
        start_at = content['start_at']
        end_at = content['end_at']
        accomplishments = content['accomplishments']
        select_user_cmd = (
            "select id, org_id, start_at from Alum_Experience_Org where id =%s, org_id=%s, start_at=%s")
        cursor.execute(select_user_cmd, (_id, org_id, start_at))
        rv = cursor.fetchone()

        if not rv:
            insert_user_cmd = """INSERT INTO Alum_Experience_Org(position, org_id, start_at, end_at, accomplishments)
                                    VALUES(%s, %s, %s, %s, %s, %s)"""
            cursor.execute(insert_user_cmd, (position, org_id,
                           start_at, end_at, accomplishments))
            mysql.connection.commit()
            response = jsonify(
                message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        else:
            update_user_cmd = """update Alum_Experience_Org
                                 set position=%s, org_id=%s, start_at=%s, end_at=%s, accomplishments=%s
                                 where id=%s and org_id=%s and start_at=%s"""
            cursor.execute(update_user_cmd, (position, org_id, start_at,
                           end_at, accomplishments, id, org_id, start_at))
            mysql.connection.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/delete/experience/<int:id>")
def deleteExperience(id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute('delete from Alum_Experience_Org where id = %s', id)
        mysql.connection.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to delete user.')
        response.status_code = 500
     


@app.route("/display/projects/<int:id>")
def getProjects(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute(
            "select name, description, date from Student_Project where id = %s", _id)
        # row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchone()
        # json_data=[dict(zip(row_headers,rv))]
        # for result in rv:
        #   json_data.append(dict(zip(row_headers,result)))
        return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
      


@app.route("/set/project/<int:_id>", methods=['GET', 'POST'])
def setProject(_id):
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        _id = content['uid']
        name = content['name']
        _date = content['date']
        description = content['description']
        select_user_cmd = (
            "select id, name, date from Student_Project where id =%s, name=%s, date=%s")
        cursor.execute(select_user_cmd, (_id, name, _date))
        rv = cursor.fetchone()

        if not rv:
            insert_user_cmd = """INSERT INTO Student_Project(id, name, date, description)
                                VALUES(%s, %s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_id, name, _date, description))
            mysql.connection.commit()
            response = jsonify(
                message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        else:
            update_user_cmd = """update Student_Project
                                 set name=%s, date=%s, description=%s
                                 where id=%s and name=%s and date=%s"""
            cursor.execute(update_user_cmd, (name, _date,
                           description, _id, name, _date))
            mysql.connection.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200

    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/delete/project/<int:_id>")
def deleteProject(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute('delete from Student_Project where id = %s', _id)
        mysql.connection.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to delete user.')
        response.status_code = 500
     


@app.route("/display/certification/<int:_id>")
def getCertifications(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute(
            "select name, url, date from Student_Certification where id = %s", _id)
        # row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchall()
        # json_data=[dict(zip(row_headers,rv))]
        # for result in rv:
        #   json_data.append(dict(zip(row_headers,result)))
        return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
      


@app.route("/set/certification", methods=['GET', 'POST'])
def setCertification(_id):
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        _id = content['uid']
        name = content['name']
        date = content['date']
        url = content['url']
        select_user_cmd = (
            "select id, name, date from Student_Certification where id =%s and name=%s and date=%s")
        cursor.execute(select_user_cmd, (_id, name, date))
        rv = cursor.fetchone()

        if not rv:
            insert_user_cmd = """INSERT INTO Student_Certification(id, name, date, url)
                                VALUES(%s, %s, %s, %s)"""
            cursor.execute(insert_user_cmd, (_id, name, date, url))
            mysql.connection.commit()
            response = jsonify(
                message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        else:
            update_user_cmd = """update Student_Certification
                                 set name=%s, date=%s, url=%s
                                 where id=%s and name=%s and date=%s"""
            cursor.execute(update_user_cmd, (name, date, url, _id, name, date))
            mysql.connection.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200

    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/delete/certification/<int:id>")
def deleteCertification(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute('delete from Student_Certification where id = %s', _id)
        mysql.connection.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to delete user.')
        response.status_code = 500
     


@app.route("/display/skills/<int:id>")
def getSkills(id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute("select name from Student_Skill where id = %s", id)
        # row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchone()
        # json_data=[dict(zip(row_headers,rv))]
        # for result in rv:
        #   json_data.append(dict(zip(row_headers,result)))
        return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
      


@app.route("/set/skills", methods=['GET', 'POST'])
def setSkills(_id):
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        _id = content['uid']
        name = content['name']
        select_user_cmd = (
            "select id, name from Student_Skill where id =%s and name=%s")
        cursor.execute(select_user_cmd, (_id, name))
        rv = cursor.fetchone()

        if not rv:
            insert_user_cmd = """INSERT INTO Student_Skill(id, name)
                                VALUES(%s, %s)"""
            cursor.execute(insert_user_cmd, (_id, name))
            mysql.connection.commit()
            response = jsonify(
                message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        else:
            update_user_cmd = """update Student_Skill
                                 set name=%s
                                 where id=%s and name=%s"""
            cursor.execute(update_user_cmd, (name, _id, name))
            mysql.connection.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200

    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/delete/followField/<int:_id>")
def unfollowField(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute('delete from Stud_Will_Work_Field where id = %s', _id)
        mysql.connection.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to delete user.')
        response.status_code = 500
     


@app.route("/set/followField", methods=['GET', 'POST'])
def followField(_id):
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        _id = content['uid']
        name = content['fieldId']
        select_user_cmd = (
            "select id, name from Stud_Will_Work_Field where id =%s and name=%s")
        cursor.execute(select_user_cmd, (_id, name))
        rv = cursor.fetchone()

        if not rv:
            insert_user_cmd = """INSERT Stud_Will_Work_Field(id, name)
                                VALUES(%s, %s)"""
            cursor.execute(insert_user_cmd, (_id, name))
            mysql.connection.commit()
            response = jsonify(
                message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
        else:
            update_user_cmd = """update Stud_Will_Work_Field
                                 set name=%s
                                 where id=%s and name=%s"""
            cursor.execute(update_user_cmd, (name, _id, name))
            mysql.connection.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200

    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/display/fields/")
def getFields():
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        name = content['name']
        sort_by_factor = content['sort_by']
        if name == pymysql.NULL and sort_by_factor == pymysql.NULL:
            cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif sort_by_factor == pymysql.NULL:
            cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name having field_name =%s", name)
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif name == pymysql.NULL and sort_by_factor == "name":
            cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name order by field_name")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif name == pymysql.NULL and sort_by_factor == "seekers":
            cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name order by n_seekers desc")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif name == pymysql.NULL and sort_by_factor == "opp":
            cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name order by n_opportunities desc")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
      


app.route("/display/field/")


def getField(_id):
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        _id = content['id']
        cursor.execute(
            "select id, name, description from opp_field where id = %s", _id)
        # row_headers=[x[0] for x in cursor.description] #this will extract row headers
        rv = cursor.fetchone()
        # json_data=[dict(zip(row_headers,rv))]
        # for result in rv:
        #   json_data.append(dict(zip(row_headers,result)))
        return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
      


@app.route("/set/Field", methods=['GET', 'POST'])
def addField():
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        name = content['name']
        description = content['description']
        insert_user_cmd = """INSERT INTO opp_field(name, description)
                                VALUES(%s, %s)"""
        cursor.execute(insert_user_cmd, (name, description))
        mysql.connection.commit()
        response = jsonify(
            message='User added successfully.', id=cursor.lastrowid)
        #response.data = cursor.lastrowid
        response.status_code = 200
    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/edit/Field", methods=['GET', 'POST'])
def editField():
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        name = content['name']
        description = content['description']
        update_user_cmd = """update opp_field
                                 set description=%s
                                 where name=%s"""
        cursor.execute(update_user_cmd, (description, name))
        mysql.connection.commit()
        response = jsonify('User updated successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/delete/Field/<int:id>")
def deleteField(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute('delete from opp_field where id = %s', _id)
        mysql.connection.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to delete user.')
        response.status_code = 500
     


@app.route("/display/organizations/")
def getOrganizations():
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        name = content['name']
        sort_by_factor = content['sort_by']
        if name == pymysql.NULL and sort_by_factor == pymysql.NULL:
            cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif sort_by_factor == pymysql.NULL:
            cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name having org.name =%s", name)
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif name == pymysql.NULL and sort_by_factor == "name":
            cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name order by org.name")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif name == pymysql.NULL and sort_by_factor == "mentors":
            cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name order by n_mentor desc")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
        elif name == pymysql.NULL and sort_by_factor == "opp":
            cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name order by n_opportunities desc")
            # row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            # json_data=[dict(zip(row_headers,rv))]
            # for result in rv:
            #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(prepDict(rv))
    except Exception as e:
        print(e)
      


@app.route("/set/Org", methods=['GET', 'POST'])
def addOrganization():
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        name = content['name']
        email = content['email']
        website = content['website']
        location = content['location']
        is_educational = content['is_educational']
        insert_user_cmd = """INSERT INTO organization(name, email,website,location,is_educational)
                                VALUES(%s, %s, %s, %s, %s)"""
        cursor.execute(insert_user_cmd, (name, email,
                       website, location, is_educational))
        mysql.connection.commit()
        response = jsonify(
            message='User added successfully.', id=cursor.lastrowid)
        #response.data = cursor.lastrowid
        response.status_code = 200
    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/edit/Field", methods=['GET', 'POST'])
def editOrganization():
    try:

        cursor = mysql.connection.cursor()
        content = request.get_json()
        name = content['name']
        email = content['email']
        website = content['website']
        location = content['location']
        is_educational = content['is_educational']
        update_user_cmd = """update organization
                                 set email=%s, website=%s, location=%s, is_educational=%s
                                 where name=%s"""
        cursor.execute(update_user_cmd, (email, website,
                       location, is_educational, name))
        mysql.connection.commit()
        response = jsonify('User updated successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        return jsonify(str(e)), 500
     


@app.route("/delete/Field/<int:id>")
def deleteOrganization(_id):
    try:

        cursor = mysql.connection.cursor()
        cursor.execute('delete from Organization where id = %s', _id)
        mysql.connection.commit()
        response = jsonify('User deleted successfully.')
        response.status_code = 200
    except Exception as e:
        print(e)
        response = jsonify('Failed to delete user.')
        response.status_code = 500
     


if __name__ == "__main__":
    app.run(debug=True)
