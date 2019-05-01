from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

from werkzeug.security import generate_password_hash, check_password_hash
from passlib.hash import sha256_crypt


login_bp = Blueprint(
    'login',
    __name__    
)

mail = Mail(app)

s = URLSafeTimedSerializer('smartiot.singh')


@login_bp.route('/login' , methods=['POST'])
def login_request():
    content = request.get_json(force=True)  
    
    user_candidate = content['username']
    password_candidate = content['password']

    #create a cursur 
    cur = mysql.connection.cursor()

    #check if confirmed user
    if '@' in user_candidate:
        result  = cur.execute("SELECT * FROM users WHERE email = %s AND confirmed ='0'",[user_candidate])
    else:
        result  = cur.execute("SELECT * FROM users WHERE username = %s AND confirmed ='0'",[user_candidate])

    if result > 0:
        #get email form database
        data = cur.fetchone()
        email = data['email']

        # #send confirm email to user
        # token = s.dumps(email, salt='email-confirm')#generate email token remind salt
        # msg = Message('Email Confirmation',sender='singh@singhthebeast.com',recipients=[email])
        # link = url_for('confirm_email.confirm_email', token=token, external=True)
        # msg.html = render_template('emails/confirm_email.html',link = link)
        # mail.send(msg)

        return json_response( 
        id = None,
        naam = None,
        email = None,
        username = None,
        role = None,
        message="Email is not confirmed. Please check your email " +email,
        status = 409
        ) 
        print("########################################################################################")


    
    #get user by email
    if '@' in user_candidate:
        result  = cur.execute("SELECT * FROM users WHERE email = %s AND confirmed ='1'",[user_candidate])

    #get user by username
    else:
        result  = cur.execute("SELECT * FROM users WHERE username = %s AND confirmed ='1'",[user_candidate])

    if result > 0:
        #get stored hash
        data = cur.fetchone()
        id = data['id']
        naam = data['name']
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
        name = naam,
        email = email,
        username = username,
        role = role,
        message="You are now logged in",
        status = 200
        ) 
        else:
            app.logger.info('PASSWORD NOT MATCHED')    

            #response password not matched
            return json_response( 
        id = None,
        naam = None,
        email = None,
        username = None,
        role = None,
        message="Password not matched",
        status = 409
        ) 
        
        #Close connection
        cur.close()
    else:
        app.logger.info('NO USER')

        #response user not found
        return json_response( 
        id = None,
        naam = None,
        email = None,
        username = None,
        role = None,
        message="user not found",
        status = 410
        ) 


@login_bp.route('/logout')
def logout_request():
    session.clear()

    #response
    return json_response(message = "You are now logged out")
 
