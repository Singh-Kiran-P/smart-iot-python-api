from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json
from flask_json import FlaskJSON, JsonError, json_response, as_json

from passlib.hash import sha256_crypt


register_bp = Blueprint(
    'register',
    __name__    
)


@register_bp.route('/register',methods=['POST'])
def json_register():  
    content = request.get_json(force=True)
    name = content['name']
    email = content['email']
    username = content['username']
    password = sha256_crypt.encrypt(str(content['password']))
    print(content)
    print(password)
    #create Cursor
    cur = mysql.connection.cursor()
    print("test")

    # #check if username is taken 
    # cur.execute("SELECT * FROM users WHERE username = (%s)",(username))
    # if int(check) > 0 :
    #     return json_response(status = "That username is already taken, please choose another")


    #execute query
    cur.execute("INSERT INTO users(naam,email,username,password,role) VALUES(%s,%s,%s,%s,%s)",(name,email,username,password,"normal_user"))

    #commit to Datebase
    mysql.connection.commit()

    #close connection
    cur.close()
    print("POST request Register")

    return json_response(username = username)         

    
   
