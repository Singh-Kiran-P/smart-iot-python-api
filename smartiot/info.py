from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json


#mysql
 #create a cursur 
    cur = mysql.connection.cursor()

    result  = cur.execute("SELECT * FROM users WHERE username = %s",[user_candidate])

        if result > 0:
            #get stored hash
            data = cur.fetchone()
            id = data['id']
            naam = data['naam']
            email = data['email']
            username = data['username']
            password = data['password']
            role = data['role']


#blueprint

login_bp = Blueprint(
    'login',
    __name__    
)


@login_bp.route('/login' , methods=['POST'])
def login_request():


#return json
 return json_response( 
        id = id,
        naam = naam,
        email = email,
        username = username,
        role = role,
        message="You are now logged in",
        status = 200
        ) 
