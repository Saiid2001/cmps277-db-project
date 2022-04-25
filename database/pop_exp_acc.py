from msilib.schema import ServiceInstall
import random
from turtle import title
import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()

mycursor.execute("Select id from Experience")

experiences = mycursor.fetchall()

titles = [
	"Cold-called 20+ potential clients on a daily basis, with a closing rate of 10% to 20%.",
	"Hit and exceeded sales KPIs by 30 for the months of October, November, and December in 2019",
	"Sent 200+ cold emails on a daily basis, managing to set up calls with 10 of the recipients",
	"Maintained a customer satisfaction rate of 95 for 2019",
	"Solved 20 - 25 tickets on a daily basis",
	"Carried out retention calls with unsatisfied customers, convincing 20 of them to keep using the software",
	"Trained and supervised 5 other cashiers over a period of 2 years at Company X.",
	"Got the employee of the month award for June, August, and December.",
	"Reached out to and made deals with new office supply providers, cutting annual supply costs by 20%.",
	"Hired, trained, and managed 15+ cleaning and maintenance staff",
	"Worked directly with the senior management, scheduling their meetings, flights, and other appointments on a daily basis",
	"Communicated with 20+ company partners and clients on a daily basis",
	"Assisted onboarding 14 employees during my time at Company X",
	"Managed an annual budget of $400,000 for a period of 7 years.",
	"Worked with a team of 3 accountants, creating financial reports for all company activities composed of 8 departments.",
	"Helped Company X stay within the budget for the past 3 years in a row",
	"Implemented and streamlined cutting-edge data management procedures, improving the operational efficiency of the company by 5%.",
	"Managed 5 different projects with a budget of over $200.000.",
	"Reduced labour and material costs by 7%.",
	"Processed 30+ customer transactions with extreme attention to detail on a daily basis",
	"Established rapport with 40+ regular customers, making sure to remember everyones names",
	"Helped onboard 3 new bank tellers, bringing them up to speed with the banks rules and policies",
	"Sourced qualified candidates utilizing various web technologies, social media, resume databases and referrals from networking events while reducing the hiring costs by 35%.",
	"Participated in community affairs to increase branch visibility and to enhance new and existing business opportunities.",
	"Provided a superior level of customer relations, promoted the sales and service culture through coaching, guidance and staff motivation.",
	"Planned, organized and executed hiring events partnering with 12 local community organizations; facilitated and delivered presentations showcasing Novorésumé career opportunities.",
	"Managed data integrity within the applicant tracking system, ensuring timely entry and visibility of recruitment activity within ATS/CRM technologies.",
	"Utilized Google Analytics and Google Tag Manager and implemented new scripts that increased performance by 25%.",
	"Converted data into actionable insights by predicting and modeling future outcomes, that increased revenue by 10 last year.",
	"Managed to reduce customer churn by 15 using collected data to perform a forecast analysis of when customers would churn.",
	"Managed 3 software projects end-to-end. Defined growth strategy, hired software and marketing team, and set goals and expectations.",
	"Established new key partnerships with Company X and Company Y, resulting in a 20 increase in annual revenue.",
	"Started a partnership program, kick-started work with 4 implementation partners in Europe.",
	"Led the digital transformation project, adopting software to help with marketing, accounting, and HR duties at Company X.",
	"Over the past 5 years, successfully completed 6 projects from start to finish, generating a total of $600,000 in revenue.",
	"Worked as a single point of contact for over 15+ clients, answering all their requests and questions in a timely manner.",
	"Revamped Company Xs social media accounts, improving user engagement by over 60 on Facebook, Twitter, and LinkedIn.",
	"Revamped the copy for the Company X website, increasing conversions by 20%.",
	"Led Facebook ad lead generation campaigns, driving 20+ leads for the sales team on a monthly basis, at a $2.7 CPC and $9 CPA.",
	"Managed a monthly ad budget of over $20,000.",
	"Maintained an ad spend ROI of 1.8 for Company Xs ad campaigns over the past 3 months.",
	"Managed to reduce Company Xs Search Ads average CPC while maintaining same conversion rate, saving them $2k in monthly ad spend.",
]

content = "The description of this achievement/accomplishement is found in my resume attached to the application. Please check it out!"

for exp in experiences:
    accs = []
    num = random.randint(1,3)
    for i in range(num):
        acc = random.choice(titles)
        if acc not in accs:
            accs.append(acc)
            mySql_insert_query = "INSERT INTO exp_accomplishments VALUES (" + str(exp[0]) + ",'" + acc + "','" + content + "')"
            cursor = mydb.cursor()
            cursor.execute(mySql_insert_query)
            mydb.commit()
            print(cursor.rowcount, "Record inserted successfully into exp_accomplishments table")
            cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

