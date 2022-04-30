from random import randint
import random
import mysql.connector

skills = [
    "Sense Weather",
    "Prestidigitation",
    "Dance",
    "Climbing",
    "Masonry",
    "Navigation",
    "Wrestling",
    "Firebuilding",
    "Psychology",
    "Torture",
    "Juggle",
    "Sign language",
    "Farming",
    "Falconry",
    "Sex appeal",
    "Poison Lore",
    "Astrology",
    "Drug Lore",
    "Blathering",
    "Laundry",
    "Scapulomancy",
    "Net",
    "Law Lore",
    "Sabotage",
    "Throwing",
    "Animal Lore",
    "Herbalism",
    "Library use",
    "Contortion",
    "Bargain",
    "Undead Lore",
    "Anatomy",
    "Swim",
    "Foraging",
    "Digging",
    "Interrogation",
    "Resist Magic",
    "Pleading",
    "Explosives",
    "Pick Pocket",
    "Smuggling",
    "Improvisation",
    "Spot Trap",
    "Agriculture",
    "Stewardship",
    "Cook",
    "Urban legends",
    "Drawing",
    "Cartography",
    "Mining",
    "Antiques",
    "Investigation",
    "Alchemy",
    "Hearing",
    "Magic Door",
    "Read/Write",
    "Stalking",
    "Pottery",
    "Heal Wounds",
    "Fire Eating",
    "Fishing",
    "Window Fishing",
    "Basket-weaving",
    "Running",
    "Streetwise",
    "Clowning",
    "History",
    "Chatter",
    "Tea Leaf Reading",
    "Rope use",
    "Escape Arts",
    "Poetry",
    "Recreational activities",
    "Acting",
    "Politics",
    "Courtesan",
    "Evaluate Item",
    "Tactics",
    "Resist Poison",
    "Fast-talk",
    "Witch Lore",
    "Occult lore",
    "Cribery",
    "Medicine Lore",
    "Herb Lore",
    "Yelling",
    "Impersonation",
    "Heraldry",
    "Tracking",
    "Fashion",
    "Story Telling",
    "First Aid",
    "Performance",
    "Metallurgy",
    "Riding",
    "Deceive",
    "Surgery",
    "Diplomacy",
    "Savoir-faire",
    "Brewing",
]


def pop_skills(connection):

    mycursor = connection.cursor()

    mycursor.execute("SELECT uemail FROM Student")

    myresult = mycursor.fetchall()

    count = 0
    for x in myresult:
        email = x[0]
        sks = random.sample(skills, k=randint(0,4))
        
        for s in sks:
            mySql_insert_query = "INSERT INTO Skills VALUES ('" + s + "','" + email + "')"
            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            connection.commit()
            cursor.close()
            count +=1

    print(count, "Record inserted successfully into Skills table")
            

