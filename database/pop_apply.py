from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random, sample
import mysql.connector



def pop_apply(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT uemail FROM Student")

    emails = mycursor.fetchall()

    mycursor.execute("SELECT id FROM Opportunity")

    opportunities = mycursor.fetchall()

    count = 0
    for user in emails:
        email = user[0]
        query = "SELECT id FROM opportunity as op where opp_field in(SELECT ofname from will_to_work where semail='"+email+"')"
        mycursor.execute(query)
        opps = mycursor.fetchall()
        for opp in sample(opps, k=min(randint(1,3), len(opps))):
            opp_id = str(opp[0])
            mySql_insert_query = "INSERT INTO apply VALUES ('" + email + "'," + opp_id + ")"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            cursor.close()
            count +=1

    print(count, "Record inserted successfully into apply table")
            



