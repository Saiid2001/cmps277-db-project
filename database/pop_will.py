from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random, sample
import mysql.connector



def pop_will(mydb):

    mycursor = mydb.cursor()

    mycursor.execute("SELECT uemail FROM Student")

    emails = mycursor.fetchall()

    mycursor.execute("SELECT ofname FROM Opportunity_Field")

    ofnames = mycursor.fetchall()

    count = 0

    for email in emails:

        ofs = sample(ofnames, k=randint(1,6))

        for of in ofs:
            mySql_insert_query = "INSERT INTO will_to_work VALUES ('" + email[0] + "','" + of[0] + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            cursor.close()
            count +=1
                    
    print(count, "Record inserted successfully into will_to_work table")
            


