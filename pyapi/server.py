from flask import Flask
from flask import jsonify
from flask import request
from flaskext.mysql import MySQL

mysql = MySQL()

app = Flask(__name__)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'testData'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello():
    return 'hello world flask dssd'

@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from User where Username='" + username + "' and Password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
