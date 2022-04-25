from calendar import month
from random import randint, random
import mysql.connector

locations = ["Moldova"
,"Jordan"
,"Thailand"
,"Algeria"
,"Cuba"
,"Sao Tome and Principe"
,"Croatia"
,"Curacao"
,"Chile"
,"Wales"
,"Netherlands"
,"Panama"
,"Afghanistan"
,"Guam"
,"Uzbekistan"]


opps = [
	"Australia Awards Scholarships",
	"ARES Scholarships in Belgium for Developing Countries",
	"Zurich One Young World Scholarships",
	"DAAD Scholarships for Postgraduate Studies in Architecture",
	"UNESCO/ISEDC Co-Sponsored Fellowships Programme",
	"Nutrition in Emergencies Scholarships at University of Westminster",
	"Caux Scholars Program in Switzerland",
	"2020 Fortis Fellowship",
	"VLIR-UOS ITP Scholarships for Sustainable Development and Human Rights Law Postgraduate Programme",
	"Talent for Governance Training Scholarships for Developing Countries)",
	"Endeavour Vocational Education and Training (VET) Leadership Award",
	"Endeavour Executive Fellowships",
	"Netherlands Fellowship Program for Short Courses",
	"Chinese Government Scholarships-Bilateral Program",
	"MENA Scholarship Programme (MSP) for Professionals",
	"UNITAR United Nations Volunteers Tuition-Fees Discounts",
	"UNITAR Outstanding Peacebuilder",
	"UNITAR Least Developed Countries",
	"Japanese Government Scholarships",
]

description = "This opportunity offers a lot for its beneficiaries including .... and .... and ..... It also encourages all students and alumni to connect and form a special network that will help expand the effects of this opportunity on the whole world and guarantee its continuity for years to come."

comp_types = ["Paid" , "Reimbursed", "Partial"]

mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT uemail FROM Alumnus")

Aemails = mycursor.fetchall()

mycursor.execute("SELECT oemail FROM Organization")

Oemails = mycursor.fetchall()

mycursor.execute("SELECT ofname FROM Opportunity_Field")

OFnames = mycursor.fetchall()

for opportunity in opps:
    alum = Aemails[randint(0, len(Aemails) - 1)][0]
    org = Oemails[randint(0, len(Oemails) - 1)][0]
    of = OFnames[randint(0, len(OFnames) - 1)][0]
    rl = randint(0,14)
    location = locations[rl]

    comptype = comp_types[randint(0,2)]
    compamount = randint(1000,200000)

    app_dead_month = randint(1,8)
    end_month = randint(1,12)
    end_year = randint(2026 , 2030)
    start_day = randint(1,29)
    start_month = randint(10,12)
    year = randint(2022,2025)

    deadline = str(year) + "-" + str(app_dead_month) + "-" + str(start_day) 
    start_date = str(year) + "-" + str(start_month) + "-" + str(start_day) 
    end_date = str(end_year) + "-" + str(end_month) + "-" + str(start_day)

    portal = opportunity.replace("in", "")
    portal = opportunity.replace("at", "")
    portal = "opportunities.net/" + portal.replace(" " , "-")
    mySql_insert_query = "INSERT INTO Opportunity VALUES (NULL,'" + org + "','" + opportunity + "','" + location + "','" + start_date + "','" + end_date + "','" + portal + "'," + str(compamount) + ",'" + comptype + "','" + description + "','" + deadline + "','" + of + "','" + alum + "')"
    cursor = mydb.cursor()
    cursor.execute(mySql_insert_query)
    mydb.commit()
    print(cursor.rowcount, "Record inserted successfully into Opportunity table")
    cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

