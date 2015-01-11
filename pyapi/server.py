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
    return render_template('index.html')

@app.route("/Authenticate")
def Authenticate():
    username = request.args.get('UserName')
    password = request.args.get('Password')
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from users WHERE username='" + username + "' and password='" + password + "'")
    data = cursor.fetchone()
    if data is None:
     return "Username or Password is wrong"
    else:
     return "Logged in successfully"

@app.route('/api/users/<user_id>', methods=['GET'])
def getUser(user_id):
    cursor = mysql.connect().cursor(MySQLdb.cursors.DictCursor)
    query1 = "SELECT * from users WHERE id='" + user_id + "'"
    query2 = "SELECT id from posts WHERE creator_id='" + user_id + "'"
    # querytest = "SELECT * from users u INNER JOIN posts p on u.id = p.creator_id WHERE u.id = '" + user_id + "'"
    # cursor.execute(" SELECT * from users WHERE id='" + user_id + "'")
    cursor.execute(query1)
    user = cursor.fetchone()
    cursor.execute(query2)
    userPosts = cursor.fetchall()
    postsList = ()
    for post in userPosts:
        postsList = postsList + (post['id'],)
    user['posts'] = postsList
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

@app.route('/api/users/', methods=['POST'])
def insertUser():
    data = {}
    data["username"] = request.form['username']
    data["password"] = request.form['password']
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    query = "INSERT INTO users(username, password)" +\
        "VALUES ('%s', '%s')"
    cursor.execute(query % (data["username"], data["password"]))
    conn.commit()
    return jsonify(data)

@app.route('/api/users/<user_id>', methods=['DELETE'])
def removeUser(user_id):
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM users WHERE id='" + user_id + "'")
    conn.commit()
    return "User " + user_id + " has been deleted successfully"

@app.route('/api/users/<user_id>', methods=['PUT'])
def updateUser(user_id):
    data = {}
    data["username"] = request.form['username']
    data["password"] = request.form['password']
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    query = " UPDATE users SET username='%s', password='%s' WHERE id='" + user_id + "'"
    cursor.execute(query % (data["username"], data["password"]))
    conn.commit()
    return jsonify(data)


# POSTS
@app.route('/api/posts/<post_id>', methods=['GET'])
def getPost(post_id):
    cursor = mysql.connect().cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(" SELECT * from posts WHERE id='" + post_id + "'")
    post = cursor.fetchone()
    return jsonify(post)
    
@app.route('/api/posts/', methods=['GET'])
def getPosts():
    mylist = {}
    cursor = mysql.connect().cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from posts")
    rows = cursor.fetchall()
    for row in rows:
        mylist[row['id']] = row
    return jsonify(mylist)

# @app.route('/api/posts/<user_id>', methods=['GET'])
# def getUserPost(user_id):
#     cursor = mysql.connect().cursor(MySQLdb.cursors.DictCursor)
#     cursor.execute(" SELECT * from posts WHERE creator_id='" + user_id + "'")
#     post = cursor.fetchone()
#     return jsonify(post)

@app.route('/api/posts/', methods=['POST'])
def insertPost():
    data = {}
    data["title"] = request.form['title']
    data["text"] = request.form['text']
    data["creator_id"] = request.form['creator_id']
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    query = "INSERT INTO posts(title, text, creator_id)" +\
        "VALUES ('%s', '%s', '%s')"
    cursor.execute(query % (data["title"], data["text"], data["creator_id"]))
    conn.commit()
    return jsonify(data)

@app.route('/api/posts/<post_id>', methods=['DELETE'])
def removePost(post_id):
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("DELETE FROM posts WHERE id='" + post_id + "'")
    conn.commit()
    return "Post " + post_id + " has been deleted successfully"

@app.route('/api/posts/<post_id>', methods=['PUT'])
def updatePost(post_id):
    data = {}
    data["title"] = request.form['title']
    data["text"] = request.form['text']
    conn = mysql.connect()
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    query = " UPDATE posts SET title='%s', text='%s' WHERE id='" + post_id + "'"
    cursor.execute(query % (data["title"], data["text"]))
    conn.commit()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)