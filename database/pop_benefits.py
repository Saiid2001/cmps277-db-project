from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random
import mysql.connector

benefits = [
	"Flexible Schedule",	
    "Free Snacks",
	"Casual Dress Code",
	"Event Tickets",
	"Telecommuting",
	"Bring Your Pet to Work Days",
	"Paid Time Off to Volunteer",
	"Maternity and Paternity Leave",
	"New Hire Welcome Packages",
	"Movie Nights",
	"Insurance Plans. ",
	"Disability Insurance.",
	"Tuition Reimbursement.",
	"Corporate Discounts.",
	"Paid Vacation.",
	"Retirement Plans.",
	"Paid Sick Leaves.",
	"Performance Bonus.",
	"Dental Insurance",
	"Paid Holidays",
	"Vision insurance",
	"Remote work options",
	"Employee discounts",
	"PTO for volunteering",
	"Free Day-care Services",
	"Company Wide Retreats",
]

mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT id FROM Opportunity")

ids = mycursor.fetchall()

for id in ids:
    op_id = id[0]
    num = randint(1,6)
    bens = []
    for i in range(num):
        ben = randint(0,25)
        if ben in bens:
            continue
        else:
            bens.append(ben)
            mySql_insert_query = "INSERT INTO benefits VALUES (" + str(op_id) + ",'" + benefits[ben] + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into benefits table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

