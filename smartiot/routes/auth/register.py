from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint
from passlib.hash import sha256_crypt


register_bp = Blueprint(
    'register',
    __name__    
)

@register_bp.route('/register',methods=['GET','POST'])
def json_register():     
    if request.method == 'POST':
        content = request.get_json()
        name = content['name']
        firstname = content['firstname']
        email = content['email']
        username = content['username']
        password = sha256_crypt.encrypt(str(content['password']))
        print(content)
        #create Cursor
        cur = mysql.connection.cursor()
        print("test")


        #execute query
        cur.execute("INSERT INTO users(naam,voornaam,email,username,password) VALUES(%s,,%s%s,%s,%s)",(name,firstname,email,username,password))

        #commit to Datebase
        mysql.connection.commit()

        #close connection
        cur.close()
        print("POST request Register")
        return ""

    if request.method == 'GET':
        print("GET request")
        return "GET request to Register"
    return ""
