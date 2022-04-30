import random
import mysql.connector

from faker import Faker

faker = Faker()



def pop_mentor(mydb):
  mycursor = mydb.cursor()

  mycursor.execute("SELECT S.uemail, A.uemail FROM Alumnus A, Student S, Opportunity O, Apply P WHERE A.uemail = O.alemail AND P.semail = S.uemail AND P.opp_id = O.id Group By S.uemail;")

  mentee_mentor = mycursor.fetchall()
  status = ["ongoing", "finished", "canceled"]


  students = []
  count = 0
  for pair in mentee_mentor:
      s_email = pair[0]
      a_email = pair[1]
      if s_email not in students and s_email != a_email:
          rating = str(random.randint(0,10))
          st = random.choice(status)

          start_date = str(faker.date_between(start_date="-10y", end_date="-4y"))

          mySql_insert_query = "INSERT INTO Mentor VALUES ('" + a_email + "','" + s_email + "','" + start_date  + "'," + rating + ",'" + st + "')"
          cursor = mydb.cursor()
          cursor.execute(mySql_insert_query)
          mydb.commit()
          cursor.close()
          count +=1

  print(count, "Record inserted successfully into Mentor table")
          

