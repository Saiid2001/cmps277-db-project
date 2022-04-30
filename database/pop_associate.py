from random import randint, random, sample
import mysql.connector



def pop_associate(mydb):

    mycursor = mydb.cursor()

    mycursor.execute("SELECT distinct uemail FROM Alumnus")

    emails = mycursor.fetchall()

    mycursor.execute("SELECT id FROM Opportunity")

    Opps = mycursor.fetchall()

    count =0 
    
    for em in emails:
        email = em[0]
        num = randint(1,2)
        opps = sample(Opps, k=num)

        for opp in opps:

            mySql_insert_query = "INSERT INTO Associate VALUES ('" + email + "'," + str(opp[0]) + ")"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            cursor.close()
            count+=1
    
    print(count, "Record inserted successfully into Associate table")
            