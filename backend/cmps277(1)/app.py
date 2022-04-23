from flask import Flask, render_template, request, redirect,jsonify
from flaskext.mysql import MySQL
from datetime import date
import json

app = Flask(__name__)

app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'MyNewPass'
app.config['MYSQL_DATABASE_DB'] = 'flaskapp'

mysql = MySQL()
mysql.init_app(app)

#json trial
@app.route('/date')
def get_current_date():
    return {"Date": date.today()}




@app.route("/", methods=['GET','POST'])
def index():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM users2")
    users = cur.fetchall()
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur.execute("INSERT INTO users2(name, email) VALUES(%s, %s) ", (name, email))
        mysql.get_db().commit()
        cur.close()
        return redirect('/')
    return render_template('index.html', users=users)

@app.route("/display")
def display():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM users2")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(json_data)

    #if result > 0:
        #users = cur.fetchall()
        #cur.close()
        #return {"users": users}
        #return render_template('users.html',users=users)

@app.route("/delete/<int:id>")
def delete(id):
    cur = mysql.get_db().cursor()
    cur.execute("DELETE FROM users2 WHERE id=%s", (id,))
    mysql.get_db().commit()
    cur.execute("SELECT * FROM users2")
    row_headers=[x[0] for x in cur.description] #this will extract row headers
    rv = cur.fetchall()
    json_data=[]
    for result in rv:
        json_data.append(dict(zip(row_headers,result)))
    return jsonify(message="success")
    return jsonify(json_data)
    
    #mysql.get_db().commit()
    #cur.execute("SELECT * FROM users2")
    #users=cur.fetchall()
    #cur.close()
    #return {"users":users}
    #return

@app.route("/update/<int:id>", methods=['GET','POST'])
def update(id):
    cur = mysql.get_db().cursor()
    #cur.execute("SELECT * FROM users2 WHERE id = %s", (id,))
    #user = cur.fetchall()
    if request.method == 'POST':
        userDetails = request.form
        name = userDetails['name']
        email = userDetails['email']
        cur.execute("UPDATE users2 SET name = %s, email = %s WHERE id = %s", (name,email,id))
        cur.execute("SELECT * FROM users2")
        row_headers=[x[0] for x in cur.description] #this will extract row headers
        rv = cur.fetchall()
        json_data=[]
        for result in rv:
            json_data.append(dict(zip(row_headers,result)))
        return jsonify(json_data)

if __name__ == "__main__":  
    app.run(debug=True)