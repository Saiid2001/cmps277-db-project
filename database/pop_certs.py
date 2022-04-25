from calendar import month
from random import randint, random
import mysql.connector

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


mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT uemail FROM Student")

myresult = mycursor.fetchall()

for x in myresult:
    num = randint(1,4)
    email = x[0]
    crts = []
    for i in range(num):
        cert = randint(0,18)
        if cert in crts:
            continue
        else:
            crts.append(cert)
            day = randint(1,29)
            month = randint(1,12)
            year = randint(2000,2022)
            certificate = certs[cert]
            url = certificate.replace(" ", "-") + ".net/certificate/crt=" + str(cert)
            mySql_insert_query = "INSERT INTO Certifications VALUES ('" + str(year) + "-" + str(month) + "-" + str(day) + "','" + certificate + "','" + url + "','" + email + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into Certifications table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

