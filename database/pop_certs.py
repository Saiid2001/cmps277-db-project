from calendar import month
from random import randint, random, sample
import mysql.connector

from faker import Faker

faker = Faker()

certs = [
	"Certified Business Analysis Professional (CBAP)",
	"APICS Certified Supply Chain Professional (CSCP)",
	"Certified Information Security Manager (CISM)",
	"Certified Information Systems Security Professional (CISSP)",
	"Certified Patient Care Technician (CPCT)",
	"Certified Clinical Medical Assistant (CCMA)",
	"Certified Commercial Investment Member (CCIM)",
	"Certified Legal Manager (CLM)",
	"Certified Business Economist (CBE)",
	"Certified Economic Developer (CED)",
	"First Aid Certification",
	"Notary Public Certification",
	"Certification in Full Stack Web Development",
	"Certification in Algorithms & Data Structures",
	"Coding Boot Camp",
	"Certified Pediatric Nurse (CPN)",
	"Certified Public Accountant (CPA)",
	"Certified ScrumMaster (CSM)",
	"Professional Educator License (PEL)",
]


def pop_certifications(connection):
	
	mycursor = connection.cursor()
	
	mycursor.execute("SELECT uemail FROM Student")
	
	myresult = mycursor.fetchall()
	count = 0
	
	for x in myresult:
		num = randint(1,4)
		email = x[0]
		crts = sample(certs, k=randint(0,4))
		
		for certificate in crts:
			
			date = str(faker.date_between(start_date="-4y", end_date="today"))
			url = certificate.replace(" ", "-") + ".net/certificate/crt=" + str(randint(10000, 20000))
			mySql_insert_query = "INSERT INTO Certifications VALUES ('"+date + "','" + certificate + "','" + url + "','" + email + "')"
			cursor = connection.cursor()
			cursor.execute(mySql_insert_query)
			connection.commit()
			cursor.close()
			count +=1
			
	print(count, "Record inserted successfully into Certifications table")

