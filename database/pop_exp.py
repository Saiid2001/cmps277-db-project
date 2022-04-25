from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random
import mysql.connector

positions = [
    "Accountant",
    "Bus Driver",
    "Carpenter",
    "Cashier",
    "Chef",
    "Computer Hardware Engineer",
    "Computer Programmer",
    "Computer Support Specialist",
    "Computer Systems Administrator",
    "Computer Systems Analyst",
    "Construction Manager",
    "Cost Estimator",
    "Court Reporter",
    "Customer Service Representative",
    "Dancer",
    "Database administrator",
    "Dental Hygienist",
    "Dentist",
    "Designer",
    "Desktop publisher",
    "Diagnostic Medical Sonographer",
    "Drafter",
    "Economist",
    "Editor",
    "Educator",
    "Electrical Engineer",
    "Electrician",
    "Elementary School Teacher",
    "Environmental scientist",
    "Epidemiologist",
    "Event Planner",
    "Executive Assistant",
    "Farmer",
    "Financial Advisor",
    "Firefighter",
    "Fitness Trainer",
    "Hairdresser",
    "High School Teacher",
    "Historian",
    "Housekeeper",
    "HR Specialist",
    "Human Resources Assistant",
    "Insurance Agent",
    "Interpreter & Translator",
    "IT Manager",
    "Janitor",
    "Judge",
    "Landscape Architect",
    "Landscaper & Groundskeeper",
    "Lawyer",
    "Librarian",
    "Loan Officer",
    "Logistician",
    "Maintenance & Repair Worker",
    "Market Research Analyst",
    "Marketing Manager",
    "Marriage & Family Therapist",
    "Mason",
    "Massage Therapist",
    "Mathematician",
    "Mechanical Engineer",
    "Physical Therapist",
    "Physician",
    "Physicist",
    "Plumber",
    "Police Officer",
    "Preschool Teacher"
]

mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT uemail FROM Alumnus")

emails = mycursor.fetchall()

mycursor.execute("SELECT oemail FROM Organization")

Orgs = mycursor.fetchall()

for em in emails:
    email = em[0]
    num = randint(1,3)
    orgs = []
    for i in range(num):
        org = randint(0, len(Orgs) - 1)
        if org in orgs:
            continue
        else:
            orgs.append(org)
            pos = positions[randint(0, len(positions) - 1)]

            end_day = randint(1,29)
            end_month = randint(1,12)
            end_year = randint(2018 , 2022)
            start_day = randint(1,29)
            start_month = randint(1,12)
            start_year = randint(2010,2018)

            start_date = str(start_year) + "-" + str(start_month) + "-" + str(start_day) 
            end_date = str(end_year) + "-" + str(end_month) + "-" + str(end_day)

            mySql_insert_query = "INSERT INTO Experience VALUES (Null,'" + pos + "','" + start_date + "','" + end_date + "','" + email + "','" + Orgs[org][0] + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into Experience table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

