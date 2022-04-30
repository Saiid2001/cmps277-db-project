from calendar import month
from random import randint, random, sample
from unicodedata import name
import mysql.connector


from faker import Faker

faker = Faker()


names = [
	"Future Values",
	"Sleepium",
	"Gadgets Lab",
	"Future Inc",
	"Prime Seven",
	"Golden Bulls",
	"Linkage",
	"Severe",
	"Colossus",
	"Celestial Interface",
	"Discovery of Era",
	"Panthers Hive",
	"Cold Fusion",
	"Kodiak",
	"Yosaku",
    "GoBee",
]

descriptions = [
    "The Futal Values Method is a unique approach to teaching you about yourself and the world--by looking at your life as a whole, and not in chunks. By understanding the Future Values, you will understand what you are most valuable, and this will allow you to maximize your potential to create positive change for the world around you. Future Values is a great tool for anyone who is interested in self development, personal development, and/or life-changing insights",
    "What if your bed could make you smarter, happier, more productive and less stressed? The Real Sleeping made it possible by combining four natural calming practices: breathing, deep restful sleep, practices that have been proven to boost happiness, and the power of positive attitude. By engaging the revolutionary practice of sleep meditation, the extremely calming vibrations are designed to help you sleep better and enjoy the positive effects for life. Just like being rested, the Sleepium will help you wake up more fully, feel more positive",
    "WiFi connected gadgets galore. • Get your morning started 30 minutes earlier with a video alarm clock that wakes you up with a personal video. • Wake up in style with LED light-up toasters that instantly toast your bread in one simple press. • Widen your horizons with an outdoor thermometer that lets you see the temperature in your backyard. • Keep the house cool with a fridge and freezer magnets that glide on top of your fridge. • Streamline the cooking process with a mini ju",
    "Future Inc is the perfect product for original decor while giving your house a futuristic feel. Sleek and sturdy, these LED lights range from colorful, gooey, and shiny designs. With your choice of a rotating, swerving, or straight up waving motion, these lights really are the future of lighting. Ideal for your pool and patio, these lights will make sure you feel every shape and every motion for a wonderful summer and relaxing evening.",
    "Seven is the newest alcoholic drink on the market, a cocktail that replicates the feeling of imbibing alcohol, without drinking alcohol. Seven is a great way to savor a cocktail, enjoy the flavors of fruit, and help your body maintain a good balance and soberness, while also giving the eager alcohol-free non-drinker a unique experience.",
    "Sow the seeds of your dreams, and let the golden bulls grow. Golden Bulls™ are seeds specially selected for high yields of astonishing bulls, bearing a solid gold aura. Soon after sprouting, these beautiful, golden-hued plants will have your garden buzzing with bees and butterflies, and your own Shangri Las.",
    "Forget finding that one person on LinkedIn who matches your skill set. Linkage is optimized for the people you read about in news articles, articles, podcasts, and blogs. And, it’s more likely to be right than a simple search using their name. Linkage’s AI-powered matching engine continuously learns and adapts to the changing needs of the modern workforce and can be configured to look for the skills you’re looking for, plus once again, those articles,",
    "Align your plan with hope—Severe. Severe is a platform dedicated to helping to build a community of doctors, nurses, hospitals and clinics. We are working with our partners to open up an online platform where communities can access the best medical care available. What started out as a need to support medical care concepts, has turned into a passion to find doctors and bring an efficient medical experience to the table with this platform.",
    "In a world where the content is divided between the good and the objectionable, the two are not what they seem. How do we separate the good from the bad? In this definitive story of the conflict between freedom of thought and free speech, Magma becomes the key to understanding this concept and a line in the sand between freedom and censorship.",
    "Give your apps, games, interfaces and websites the best design they deserve with a professional interface, that takes less than 1 minute to customize.",
    "Explore different planets and galaxies using this digital equipment that is in line with your VR headset. Start with a casual journey as you get to explore different planets and stars, but slowly get immersed in space as you slowly make your way to different galaxies. You can turn in into a dynamic and competitive race as you watch the Leaderboard and compare your performance to others. Get on it and start exploring the beautiful world of the outer space today!",
    "You know the drill, you always find them in the last place you look. Enter these two ravenous, hard-working and royalty-worthy scavengers: the panthers, who want the honey but put up (with the) fight, and the bee colony, who surely want the panther meat, but their queen will have none of it. The game is fast-paced and simple to learn and play with infinite possibilities for victory, evolution and extinction. This game is best enjoyed with friends",
    "It’s like magic, it’s science, it’s fantastic! We provide you with detailed instructions on over 15 types of chemical reactions, both old and new. Collect and observe a variety of raw materials, old and new. Take part in our exciting experiments and create chemical reactions in many forms - fizzles, explosions, explosions, coloring, boiling, astro turf, smoke, and lots more!",
    "Dance Dance Revolution is a phenomenon that has taken dance to a whole new level of crazy popularity. For those of you who don’t know what DDR is, you’ve been missing out on an amazing (and sometimes frustrating) time with your friends and family. These days, you have so many options when it comes to DDR. With the Kodiak DDR, you get the best of the best. The build is absolutely beautiful, the interface is realistic, and the music is updated!",
    "Yamaha won just about every motorcycle at the electric motor competitions in Beijing, but there was a new player on the block-Yosaku. Targeting electric motor sports from a young age, he quickly became one of the best rider in the nation. His speed and his touch distinguished him from other athletes, who often rely on pure strength, for example, to win a race. Yet there was an unexpected phenomenon when Yosaku was given a new electric motor that he was completely unfamiliar with.",
    "GoBee provides the perfect solution for beehives enthusiasts. With GoBee, you can now view your bees around the clock, via video feed, without having to head outdoors. Co-founders, Abe and Alan, are passionate beekeepers and founders of BeeHive Technologies and they designed this tool to monitor the safety of a beehive and to ensure that there are no pests, diseases or drama on a beekeeper’s behalf. GoBee is solar powered",
]


def pop_projects(connection):

        mycursor = connection.cursor()

        mycursor.execute("SELECT uemail FROM Student")

        myresult = mycursor.fetchall()

        count = 0

        for x in myresult:
            num = randint(1,2)
            email = x[0]
            n_prj = randint(1,4)
            prjs_names = sample(names, k=n_prj)
            prjs_desc = sample(descriptions, k=n_prj)
            
            for name, description in zip(prjs_names, prjs_desc):
                date = str(faker.date_between(start_date="-3y", end_date="today"))
                mySql_insert_query = "INSERT INTO Projects VALUES ('" + date + "','" + name + "','" + description + "','" + email + "')"
                cursor = connection.cursor()
                cursor.execute(mySql_insert_query)
                connection.commit()
                cursor.close()
                count +=1

        print(count, "Record inserted successfully into Projects table")
                
