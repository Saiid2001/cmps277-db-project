from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT uemail FROM Student")

emails = mycursor.fetchall()

mycursor.execute("SELECT id FROM Opportunity")

opportunities = mycursor.fetchall()

for em in emails:
    email = em[0]
    num = randint(1,5)
    opps = []
    for i in range(num):
        opp = randint(0, len(opportunities) - 1)
        if opp in opps:
            continue
        else:
            opps.append(opp)
            mySql_insert_query = "INSERT INTO apply VALUES ('" + email + "'," + str(opportunities[opp][0]) + ")"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into apply table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

