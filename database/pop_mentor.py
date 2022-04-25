import random
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT S.uemail, A.uemail FROM Alumnus A, Student S, Opportunity O, Apply P WHERE A.uemail = O.alemail AND P.semail = S.uemail AND P.opp_id = O.id Group By S.uemail;")

mentee_mentor = mycursor.fetchall()
status = ["ongoing", "pending", "done"]


students = []
for pair in mentee_mentor:
    s_email = pair[0]
    a_email = pair[1]
    if s_email not in students and s_email != a_email:
        rating = str(random.randint(0,10))
        st = random.choice(status)

        start_day = random.randint(1,29)
        start_month = random.randint(1,12)
        start_year = random.randint(2015,2021)

        start_date = str(start_year) + "-" + str(start_month) + "-" + str(start_day) 

        mySql_insert_query = "INSERT INTO Mentor VALUES ('" + a_email + "','" + s_email + "','" + start_date  + "'," + rating + ",'" + st + "')"
        cursor = mydb.cursor()
        cursor.execute(mySql_insert_query)
        mydb.commit()
        print(cursor.rowcount, "Record inserted successfully into Mentor table")
        cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

