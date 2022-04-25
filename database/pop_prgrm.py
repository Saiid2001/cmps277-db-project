from ast import If
from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random, choice
import mysql.connector

majors = [
	"Animal Sciences",
	"Food Sciences & Technology",
	"Horticulture Operations & Management",
	"Horticulture Science",
	"Natural Resources Conservation, General",
	"Environmental Science",
	"African American Studies",
	"American Indian/Native American Studies",
	"Latino/Chicano Studies",
	"Women’s Studies",
	"Liberal Arts & General Studies*",
	"Library Science",
	"Architectural Engineering Technology",
	"Automotive Engineering Technology",
	"Civil Engineering Technology",
	"Computer Engineering Technology",
	"Construction/Building Technology",
	"Electrical, Electronics Engineering Technologies",
	"Astronomy",
	"Atmospheric Sciences & Meteorology",
	"Chemistry",
	"Geological & Earth Sciences",
	"Physics",
	"Anthropology",
	"Criminology",
	"Economics",
	"Geography",
	"History",
	"International Relations & Affairs",
	"Political Science & Government",
	"Psychology, Clinical & Counseling",
]

mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT email FROM User")

emails = mycursor.fetchall()

mycursor.execute("SELECT oemail FROM Organization Where is_educational = true")

Orgs = mycursor.fetchall()

for em in emails:
	cmp = randint(0,100)
	if cmp % 3 != 0:
		email = em[0]
		org = choice(Orgs)[0]
		is_complete = randint(0,1)
		major = choice(majors)
		score = randint(0,10)


		end_day = randint(1,29)
		end_month = randint(1,12)
		end_year = randint(2019 , 2022)
		start_day = randint(1,29)
		start_month = randint(1,12)
		start_year = randint(2010,2018)

		start_date = str(start_year) + "-" + str(start_month) + "-" + str(start_day) 
		end_date = str(end_year) + "-" + str(end_month) + "-" + str(end_day)


		mySql_insert_query = "INSERT INTO Complete_program VALUES (Null,'" + org + "','" + email + "','" + start_date + "','" + end_date + "'," + str(score) + ",'" + major + "'," + str(is_complete) + ")"
		cursor = mydb.cursor()
		cursor.execute(mySql_insert_query)
		mydb.commit()
		print(cursor.rowcount, "Record inserted successfully into Complete_program table")
		cursor.close()
        

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

