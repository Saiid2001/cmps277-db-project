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

mycursor.execute("SELECT email FROM User")

myresult = mycursor.fetchall()

mycursor.execute("SELECT oemail FROM Organization")

org = mycursor.fetchall()

org_emails = []

for em in org:
    org_emails.append(em[0])

for x in myresult:
    random = randint(0,100)
    if(random % 3 != 0):
        continue
    email = x[0]
    score = randint(0,10)
    position = randint(0,50)
    org = randint(0,14)
    mySql_insert_query = "INSERT INTO Alumnus VALUES ('" + email +"'," + str(score) + ",'" + positions[position] + "','" + org_emails[org] + "')"

    cursor = mydb.cursor()
    cursor.execute(mySql_insert_query)
    mydb.commit()
    print(cursor.rowcount, "Record inserted successfully into Alumnus table")
    cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

