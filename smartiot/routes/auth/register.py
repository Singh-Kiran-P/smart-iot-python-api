from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask, render_template, flash, redirect, session, url_for, logging, request, Blueprint, json
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
    # EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='smart.iot.singh@gmail.com',
    MAIL_PASSWORD='FA4UpyL3y9naQwH'
)

mail = Mail(app)

s = URLSafeTimedSerializer('smartiot.singh')


@register_bp.route('/register', methods=['POST'])
def json_register():
    content = request.get_json(force=True)
    name = content['name']
    email = content['email']
    username = content['username']
    password = generate_password_hash(content['password'], method='sha256')
    firebaseToken = content['firebase_token']

    print(content)
    print(password)

    # create Cursor
    cur = mysql.connection.cursor()
    print("test")

    # check if username is taken
    checkUsername = cur.execute(
        "SELECT * FROM users WHERE username = (%s)", [username])
    if int(checkUsername) > 0:
        return json_response(message="That username is already taken, please choose another", status=901)

    checkEmail = cur.execute("SELECT * FROM users WHERE email = (%s)", [email])
    if int(checkEmail) > 0:
        return json_response(message="This email is already in use, please choose another ", status=902)
    now = datetime.datetime.now()
    dataTime=now.strftime("%Y-%m-%d %H:%M")
    # execute query
    cur.execute("INSERT INTO users(name,email,username,password,role,firebase_token,registerDate) VALUES(%s,%s,%s,%s,%s,%s,%s)",
                (name, email, username, password, "normal_user", firebaseToken,dataTime))

    # commit to Datebase
    mysql.connection.commit()

    # close connection
    cur.close()
    print("POST request Register")

    # send confirm email to user
    # generate email token remind salt
    token = s.dumps(email, salt='email-confirm')
    msg = Message('Email Confirmation',
                  sender='singh@singhthebeast.com', recipients=[email])
    link = url_for('confirm_email.confirm_email', token=token, external=True)
    msg.html = render_template('emails/confirm_email.html', link=link)
    mail.send(msg)

    return json_response(status=200, message="Confirm email Send to "+email)



# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message('Email Confirmation',
#                   sender='singh@singhthebeast.com', recipients=[email])
#     link = url_for('confirm_email.confirm_email', token=token, external=True)
#     msg.body = "To reset your password, visit the following link:{url_for('reset_token', token=token, _external=True)}If you did not make this request then simply ignore this email and no changes will be made."
    
#     mail.send(msg)


# @app.route("/reset_password", methods=['GET', 'POST'])
# def reset_request():
#     if current_user.is_authenticated:
#         return redirect(url_for('home'))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash('An email has been sent with instructions to reset your password.', 'info')
#         return redirect(url_for('login'))
#     return render_template('reset_request.html', title='Reset Password', form=form)


# @app.route("/reset_password/<token>", methods=['GET', 'POST'])
# def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
    return None 