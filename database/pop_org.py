from random import random
import mysql.connector
from mysql.connector import Error
import math

org_names = ["Eco Focus", 
    "Innovation Arch"
    ,"Strat Security"
    ,"Inspire Fitness Co"
    ,"Candor Corp"
    ,"Cogent Data"
    ,"Epic Adventure Inc"
    ,"Sanguine Skincare"
    ,"Vortex Solar"
    ,"Admire Arts"
    ,"Bravura Inc"
    ,"Bonefete Fun"
    ,"Moxie Marketing"
    ,"Zeal Wheels"
    ,"Obelus Concepts"
    ,"Quad Goals"
    ,"Erudite Learning"
    ,"Cipher Publishing"
    ,"Flux Water Gear"
    ,"Lambent Illumination"]

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

website = []
emails = []
org_locations = []
scores = []
typs = []
for org in org_names:
    lead = org.replace(" " , "-").lower()
    web = lead + ".org"
    website.append(web)
    email = "info@"+lead+".org"
    emails.append(email)
    score = random() * 10
    scores.append(score)
    loc = random() * 15
    org_locations.append(locations[math.floor(loc)])
    if (loc > 7):
        typs.append(1)
    else:
        typs.append(0)



def pop_org(connection):

    try:

        count = 0
        for i in range(20): 
            name = org_names[i]
            web = website[i]
            email = emails[i]
            score = scores[i]
            location = org_locations[i]
            work = typs[i]
            inst = not work

            mySql_insert_query = "INSERT INTO Organization VALUES ('" + web +"','" + name + "','" + email + "','" + location +  "', " + str(score) + "," + str(inst) + "," + str(work) + ")"


            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            connection.commit()
            cursor.close()
            count +=1

        print(count, "Record inserted successfully into Organization table")
            
        

    except mysql.connector.Error as error:
        print("Failed to insert record into Organization table {}".format(error))

