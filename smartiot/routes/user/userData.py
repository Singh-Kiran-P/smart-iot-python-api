from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask, Response, render_template, flash, redirect, session, url_for, logging, request, Blueprint, json
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import json

from werkzeug.security import generate_password_hash, check_password_hash

from passlib.hash import sha256_crypt


userData_bp = Blueprint(
    'userData_bp',
    __name__
)


@userData_bp.route('/showLogs', methods=['POST'])
def showLogs():
    content = request.get_json(force=True)

    userId = content['userId']

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "SELECT logs.info as Permission  ,logs.value,logs.deviceName as Eindpoint,devices.name,logs.createdOn from logs inner JOIN devices on logs.deviceId = devices.id WHERE logs.userId = %s ORDER BY `logs`.`createdOn` DESC", [userId])

    if result > 0:

        jsondata = []
        data = cur.fetchall()

        for row in data:
            if row['Permission'] == "":
                row['Permission'] = "Permission Granted"
            jsondata.append(row)

        return Response(json.dumps(jsondata), mimetype='application/json')

    else:
        js = [
            {"message": "There are null logs for this user in our database", "status": 465}]
        return Response(json.dumps(js), mimetype='application/json')


@userData_bp.route('/sendFeedback', methods=['POST'])
def sendFeedback():
    content = request.get_json(force=True)

    userId = content['userId']
    feedback_context = content['feedback']
    platform = content['platform']

    # create a cursur
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO feedback(feedback,userId,platform) VALUES(%s,%s,%s)",
                (feedback_context, userId, platform))

    # commit to Datebase
    mysql.connection.commit()


    FBC = "";
    result = cur.execute(
        "SELECT firebase_token FROM users where username = 'admin'")

    if result > 0:

        data = cur.fetchone()
        FBC = data['firebase_token']
     
    # close connection
    cur.close()
    print("POST request Register")

    from pyfcm import FCMNotification

    push_service = FCMNotification(
    api_key="AAAAwTL24fI:APA91bEDQy3avVBNw2XcFLztyZ7UTFKd1RtRmf_h7V51McuyPwZp4fM0K68nYoPy1hH46FBAnVEhkkHsK8EVocHNMU9N9CSGddlB2HuhKiGJ6zN0cFhlWlTqgS37IcWgIFZJ2UurhJXy")

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = FBC
    message_title = "Feedback"
    message_body = "Feedback in your inbox open Admin account"
    result = push_service.notify_single_device(
    registration_id=registration_id, message_title=message_title, message_body=message_body)

    print(result)
    return json_response(status=200, message="Send succesfully")


@userData_bp.route('/changeUserData', methods=['PUT'])
def changeUserData():
    content = request.get_json(force=True)

    userId = content['userId']
    name = content['name']
    email = content['email']
    password = generate_password_hash(content['password'], method='sha256')

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "UPDATE users SET name = %s, email = %s, password = %s WHERE users.id = %s", (name, email, password, userId))

    # commit to Datebase
    mysql.connection.commit()

    # close connection
    cur.close()
    return json_response(
        message="User data succesfuly updated",
        status=200
    )



@userData_bp.route('/request_permission', methods=['POST'])
def sendFeedback_request():
    content = request.get_json(force=True)

    userId = content['userId']
    endpoint = content['endpoint']


        # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute("SELECT * FROM endpoints WHERE userId = %s AND name = %s",
                ( userId,endpoint))
    if result > 0:
        return json_response(
            message="You already have access to this eindPoint",
            status=200
            )
    
    result = cur.execute("SELECT * FROM `permission_requests` WHERE userId = %s AND endPoint = %s",
                ( userId,endpoint))
    if result > 0:
        return json_response(
            message="You already have send a request for this endPoint",
            status=200
            )
        

    # commit to Datebase
    mysql.connection.commit()

    # create a cursur
    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO `permission_requests` (`id`, `route_permissionId`, `userId`, `endPoint`) VALUES (NULL, %s, %s, %s)",
                ( "1", userId,endpoint))

    # commit to Datebase
    mysql.connection.commit()

    FBC = "";
    result = cur.execute(
        "SELECT firebase_token FROM users where username = 'admin'")

    if result > 0:

        data = cur.fetchone()
        FBC = data['firebase_token']

    from pyfcm import FCMNotification

    push_service = FCMNotification(
    api_key="AAAAwTL24fI:APA91bEDQy3avVBNw2XcFLztyZ7UTFKd1RtRmf_h7V51McuyPwZp4fM0K68nYoPy1hH46FBAnVEhkkHsK8EVocHNMU9N9CSGddlB2HuhKiGJ6zN0cFhlWlTqgS37IcWgIFZJ2UurhJXy")

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = FBC
    message_title = "Route permission"
    message_body = "Check requests for changing permissions"
    result = push_service.notify_single_device(
    registration_id=registration_id, message_title=message_title, message_body=message_body)

    return json_response(
    message="Change route permission request sent!",
    status=200
    )


@userData_bp.route('/changeFCM_token', methods=['POST'])
def changeFCM_token():

    return ""
