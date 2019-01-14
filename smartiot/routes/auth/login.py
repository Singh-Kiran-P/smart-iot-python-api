from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json

from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt


login_bp = Blueprint(
    'login',
    __name__    
)


@login_bp.route('/login' , methods=['POST'])
def login_request():
    content = request.get_json(force=True)  
    
    username_candidate = content['username']
    password_candidate = content['password']

    #create a cursur 
    cur = mysql.connection.cursor()

    #get user by username
    result  = cur.execute("SELECT * FROM users WHERE username = %s",[username_candidate])

    if result > 0:
        #get stored hash
        data = cur.fetchone()
        id = data['id']
        naam = data['naam']
        email = data['email']
        username = data['username']
        password = data['password']
        role = data['role']


        #compare password
        if check_password_hash(password, password_candidate):
            # Passed
            session['logged_in'] = True
            session['id'] = id
            session['naam'] = naam
            session['email'] = email
            session['username'] = username
            session['role'] = role
            app.logger.info('PASSWORD MATCHED')

            #response
            return json_response( 
        id = id,
        naam = naam,
        email = email,
        username = username,
        role = role,
        message="You are now logged in"
        ) 
        else:
            app.logger.info('PASSWORD NOT MATCHED')    

            #response
            return json_response(success= "flase",message = "Password not matched")
        
        #Close connection
        cur.close()
    else:
        app.logger.info('NO USER')

        #response
        return json_response(success= "flase",message = "User not found")


@login_bp.route('/logout')
def logout_request():
    session.clear()

    #response
    return json_response(message = "You are now logged out")
 