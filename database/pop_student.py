from random import randint

statements = [
    "Architecture is the will of an epoch translated into space.” I was 16 when I first read this quote by Mies van der Rohe, and, back then, I thought I really understood what it meant. Thinking of this quote one summer evening, as I walked around my beloved New York City, I was inspired to commit to a future in architecture. At that early stage, I cherished romantic ideals of designing grandiose buildings that would change a city; of adding my name to the list of architectural geniuses who had immortalized their vision of the world in concrete, steel, glass, and stone. It was in college that I became passionately interested in the theoretical design and engineering concepts that form the basis of architecture, while also exploring in greater detail the sociological and economic impact of architecture.",
    "My interest in the Health Economics specialization option is a testament to my conviction that health is one of the most interesting and complex determinants of social welfare. In my experiences as a traveler, researcher, and student, I understand health policy to be one of the most defining characteristics of a national identity as well as the locus of key clashes between equity and efficiency. Health economic policy is the most interesting because it juxtaposes health care, in which universality and equality are perceived as dominant principles, against the rationality and efficiency considerations of an increasingly liberal global economic reality. Graduate studies in health economic policy is the ideal corollary to my academic, personal and social background. I am most keen to explore the relationship between economic and psychological models of human behavior to hopefully advance a more holistic social sciences perspective on why people act against their own self-interest when it comes to their health.",
    "After spending four years as an Arts & Science undergraduate and earning a Minor specialization in Economics, I have developed strong analytical research skills, a capacity for truly critical thought and an appreciation for the universal relevance of economic investigation. My interest in the social determinants of health, and how these interplay with policy and economics, was the impetus for my senior undergraduate research project entitled, “Health and behavior: Advancing a microeconomic framework for changing decision-making in people with obesity.” I was fortunate to work with economists Drs. Levi and Traut, with whom I interrogated the classical and contemporary theories around human behavior and health. In my role as a research assistant, I conducted three literature reviews, one of which was used to support the work of a senior graduate student and will be published in an upcoming issue of Health Economics and the abstract was accepted for a poster presentation at the Annual Health Economics Conference in Denver CO.",
    "It is the responsibility of economics researchers to offer sustainable and feasible alternatives and recommendations to experts in all other fields regarding their most pressing challenges such as climate change and regulation of illegal trade. Further, the intermediary between economics research and the implementation of its corresponding results is the policy process. Because analytical research and writing are my most well-developed academic strengths, as evidenced by my GPA, undergraduate thesis, reference letters, and writing samples, the MA Economic Policy (Health Specialization) program is an ideal launch point for a research career in academia with branch points into policy work in the social determinants of health. Eventually, I want to complete a PhD. I want to build a focused academic practice at McMaster where I can help civil society, government and social enterprises understand and address ‘wicked problems’ at the intersection of economics and public health. The skills I aim to acquire through this graduate training are crucial to the evolution of my practice.",
    "When I was 12 years old, my sister suffered a traumatic car accident that left her with PTSD, depression, and severe anxiety. Our parents did not really understand the impact of what she was going through and as a family, we never talked about it much, though we all could witness her pain. So, through my teen years, I watched as a beloved family member struggled with her mental health. Though I did my best to support her through the worst times and assist her in getting professional help, there were still many moments when I felt powerless and clueless in the face of her suffering. This challenging experience set me on the path to pursuing clinical psychology as a career. I wanted to question, dissect, analyze, and hopefully, understand, this mysterious phenomenon that had dominated my life for so long. Through my academic study of psychology and personal experience of my sister’s PTSD, I found that I was particularly interested in clinical psychology with relation to adolescent populations.",
    "From the age of 16 to 21, I worked as a volunteer at an after-school care program for children and teens from disadvantaged backgrounds. While there, I met numerous young people, who had faced starvation, neglect, abuse, and violence, from a very young age, and who needed help to cope with the long-term effects of those early experiences. Working with these kids, helping them through events that might be unimaginable for most adults, further sharpened my interest in how trauma influences the development of generalized anxiety disorders and panic disorders, and in particular, the pre-existing conditions and underlying risk factors for suicide in adolescents with PTSD, anxiety, and depression. This is the topic I hope to continue to explore as a Master’s student in the Clinical Psychology program of your university. Thanks to my personal and first-hand experiences with the effects of trauma, I think I can bring a unique perspective to the study of long-term PTSD in adolescents.",
    "Though my core interest in clinical psychology and the effects of trauma started as deeply personal, my scholarly curiosity and intellectual proficiency led me to academic explorations of this subject from a young age. While in high school, I took up Intro to Psychology classes from my local community college and completed a Peer Youth Counselling certificate course from the Ryerson Center for Mental Health. This academic exploration confirmed my desire to study psychology in college, and my coursework through my undergrad years focused on building a broad portfolio of the key areas of psychology, including Clinical Psychology, Cognitive Psychology and Behavioral Science, Industrial Psychology, Abnormal Psychology, and more. I also took up courses in Biology, Physiology, and Neuroscience to better understand the physical pathologies of adolescent trauma. I believe this thorough grounding in the biological aspects of developmental psychopathology will help me to address the sorely needed requirement for cross-disciplinary research into effective treatment programs for trauma survivors."
]



def pop_students(connection):
    mycursor = connection.cursor()

    mycursor.execute("SELECT email FROM User")

    myresult = mycursor.fetchall()

    count = 0

    for x in myresult:

        if randint(0,1):
            email = x[0]
            stm = randint(0,6)
            statement = statements[stm]
            work = randint(0,1)
            mySql_insert_query = "INSERT INTO Student VALUES ('" + email +"','" + statement + "'," + str(work) + ")"

            cursor = connection.cursor()
            cursor.execute(mySql_insert_query)
            connection.commit()
            cursor.close()
            count +=1

    print(count, "Record inserted successfully into Student table")
            
