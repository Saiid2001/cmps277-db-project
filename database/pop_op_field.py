from random import randint, random
import mysql.connector

opp_fields = [
    "Music",
    "Nursing",
    "Oceanography",
    "Photography",
    "Psychology",
    "Statistics",
    "Urban Planning",
]

description = [
    "Music is the art of arranging sounds in time through the elements of melody, harmony, rhythm, and timbre.[1][2] It is one of the universal cultural aspects of all human societies. General definitions of music include common elements such as pitch (which governs melody and harmony), rhythm (and its associated concepts tempo, meter, and articulation), dynamics (loudness and softness), and the sonic qualities of timbre and texture (which are sometimes termed the color of a musical sound). Different styles or types of music may emphasize, de-emphasize or omit some of these elements. Music is performed with a vast range of instruments and vocal techniques ranging from singing to rapping; there are solely instrumental pieces, solely vocal pieces (such as songs without instrumental accompaniment) and pieces that combine singing and instruments. ",
    "Nursing is a profession within the health care sector focused on the care of individuals, families, and communities so they may attain, maintain, or recover optimal health and quality of life. They also take on vital roles of education, assessing situations, as support.[1] Nurses may be differentiated from other health care providers by their approach to patient care, training, and scope of practice. Nurses practice in many specialties with differing levels of prescription authority. Nurses comprise the largest component of most healthcare environments;[2][3] but there is evidence of international shortages of qualified nurses.[4] Many nurses provide care within the ordering scope of physicians, and this traditional role has shaped the public image of nurses as care providers. Nurse practitioners are nurses with a graduate degree in advanced practice nursing. They are however permitted by most jurisdictions to practice independently in a variety of settings. Since the postwar period, nurse education has undergone a process of diversification towards advanced and specialized credentials, and many of the traditional regulations and provider roles are changing.",
    "Oceanography (from the Ancient Greek ὠκεανός ocean and γράφω write), also known as oceanology, is the scientific study of the oceans. It is an important Earth science, which covers a wide range of topics, including ecosystem dynamics; ocean currents, waves, and geophysical fluid dynamics; plate tectonics and the geology of the sea floor; and fluxes of various chemical substances and physical properties within the ocean and across its boundaries. These diverse topics reflect multiple disciplines that oceanographers utilize to glean further knowledge of the world ocean, including astronomy, biology, chemistry, climatology, geography, geology, hydrology, meteorology and physics. Paleoceanography studies the history of the oceans in the geologic past. An oceanographer is a person who studies many matters concerned with oceans including marine geology, physics, chemistry and biology. ",
    "Photography is the art, application, and practice of creating durable images by recording light, either electronically by means of an image sensor, or chemically by means of a light-sensitive material such as photographic film. It is employed in many fields of science, manufacturing (e.g., photolithography), and business, as well as its more direct uses for art, film and video production, recreational purposes, hobby, and mass communication. Typically, a lens is used to focus the light reflected or emitted from objects into a real image on the light-sensitive surface inside a camera during a timed exposure. With an electronic image sensor, this produces an electrical charge at each pixel, which is electronically processed and stored in a digital image file for subsequent display or processing. The result with photographic emulsion is an invisible latent image, which is later chemically developed into a visible image, either negative or positive, depending on the purpose of the photographic material and the method of processing. A negative image on film is traditionally used to photographically create a positive image on a paper base, known as a print, either by using an enlarger or by contact printing. "
    "Psychology is the scientific study of mind and behavior. Psychology includes the study of conscious and unconscious phenomena, including feelings and thoughts. It is an academic discipline of immense scope, crossing the boundaries between the natural and social sciences. Psychologists seek an understanding of the emergent properties of brains, linking the discipline to neuroscience. As social scientists, psychologists aim to understand the behavior of individuals and groups.[1][2] Ψ (or psi) is a Greek letter which is commonly associated with the science of psychology. A professional practitioner or researcher involved in the discipline is called a psychologist. Some psychologists can also be classified as behavioral or cognitive scientists. Some psychologists attempt to understand the role of mental functions in individual and social behavior. Others explore the physiological and neurobiological processes that underlie cognitive functions and behaviors.",
    "Statistics is the discipline that concerns the collection, organization, analysis, interpretation, and presentation of data.[1][2][3] In applying statistics to a scientific, industrial, or social problem, it is conventional to begin with a statistical population or a statistical model to be studied. Populations can be diverse groups of people or objects such as all people living in a country or every atom composing a crystal. Statistics deals with every aspect of data, including the planning of data collection in terms of the design of surveys and experiments.[4] When census data cannot be collected, statisticians collect data by developing specific experiment designs and survey samples. Representative sampling assures that inferences and conclusions can reasonably extend from the sample to the population as a whole. An experimental study involves taking measurements of the system under study, manipulating the system, and then taking additional measurements using the same procedure to determine if the manipulation has modified the values of the measurements. In contrast, an observational study does not involve experimental manipulation. ",
    "Urban planning, also known as regional planning, town planning, city planning, or rural planning, is a technical and political process that is focused on the development and design of land use and the built environment, including air, water, and the infrastructure passing into and out of urban areas, such as transportation, communications, and distribution networks and their accessibility.[1] Traditionally, urban planning followed a top-down approach in master planning the physical layout of human settlements.[2] The primary concern was the public welfare,[1][2] which included considerations of efficiency, sanitation, protection and use of the environment,[1] as well as effects of the master plans on the social and economic activities.[3] Over time, urban planning has adopted a focus on the social and environmental bottom-lines that focus on planning as a tool to improve the health and well-being of people while maintaining sustainability standards. Sustainable development was added as one of the main goals of all planning endeavors in the late 20th century when the detrimental economic and the environmental impacts of the previous models of planning had become apparent.[citation needed] Similarly, in the early 21st century, Jane Jacobs writings on legal and political perspectives to emphasize the interests of residents, businesses and communities effectively influenced urban planners to take into broader consideration of resident experiences and needs while planning. ",
]

mydb = mysql.connector.connect(
  host="localhost",
  user="Nas",
  password="Sanasaida123",
  database="project"
)

mycursor = mydb.cursor()


for i in range(6):

    mySql_insert_query = "INSERT INTO Opportunity_Field VALUES ('" + opp_fields[i] + "','" + description[i] + "')"
    cursor = mydb.cursor()
    cursor.execute(mySql_insert_query)
    mydb.commit()
    print(cursor.rowcount, "Record inserted successfully into Opportunity_Field table")
    cursor.close()

if mydb.is_connected():
    mydb.close()
    print("MySQL connection is closed")

