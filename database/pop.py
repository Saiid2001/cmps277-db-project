import json
from random import random
import mysql.connector
from mysql.connector import Error

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


try:
    connection = mysql.connector.connect(host='localhost',
                                         database='project',
                                         user='Nas',
                                         password='Sanasaida123')

    for i in range(100):
        fname = first_names[i]
        lname = last_names[i]
        email = fname + "." + lname + "@gmail.com"
        linked_in = fname + "-" + lname
        age = random() * 80 + 20
        gender = "Female"
        website = fname + "git.com"
        phone = "71775923" 
        mySql_insert_query = "INSERT INTO User VALUES ('" + fname +"','" + lname + "','" + email + "','" + linked_in + "','" + phone + "', " + str(age) + ",'" + website + "','" + gender + "')"


        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        print(cursor.rowcount, "Record inserted successfully into User table")
        cursor.close()

except mysql.connector.Error as error:
    print("Failed to insert record into User table {}".format(error))

finally:
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")


