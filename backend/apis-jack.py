
@app.route("/display/postedOpp/<string:email>")
def getPostedOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select o.hosting_email, o.name, org.email as org_id, org.name, org.location, a.email, u.name, u.email, count(distinct ao.email) as n_mentors, count(distinct st.email) as n_seekers from opportunity o, organization org, alumnus a, alum_associate_opp ao, stud_apply_oppr st, user u where o.org_id = org.email and o.posting_alum_email = a.email and u.email = a.email and ao.opp_id = o.email and st.opp_id = o.email and a.email = '{email}'""")
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/display/associateOpp/<string:email>")
def getAssociateOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select o.email, o.name, org.email as org_id, org.name, org.location, a.email, u.name, u.email, count(distinct ao.email) as n_mentors, count(distinct st.email) as n_seekers from opportunity o, organization org, alumnus a, alum_associate_opp ao, stud_apply_oppr st, user u where o.org_id = org.email and o.posting_alum_email = a.email and u.email = a.email and ao.opp_id = o.email and st.opp_id = o.email and ao.email = '{email}'""")         
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/display/matchedSeekerOpp/<string:email>")
def getMatchedSeekerOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select o.email, o.name, org.email as org_id, org.name, org.location, a.email, as.stud_email as seeker_email, us.name, u.name, u.email from opportunity o, organization org, alumnus a, alum_associate_opp ao, stud_apply_oppr st, alum_mentor_stud as, user u, user us where o.org_id = org.email and o.posting_alum_email = a.email and u.email = a.email and ao.opp_id = o.email and st.opp_id = o.email and as.alum_email = ao.email and as.stud_email= us.email and u.email = '{email}'""")           
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()


@app.route("/display/appliedOpp/<string:email>")
def getAppliedOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select o.email, o.name, org.email as org_id, org.name, org.location, a.email, u.name, u.email, count(distinct ao.email) as n_mentors, count(distinct st.email) as n_seekers from opportunity o, organization org, alumnus a, alum_associate_opp ao, stud_apply_oppr st, user u where o.org_id = org.email and o.posting_alum_email = a.email and u.email = a.email and ao.opp_id = o.email and st.opp_id = o.email and st.email = '{email}'""")          
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/display/matchedMentorOpp/<string:email>")
def getMatchedMentorOpportunities(email):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select o.email, o.name, org.email as org_email, org.name, org.location, a.email, as.alum_email as mentor_email, us.name as mentor_name, u.name, u.email from opportunity o, organization org, alumnus a, alum_associate_opp ao, stud_apply_oppr st, alum_mentor_stud as, user u, user us where o.org_email = org.email and o.posting_alum_email = a.email and ao.opp_id = o.email and st.opp_id = o.email and as.stud_email = st.email and as.stud_email= u.email and u.email = '{email}'""")            
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()


@app.route("/set/applyOpp", methods=['POST'])
def applyToOpportunity():
    try:
            cursor = mysql.connection.cursor()
            content = request.get_json()
            uid = get(content,"uid")
            opp_id = get(content,"oppid")
            insert_user_cmd = f"""INSERT INTO stud_apply_oppr(email, opp_id) 
                                VALUES({uid}, {opp_id})"""
            cursor.execute(insert_user_cmd)
            mysql.connection.commit()
            response = jsonify(
                    message='User added successfully.'), 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            return(response)


@app.route("/delete/users/<string:email>/opp/<int:opp_id>", methods= ["DELETE"])
def cancelApplytoOpportunity(email, opp_id):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""delete from stud_apply_oppr where email = '{email}' and opp_id = '{opp_id}'""")
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

@app.route("/display/users/<string:email>/relationOpp/<int:opp_id>/rel/<string:rel>")
def getOpportunityRelation(email,opp_id):
    try:
            cursor = mysql.connection.cursor()
            content = request.get_json()
            rel = get(content, "rel")
            if rel == "associated":
                cursor.execute(f"""select ao.email, o.email from alum_associate_opp ao, opportunity o where ao.opp_id = o.email""")
                rv = cursor.fetchall()
                return jsonify(rv), 200
            elif rel == "matchedMentor":
                cursor.execute(f"""select as.alum_email, o.email from alum_associate_opp ao, alum_mentor_stud as , opportunity o where ao.opp_id = o.email and ao.email = as.alum_email and as.alum_email = '{email}'""")
                rv = cursor.fetchall()
                return jsonify(rv), 200
            elif rel =="matchedSeeker":
                cursor.execute(f"""select o.email from stud_apply_oppr st , opportunity o where st.opp_id = o.email and st.email = '{email}'""")
                rv = cursor.fetchall(), 200
                return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/display/oppBenefits/<string:email>")
def getOpportunityBenefits(email):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select o.email, b.content from opportunity o, opp_comp_benefits b where o.opp_id = '{email}'""")           
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/set/oppBenefits/<int:opp_id>", methods=['GET','POST'])
def addOpportunityBenefits(opp_id):
    try:
            cursor = mysql.connection.cursor()
            content = request.get_json()
            benefit = get(content, "benefit")
            insert_user_cmd = f"""INSERT INTO opp_comp_benefits(org_email, content) 
                                VALUES('{opp_id}', '{benefit}')"""
            cursor.execute(insert_user_cmd)
            mysql.connection.commit()
            response = jsonify(message='User added successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add user.')         
            response.status_code = 400 
    finally:
            cursor.close()
            return(response)

@app.route("/edit/opportunity/<int:opp_id>/Benefit/benefit_id", methods=['GET','POST'])
def editOpportunityBenefits(opp_id, benefit_id):
    try:
            cursor = mysql.connect.cursor()
            content = request.get_json()
            benefit = get(content, "benefit")
            content= content['benefit']
            update_user_cmd = f"""update opp_comp_benefits
                                 set content='{benefit}'
                                 where id='{benefit_id}' and oppid= '{opp_id}'"""
            cursor.execute(update_user_cmd)
            mysql.connect.commit()
            response = jsonify('User updated successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add opp benefit.')         
            response.status_code = 400 
    finally:
            cursor.close()
            return(response)

@app.route("/delete/opportunity/<int:opp_id>/Benefit/benefit_id")
def deleteOpportunityBenefit(opp_id,benefit_id):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""delete from opp_comp_benefits where id = '{benefit_id}' and oppid = '{opp_id}'""")
            mysql.connection.commit()
            response = jsonify('User deleted successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to delete opp benefit.')         
            response.status_code = 400
    finally:
            cursor.close() 
            return(response)

@app.route("/display/associate/<string:email>/opportunity/<int:opp_id>")
def associateOpportunity(email,opp_id):
    try:
            cursor = mysql.connect.cursor()
            cursor.execute(f"""select email, opp_id from alum_associate_opp where email = '{email}' and opp_id = '{opp_id}'""")            
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/set/match/opp/<int:opp_id>/mentor/<string:mentor_email>/seeker/<string:seeker_email>", methods=['GET','POST'])
def matchMentoring(mentor_email, seeker_email, opp_id):
    try:
            cursor = mysql.connection.cursor()
            insert_user_cmd = f"""INSERT INTO alum_associate_opp(email, opp_id) 
                                VALUES('{seeker_email}', '{opp_id}') and insert into stud_apply_oppr(email, opp_id) 
                                VALUES('{mentor_email}','{opp_id}')"""
            cursor.execute(insert_user_cmd)
            mysql.connection.commit()
            response = jsonify(message='User added successfully.', id=cursor.lastrowid)
            update_user_cmd = f"""update alum_mentor_stud
                                 set status="ongoing"
                                 where alum_email = '{mentor_email}' and stud_email ='{seeker_email}'"""
            cursor.execute(update_user_cmd)
            mysql.connection.commit()
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add match.')         
            response.status_code = 400 
    finally:
            cursor.close()
            return(response)

@app.route("/delete/mentoringOpp/<int:opp_id>/mentor/<string:mentor_email>/seeker/<string:seeker_email>", methods=['GET','POST'])
def finishMentoring(opp_id, mentor_email, seeker_email):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            rating = get(content, "rating")
            delete_user_cmd = f"""delete from stud_apply_oppr s where s.email = '{seeker_email}' and s.opp_id = '{opp_id}'"""
            cursor.execute(delete_user_cmd)
            update_user_cmd = f"""update alum_mentor_stud
                                 set rating='{rating}', status="done"
                                 where alum_email='{mentor_email}' and stud_email='{seeker_email}'"""
            cursor.execute(update_user_cmd)
            conn.commit()
            response = jsonify('Updated successfully.')
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to do task.')         
            response.status_code = 400 
    finally:
            cursor.close()
            conn.close()
            return(response)

@app.route("/set/message/<string:email>", methods=['GET','POST'])
def sendMessage(email):
    try:
            cursor = mysql.connect.cursor()
            content = request.get_json()
            other_id = get(content,"other_id")
            message = get(content,"message")
            insert_user_cmd = f"""INSERT INTO user_messages(sender_id, receiver_id, content) 
                                VALUES('{email}', '{other_id}', '{message}')"""
            cursor.execute(insert_user_cmd)
            mysql.connect.commit()
            response = jsonify(message='Message added successfully.', id=cursor.lastrowid)
            response.status_code = 200
    except Exception as e:
            print(e)
            response = jsonify('Failed to add message.')         
            response.status_code = 400 
    finally:
            cursor.close()
            return(response)

@app.route("/display/messageSender/<string:email>/Receiver/<string:other_id>")
def getMessages(email, other_id):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select message from user_messages where sender_email = '{email}' and receiver_email = '{other_id}'""")
            rv = cursor.fetchall()
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()


@app.route("/display/users")
def getUsers():
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select name, email from user""")
            rv = cursor.fetchall()
            return jsonify(rv),200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/display/mentors/")
def getMentors():
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select u.name, a.alum_email from alum_mentor_stud a, user u where a.alum_email=u.email""")
            rv = cursor.fetchall()
            return jsonify(rv)
    except Exception as e:
            print(e)
    finally:  
            cursor.close()


@app.route("/display/seekersOpp/<int:opp_id>")
def getSeekers(opp_id):
    try:
            cursor = mysql.connection.cursor()
            cursor.execute(f"""select o.opp_id, a.email from stud_apply_oppr s, opportunity o, alum_associate_opp a where a.opp_id = o.opp_id and s.opp_id = o.opp_id and o.opp_id='{opp_id}'""")
            rv = cursor.fetchall()
            return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()

@app.route("/display/mentoringMentors/<string:email>")
def getMentoringmentors(email):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            opp_id = get(content, "opp_id")
            if opp_id == NULL: 
                cursor.execute(f"""select a.alum_email, u.name from alum_mentor_stud a, user u where a.alum_email = u.email and a.stud_email = '{email}'""")
                rv = cursor.fetchall()
                return jsonify(rv), 200
            else:
                cursor.execute(f"""select a.email, u.name from stud_apply_oppr s, opportunity o, alum_associate_opp a, user u where a.opp_id = o.opp_id and s.opp_id = o.opp_id and u.email = a.email and s.email='{email}' and opp_id='{opp_id}'""")            
                rv = cursor.fetchall()
                return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()


@app.route("/display/mentoredSeekers/")
def getMentoredSeekers(email):
    try:
            conn = mysql.connect()
            cursor = conn.cursor()
            content = request.get_json()
            opp_id = get(content,"opp_id")
            if opp_id == pymysql.NULL: 
                cursor.execute(f"""select a.stud_email, u.name from alum_mentor_stud a, user u where a.stud_email = u.email and a.alum_email = '{email}'""")
                rv = cursor.fetchall()
                return jsonify(rv), 200
            else:
                cursor.execute(f"""select s.email, u.name from stud_apply_oppr s, opportunity o, alum_associate_opp a, user u where a.opp_id = o.opp_id and s.opp_id = o.opp_id and u.email = s.email and a.email='{email}' and opp_id='{opp_id}'""")                
                rv = cursor.fetchall()
                return jsonify(rv), 200
    except Exception as e:
            print(e)
    finally:  
            cursor.close()
            conn.close()