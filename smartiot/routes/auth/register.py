from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


from werkzeug.security import generate_password_hash, check_password_hash

from passlib.hash import sha256_crypt


register_bp = Blueprint(
    'register',
    __name__    
)

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'smart.iot.singh@gmail.com',
	MAIL_PASSWORD = 'Singh@iot280'
	)

mail = Mail(app)

s = URLSafeTimedSerializer('smartiot.singh')


@register_bp.route('/register',methods=['POST'])
def json_register():  
    content = request.get_json(force=True)
    name = content['name']
    email = content['email']
    username = content['username']
    password = generate_password_hash(content['password'], method='sha256')
    print(content)
    print(password)

    #create Cursor
    cur = mysql.connection.cursor()
    print("test")

    #check if username is taken 
    checkUsername = cur.execute("SELECT * FROM users WHERE username = (%s)",[username])
    if int(checkUsername) > 0 :
        return json_response(message = "That username is already taken, please choose another",status = 901)

    checkEmail = cur.execute("SELECT * FROM users WHERE email = (%s)",[email])
    if int(checkEmail) > 0 :
        return json_response(message = "This email is already in use, please choose another ",status = 902)


    #execute query
    cur.execute("INSERT INTO users(name,email,username,password,role) VALUES(%s,%s,%s,%s,%s)",(name,email,username,password,"normal_user"))

    #commit to Datebase
    mysql.connection.commit()

    #close connection
    cur.close()
    print("POST request Register")

    #send confirm email to user
    token = s.dumps(email, salt='email-confirm')#generate email token remind salt
    msg = Message('Email Confirmation',sender='singh@singhthebeast.com',recipients=[email])
    link = url_for('confirm_email.confirm_email', token=token, external=True)
    msg.html = render_template('emails/confirm_email.html',link = link)
    mail.send(msg)

    return json_response(status = 200,message="Confirm email Send to "+email)         

    
   
