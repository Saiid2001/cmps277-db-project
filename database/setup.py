import sys
import subprocess
from pop_alum import pop_alum
from pop_apply import pop_apply
from pop_associate import pop_associate
from pop_benefits import pop_benefits
from pop_certs import pop_certifications
from pop_exp import pop_exp
from pop_exp_acc import pop_exp_acc
from pop_mentor import pop_mentor
from pop_op_field import pop_op_field
from pop_opps import pop_opportunities

from pop_org import pop_org
from pop_prgm_acc import pop_prgrm_acc
from pop_prgrm import pop_prgrm
from pop_projects import pop_projects
from pop_skills import pop_skills
from pop_student import pop_students
from pop_will import pop_will

# CONSTANTS
DB_NAME = "project"


print("INSTALLING REQUIREMENTS")
print("--------------------------------------")
# implement pip as a subprocess:
subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
'-r', 'requirements.txt'])

from decouple import config
from pop import pop_users


try:
    print("\nConnecting to local database")
    import mysql.connector

    connection = mysql.connector.connect(host=config('mysql_hostname'),
                                            database=config('mysql_db'),
                                            user=config('mysql_user'),
                                            password=config('mysql_password'))


    if connection.is_connected():
        print("MySQL connection opened")

    with open('Final_DB_Creation.sql', 'r') as f:
        
        for query in f.read().split(';'):
            cursor = connection.cursor()
            cursor.execute(query)
            connection.commit()
            print("Creating database ", cursor)
            cursor.close()
        
        
    pop_org(connection)
    pop_users(connection)
    pop_students(connection)
    pop_alum(connection)
    pop_op_field(connection)
    pop_skills(connection)
    pop_projects(connection)
    pop_certifications(connection)
    pop_opportunities(connection)
    pop_benefits(connection)
    pop_will(connection)
    pop_apply(connection)
    pop_exp(connection)
    pop_exp_acc(connection)
    pop_prgrm(connection)
    pop_prgrm_acc(connection)
    pop_mentor(connection)
    pop_associate(connection)

    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

except Exception as e:
    print("Connection Failed")
    raise(e)
