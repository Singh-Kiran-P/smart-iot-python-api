from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired    
    
    
    
confirm_email_bp = Blueprint(
    'confirm_email',
    __name__    
)

s = URLSafeTimedSerializer('smartiot.singh')
    


@confirm_email_bp.route('/confirm_email/<token>')
def confirm_email(token):
    email =""
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)# get email form token salt must be same max_age in seconds


        #create Cursor
        cur = mysql.connection.cursor()

        #execute query
        cur.execute("UPDATE users SET confirmed = '1' WHERE email = %s",[email])

        #commit to Datebase
        mysql.connection.commit()

        #close connection
        cur.close()     

    except SignatureExpired:
        return json_response(status = 410,message="Confirmtion token is expired")    
    return json_response(status = 200,message="Email Confirmed")  
    
