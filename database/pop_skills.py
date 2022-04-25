from random import randint, random
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

mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT uemail FROM Student")

myresult = mycursor.fetchall()

for x in myresult:
    num = randint(1,4)
    email = x[0]
    sks = []
    for i in range(num):
        sk = randint(0,99)
        if sk in sks:
            continue
        else:
            sks.append(sk)
            mySql_insert_query = "INSERT INTO Skills VALUES ('" + skills[sk] + "','" + email + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into Skills table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

