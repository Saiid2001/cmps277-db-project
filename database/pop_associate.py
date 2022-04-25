from random import randint, random
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT distinct uemail FROM Alumnus")

emails = mycursor.fetchall()

mycursor.execute("SELECT id FROM Opportunity")

Opps = mycursor.fetchall()


for em in emails:
    email = em[0]
    num = randint(1,2)
    opps = []
    for i in range(num):
        rand = randint(0, len(Opps) - 1)
        if rand in opps:
            continue
        else:
            opps.append(rand)
            id = Opps[rand][0]

            mySql_insert_query = "INSERT INTO Associate VALUES ('" + email + "'," + str(id) + ")"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into Associate table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

