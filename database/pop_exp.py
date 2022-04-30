from calendar import month
from msilib.schema import ServiceInstall
from random import randint, random, sample
import mysql.connector

from faker import Faker

faker = Faker()

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


def pop_exp(mydb):
    mycursor = mydb.cursor()

    mycursor.execute("SELECT uemail FROM Alumnus")

    emails = mycursor.fetchall()

    mycursor.execute("SELECT oemail FROM Organization")

    Orgs = mycursor.fetchall()

    count = 0
    
    for em in emails:
        email = em[0]
        num = randint(1,3)
        orgs = sample(Orgs, k=num)

        for org in orgs:
            pos = positions[randint(0, len(positions) - 1)]

            start_date = str(faker.date_between(start_date="-10y", end_date="-4y"))
            end_date = str(faker.date_between(start_date="-4y", end_date="today"))

            mySql_insert_query = "INSERT INTO Experience VALUES (Null,'" + pos + "','" + start_date + "','" + end_date + "','" + email + "','" + org[0] + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            cursor.close()
            count +=1

    print(count, "Record inserted successfully into Experience table")
           
