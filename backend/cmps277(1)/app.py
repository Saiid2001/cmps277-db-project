import re
from flask import Flask, render_template, request, redirect,jsonify
from flaskext.mysql import MySQL
from datetime import date
import json
import pymysql

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MyNewPass'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'

mysql = MySQL()
mysql.init_app(app)


@app.route("/set", methods=['GET','POST'])
def addUser():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            first_name = content['first_name']
            last_name = content['last_name']
            birth_date = content['birth_date']
            linkedin = content['linkedin']
            website = content['website']
            phone = content['phone']
            select_user_cmd = ("select id from User where id =%s")
            cursor.execute(select_user_cmd, (_id,))
            rv = cursor.fetchone()

            if not rv: 

                insert_user_cmd = """INSERT INTO User(first_name, last_name, birth_date, linkedin, website, phone) 
                                    VALUES(%s, %s, %s, %s, %s, %s)"""
                cursor.execute(insert_user_cmd, (first_name, last_name, birth_date, linkedin, website, phone))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200
            else: 
                update_user_cmd = """update User 
                                 set first_name=%s, last_name=%s, birth_date=%s, linkedin=%s, website=%s, phone=%s
                                 where id=%s"""
                cursor.execute(update_user_cmd, (first_name, last_name, birth_date, linkedin, website, phone, _id))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/display/<int:_id>/")
def getUser(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute('select * from User where id = %s',_id)
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchone()
            #json_data=[dict(zip(row_headers,rv))]
            #for result in rv:
             #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:   
            cursor.close()
            conn.close()



@app.route("/display/organizations")
def getAllOrganizationNames():
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select id, name from Organization")
            rows = cursor.fetchall()
            return jsonify(rows)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()
    

@app.route("/delete/<int:_id>")
def deleteUser(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from User where id = %s',_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response) 
    

@app.route("/set/education/<int:_id>", methods=['GET','POST'])
def setEducation(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            major = content['major']
            org_id = content['org_id']
            org_name = content['org_name']
            score = content['score']
            start_date = content['start_at']
            end_date = content['end_at']
            accomplishments = content['accomplishments']
            select_user_cmd = ("select id, org_id, start_date, end_date from User_Complete_Prog where id =%s and org_id = %s and start_date=%s and end_date=%s")
            cursor.execute(select_user_cmd, (_id, org_id, start_date, end_date))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT INTO User_Complete_Prog(id, major, org_id, org_name, score, start_date, end_date, accomplishments) 
                                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(insert_user_cmd, (_id, major, org_id, org_name, score, start_date, end_date, accomplishments))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200

            else: 
                update_user_cmd = """update User_Complete_Prog 
                                 set major=%s, org_id=%s, org_name=%s, score=%s, start_date=%s, end_date=%s, accomplishments=%s
                                 where id=%s and org_id = %s and start_date=%s and end_date=%s"""
                cursor.execute(update_user_cmd, (major, org_id, org_name, score, start_date, end_date, accomplishments,_id, org_id, start_date, end_date))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/display/education")
def getEducations():
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select * from User_Complete_Prog")
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            #json_data=[]
            #for result in rv:
                #json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/delete/education/<int:_id>")
def deleteEducation(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from User_Complete_Prog where id = %s',_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response) 
@app.route("/display/seekerData/<int:id>")
def getSeekerData(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select sop, is_open_work as open_to_work from Student where id=%s", _id)
            rows = cursor.fetchone()
            return jsonify(rows)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/set/seekerData", methods=['GET','POST'])
def setSeekerData():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            sop = content['sop']
            is_open_work = content['open_to_work']
            select_user_cmd = ("select _id from Student where id =%s")
            cursor.execute(select_user_cmd, (_id,))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT INTO Student(sop, is_open_work) 
                                    VALUES(%s, %s)"""
                cursor.execute(insert_user_cmd, (sop, is_open_work))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200
            else: 
                update_user_cmd = """update Student 
                                 set sop=%s, is_open_work=%s
                                 where id=%s"""
                cursor.execute(update_user_cmd, (sop, is_open_work, _id))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)



@app.route("/display/currentPosition/<int:_id>")
def getCurrentPosition(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select a.position as position, o.name as org_name, org_id from Organization o, Alumnus a where org_id = o.id and a.id = %s", _id)
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchone()
            #json_data=[dict(zip(row_headers,rv))]
            #for result in rv:
             #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/set/currentPosition/<int:_id>", methods=['GET','POST'])
def setCurrentPosition(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            org_id = content['org_id']
            position = content['position']
            select_user_cmd = ("select id from Alumnus where id =%s")
            cursor.execute(select_user_cmd, (_id,))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT INTO Alumnus(id, org_id, position) 
                                    VALUES(%s, %s, %s, %s)"""
                cursor.execute(insert_user_cmd, (_id, org_id, position))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200

            else: 
                update_user_cmd = """update Alumnus 
                                 set org_id=%s, position=%s
                                 where id=%s"""
                cursor.execute(update_user_cmd, (org_id, position, _id))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/display/experiences/<int:id>")
def getExperience(id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select org_id, start_date, end_date, position, accomplishments, org_name from Alum_Experience_Org a, Organization o where a.org_id = o.id and a.id=%s ", id)
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchone()
            #json_data=[dict(zip(row_headers,rv))]
            #for result in rv:
             #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/set/Experience", methods=['GET','POST'])
def setExperience(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            position = content['position']
            org_id = content['org_id']
            org_name = content['org_name']
            start_at = content['start_at']
            end_at = content['end_at']
            accomplishments = content['accomplishments']
            select_user_cmd = ("select id, org_id, start_at from Alum_Experience_Org where id =%s, org_id=%s, start_at=%s")
            cursor.execute(select_user_cmd, (_id, org_id, start_at))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT INTO Alum_Experience_Org(position, org_id, start_at, end_at, accomplishments) 
                                    VALUES(%s, %s, %s, %s, %s, %s)"""
                cursor.execute(insert_user_cmd, (position, org_id, start_at, end_at, accomplishments))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200
            else: 
                update_user_cmd = """update Alum_Experience_Org 
                                 set position=%s, org_id=%s, start_at=%s, end_at=%s, accomplishments=%s
                                 where id=%s and org_id=%s and start_at=%s"""
                cursor.execute(update_user_cmd, (position, org_id, start_at, end_at, accomplishments, id, org_id, start_at))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)
@app.route("/delete/experience/<int:id>")
def deleteExperience(id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from Alum_Experience_Org where id = %s',id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response) 

@app.route("/display/projects/<int:id>")
def getProjects(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select name, description, date from Student_Project where id = %s", _id)
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchone()
            #json_data=[dict(zip(row_headers,rv))]
            #for result in rv:
             #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/set/project/<int:_id>", methods=['GET','POST'])
def setProject(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            name = content['name']
            _date = content['date']
            description = content['description']
            select_user_cmd = ("select id, name, date from Student_Project where id =%s, name=%s, date=%s")
            cursor.execute(select_user_cmd, (_id, name, _date))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT INTO Student_Project(id, name, date, description) 
                                VALUES(%s, %s, %s, %s)"""
                cursor.execute(insert_user_cmd, (_id, name, _date, description))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200
            else: 
                update_user_cmd = """update Student_Project 
                                 set name=%s, date=%s, description=%s
                                 where id=%s and name=%s and date=%s"""
                cursor.execute(update_user_cmd, (name, _date, description, _id, name, _date))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200

    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/delete/project/<int:_id>")
def deleteProject(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from Student_Project where id = %s',_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response) 

@app.route("/display/certification/<int:_id>")
def getCertifications(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select name, url, date from Student_Certification where id = %s", _id)
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchall()
            #json_data=[dict(zip(row_headers,rv))]
            #for result in rv:
             #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/set/certification", methods=['GET','POST'])
def setCertification(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            name = content['name']
            date = content['date']
            url = content['url']
            select_user_cmd = ("select id, name, date from Student_Certification where id =%s and name=%s and date=%s")
            cursor.execute(select_user_cmd, (_id, name, date))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT INTO Student_Certification(id, name, date, url) 
                                VALUES(%s, %s, %s, %s)"""
                cursor.execute(insert_user_cmd, (_id, name, date, url))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200
            else: 
                update_user_cmd = """update Student_Certification 
                                 set name=%s, date=%s, url=%s
                                 where id=%s and name=%s and date=%s"""
                cursor.execute(update_user_cmd, (name, date, url, _id, name, date))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200

    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/delete/certification/<int:id>")
def deleteCertification(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from Student_Certification where id = %s',_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response) 

@app.route("/display/skills/<int:id>")
def getSkills(id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            cursor.execute("select name from Student_Skill where id = %s", id)
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchone()
            #json_data=[dict(zip(row_headers,rv))]
            #for result in rv:
             #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/set/skills", methods=['GET','POST'])
def setSkills(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            name = content['name']
            select_user_cmd = ("select id, name from Student_Skill where id =%s and name=%s")
            cursor.execute(select_user_cmd, (_id, name))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT INTO Student_Skill(id, name) 
                                VALUES(%s, %s)"""
                cursor.execute(insert_user_cmd, (_id, name))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200
            else: 
                update_user_cmd = """update Student_Skill 
                                 set name=%s
                                 where id=%s and name=%s"""
                cursor.execute(update_user_cmd, (name, _id, name))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200

    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)



@app.route("/delete/followField/<int:_id>")
def unfollowField(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from Stud_Will_Work_Field where id = %s',_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response) 

@app.route("/set/followField", methods=['GET','POST'])
def followField(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            _id = content['uid']
            name = content['fieldId']
            select_user_cmd = ("select id, name from Stud_Will_Work_Field where id =%s and name=%s")
            cursor.execute(select_user_cmd, (_id, name))
            rv = cursor.fetchone()

            if not rv:
                insert_user_cmd = """INSERT Stud_Will_Work_Field(id, name) 
                                VALUES(%s, %s)"""
                cursor.execute(insert_user_cmd, (_id, name))
                conn.commit()
                response = jsonify(message='User added successfully.', id=cursor.lastrowid)
                #response.data = cursor.lastrowid
                response.status_code = 200
            else: 
                update_user_cmd = """update Stud_Will_Work_Field
                                 set name=%s
                                 where id=%s and name=%s"""
                cursor.execute(update_user_cmd, (name, _id, name))
                conn.commit()
                response = jsonify('User updated successfully.')
                response.status_code = 200

    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/display/fields/")
def getFields():
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            content = request.get_json()
            name = content['name']
            sort_by_factor = content['sort_by']
            if name == pymysql.NULL and sort_by_factor==pymysql.NULL:
                cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif sort_by_factor == pymysql.NULL:
                cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name having field_name =%s", name)
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif name == pymysql.NULL and sort_by_factor == "name" :
                cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name order by field_name")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif name == pymysql.NULL and sort_by_factor == "seekers" :
                cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name order by n_seekers desc")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif name == pymysql.NULL and sort_by_factor == "opp" :
                cursor.execute("select opp.id as field_id, o.required_opp_field_name as name, opp.description, count(distinct o.id) as n_opportunities, count(distinct sw.id) as n_seekers from opp_field opp inner join opportunity o on o.required_opp_field_name = opp.name inner join stud_will_work_field sw on sw.field_name = opp.name group by field_name order by n_opportunities desc")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

app.route("/display/field/")
def getField(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            content = request.get_json()
            _id = content['id']
            cursor.execute("select id, name, description from opp_field where id = %s", _id)
            #row_headers=[x[0] for x in cursor.description] #this will extract row headers
            rv = cursor.fetchone()
            #json_data=[dict(zip(row_headers,rv))]
            #for result in rv:
                #   json_data.append(dict(zip(row_headers,result)))
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()
@app.route("/set/Field", methods=['GET','POST'])
def addField():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            name = content['name']
            description = content['description']
            insert_user_cmd = """INSERT INTO opp_field(name, description) 
                                VALUES(%s, %s)"""
            cursor.execute(insert_user_cmd, (name, description))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/edit/Field", methods=['GET','POST'])
def editField():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            name = content['name']
            description = content['description']
            update_user_cmd = """update opp_field
                                 set description=%s
                                 where name=%s"""
            cursor.execute(update_user_cmd, (description, name))
            conn.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)
@app.route("/delete/Field/<int:id>")
def deleteField(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from opp_field where id = %s',_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response)
        
@app.route("/display/organizations/")
def getOrganizations():
    try:
            conn = mysql.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            content = request.get_json()
            name = content['name']
            sort_by_factor = content['sort_by']
            if name == pymysql.NULL and sort_by_factor==pymysql.NULL:
                cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif sort_by_factor == pymysql.NULL:
                cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name having org.name =%s", name)
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif name == pymysql.NULL and sort_by_factor == "name" :
                cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name order by org.name")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif name == pymysql.NULL and sort_by_factor == "mentors" :
                cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name order by n_mentor desc")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
            elif name == pymysql.NULL and sort_by_factor == "opp" :
                cursor.execute("select org.id as id, org.name as name, org.location as location, count(distinct o.id) as n_opportunities, count(distinct me.id) as n_mentor from Organization org inner join opportunity o on o.org_id = org.id inner join Alum_Associate_Opp me on me.opp_id = o.id group by org.name order by n_opportunities desc")
                #row_headers=[x[0] for x in cursor.description] #this will extract row headers
                rv = cursor.fetchall()
                #json_data=[dict(zip(row_headers,rv))]
                #for result in rv:
                 #   json_data.append(dict(zip(row_headers,result)))
                return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()

@app.route("/set/Org", methods=['GET','POST'])
def addOrganization():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            name = content['name']
            email = content['email']
            website = content['website']
            location = content['location']
            is_educational = content['is_educational']
            insert_user_cmd = """INSERT INTO organization(name, email,website,location,is_educational) 
                                VALUES(%s, %s, %s, %s, %s)"""
            cursor.execute(insert_user_cmd, (name, email,website,location,is_educational))
            conn.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            #response.data = cursor.lastrowid
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)
@app.route("/edit/Field", methods=['GET','POST'])
def editOrganization():
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            name = content['name']
            email = content['email']
            website = content['website']
            location = content['location']
            is_educational = content['is_educational']
            update_user_cmd = """update organization
                                 set email=%s, website=%s, location=%s, is_educational=%s
                                 where name=%s"""
            cursor.execute(update_user_cmd, (email, website, location, is_educational, name))
            conn.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)
@app.route("/delete/Field/<int:id>")
def deleteOrganization(_id):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute('delete from Organization where id = %s',_id)
            conn.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete user.')         
            response.status_code = 400
    finally:
            cursor.close()
            conn.close()    
            return(response)


if __name__ == "__main__":  
    app.run(debug=True)
