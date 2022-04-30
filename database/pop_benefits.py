from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random, sample
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


def pop_benefits(mydb):

	mycursor = mydb.cursor()

	mycursor.execute("SELECT id FROM Opportunity")

	ids = mycursor.fetchall()

	count =0

	for id in ids:
		op_id = id[0]
		num = randint(1,6)
		bens = sample(benefits, randint(0,7))
		
		for benefit in bens:
			mySql_insert_query = "INSERT INTO benefits VALUES (" + str(op_id) + ",'" + benefit + "')"
			cursor = mydb.cursor()
			cursor.execute(mySql_insert_query)
			mydb.commit()
			cursor.close()
			count +=1

	print(count, "Record inserted successfully into benefits table")
			

