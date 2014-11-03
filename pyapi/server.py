from flask import Flask
from flask import jsonify
from flask import request
from flask import render_template
from flaskext.mysql import MySQL
import MySQLdb 
import MySQLdb.cursors
import json 

mysql = MySQL()

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '123'
app.config['MYSQL_DATABASE_DB'] = 'testdata'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello():
    #return 'hello world flask dssd'
    return render_template('index.html')

@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from users where username='" + username + "' and password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"

@app.route('/api/users/<user_id>', methods=['GET'])
def getUser(user_id):
    cursor = mysql.connect().cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(" SELECT * from users where id='" + user_id + "'")
    user = cursor.fetchone()
    return jsonify(user)
    
@app.route('/api/users/', methods=['GET'])
def getUsers():
    mylist = {}
    cursor = mysql.connect().cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from users")
    rows = cursor.fetchall()
    for row in rows:
        mylist[row['id']] = row
    return jsonify(mylist)



if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)