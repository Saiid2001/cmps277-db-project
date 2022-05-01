import json
from random import randint, random
import mysql.connector
from mysql.connector import Error
from datetime import datetime
from faker import Faker

faker = Faker() 

# Opening JSON file
f = open('first_names.json')
c = open('second_names.json')

# returns JSON object as
# a dictionary
data = json.load(f)
data2 = json.load(c)
# Iterating through the json
# list
first_names = []
for i in data['second']:
    first_names.append(i)

last_names = []
for i in data2['first']:
    last_names.append(i)

# Closing file
f.close()
c.close()


def pop_users(connection):

    try:
        count = 0
        for i in range(100):
            fname = first_names[i]
            lname = last_names[i]
            email = fname + "." + lname + "@gmail.com"
            email = email.lower()
            linked_in = fname + "-" + lname
            dob = faker.date_between(start_date="-30y", end_date="-18y")
            gender = "Male" if randint(0,1)==1 else "Female"
            website = fname + "git.com"
            phone = "71775923" 
            mySql_insert_query = "INSERT INTO User VALUES ('" + fname +"','" + lname + "','" + email + "', sha1('"+str(randint(1000,2000)) +"'),'"+ linked_in + "','" + phone + "', '" + str(dob) + "','" + website + "','" + gender + "')"
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            connection.commit()
            cursor.close()
            count +=1

        print(count, "Record inserted successfully into User table")
            

    except mysql.connector.Error as error:
        print("Failed to insert record into User table {}".format(error))


