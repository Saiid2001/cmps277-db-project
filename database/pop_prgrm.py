from ast import If
from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random, choice
import mysql.connector

from faker import Faker

faker = Faker()


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


def pop_prgrm(mydb):
	mycursor = mydb.cursor()

	mycursor.execute("SELECT email FROM User")

	emails = mycursor.fetchall()

	mycursor.execute("SELECT oemail FROM Organization Where is_educational = true")

	Orgs = mycursor.fetchall()

	count = 0
	for em in emails:
		
		for i  in range(randint(0,3)):
			email = em[0]
			org = choice(Orgs)[0]
			is_complete = randint(0,1)
			major = choice(majors)
			score = randint(0,10)

			start_date = str(faker.date_between(start_date="-10y", end_date="-4y"))
			end_date = str(faker.date_between(start_date="-4y", end_date="today"))

			mySql_insert_query = "INSERT INTO Complete_program VALUES (Null,'" + org + "','" + email + "','" + start_date + "','" + end_date + "'," + str(score) + ",'" + major + "'," + str(is_complete) + ")"
			cursor = mydb.cursor()
			cursor.execute(mySql_insert_query)
			mydb.commit()
			cursor.close()
			count +=1
			
	print(count, "Record inserted successfully into Complete_program table")
			

