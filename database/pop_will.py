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

mycursor.execute("SELECT ofname FROM Opportunity_Field")

ofnames = mycursor.fetchall()

names = []
for ofname in ofnames:
    names.append(ofname[0])

mycursor.execute("SELECT count(*) FROM Opportunity_Field")

size = mycursor.fetchall()

for em in emails:
    email = em[0]
    num = randint(1,3)
    fields = []
    for i in range(num):
        fl = randint(0, len(names) - 1)
        if fl in fields:
            continue
        else:
            fields.append(fl)
            mySql_insert_query = "INSERT INTO will_to_work VALUES ('" + email + "','" + names[fl] + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into will_to_work table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

