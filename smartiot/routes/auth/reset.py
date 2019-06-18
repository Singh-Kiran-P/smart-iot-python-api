from smartiot import app
from smartiot.forms.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                             PostForm, RequestResetForm, ResetPasswordForm)

from smartiot.bin.config.db_config import mysql
from flask import Flask, render_template, flash, redirect, session, url_for, logging, request, Blueprint, json
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


from werkzeug.security import generate_password_hash, check_password_hash

from passlib.hash import sha256_crypt


reset_bp = Blueprint(
    'reset',
    __name__
)

app.config.update(
    DEBUG=True,
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='smart.iot.singh@gmail.com',
    MAIL_PASSWORD='FA4UpyL3y9naQwH'
)

mail = Mail(app)

s = URLSafeTimedSerializer('smartiot.singh')


@reset_bp.route('/reset_password', methods=['POST','GET'])
def reset():
    if request.method == 'POST':
        form = RequestResetForm()
        if form.validate_on_submit():
            email=form.email.data                
            # create Cursor
            cur = mysql.connection.cursor()
            print("test")

            # check if username is taken
            result = cur.execute(
                "SELECT * FROM users WHERE email = (%s)", [email])
            mysql.connection.commit()
            cur.close()

            print("####################################################################################")
            print(result)

            if result > 0:    

                # send reset email to user
                # generate rest token remind salt
                token = s.dumps(email, salt='email-reset')
                msg = Message('Password reset',
                            sender='singh@singhthebeast.com', recipients=[email])
                link = url_for('reset.Reset_Password', token=token, external=True)
                msg.html = render_template('emails/password_reset.html', link=link)
                mail.send(msg)


                return json_response(status=200, message="Confirm email Send to "+email)
        
        return render_template('reset_request.html', title='Reset Password', form=form)


    if request.method == 'GET':   
        form = RequestResetForm()
    
        return render_template('reset_request.html', title='Reset Password', form=form)


    


@reset_bp.route('/reset_rassword/<token>', methods=['GET', 'POST'])
def Reset_Password(token):
    if request.method == 'GET':   
        form = ResetPasswordForm()

        return render_template('reset_token.html', title='Reset Password', form=form)


    if request.method == 'POST':

        email = ""
        try:
            email = s.loads(token, salt='email-reset', max_age=3600)# get email form token salt must be same max_age in seconds
            

            form = ResetPasswordForm()
            if form.validate_on_submit():
                
                hashed_password= generate_password_hash(form.password.data, method='sha256')
                    #create Cursor
                cur = mysql.connection.cursor()

                #execute query
                cur.execute("UPDATE users SET password = %s WHERE email = %s",(hashed_password,email))

                #commit to Datebase
                mysql.connection.commit()

                #close connection
                cur.close()     
                
                flash('Your password has been updated! You are now able to log in', 'success')
                return json_response(status = 200,message="Password changed")  
            return render_template('reset_token.html', title='Reset Password', form=form)

            

        except SignatureExpired:
            return json_response(status = 410,message="Confirmtion token is expired")    
        return json_response(status = 200,message="Password changed")  
        
    

 