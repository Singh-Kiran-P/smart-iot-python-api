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
        "SELECT logs.info as Permission  ,logs.value,devices.name,logs.createdOn from logs inner JOIN devices on logs.deviceId = devices.id WHERE logs.userId = %s", [userId])

    if result > 0:

        jsondata = []
        data = cur.fetchall()

        for row in data:
            if row['Permission'] == "":
                row['Permission'] = "Permission Granted"
            jsondata.append(row)

        return Response(json.dumps(jsondata), mimetype='application/json')

    else:
        return json_response(
            message="There are null logs for this user in our database",
            status=200
        )


@userData_bp.route('/sendFeedback', methods=['POST'])
def sendFeedback():

    return ""


@userData_bp.route('/sendFeedback_request', methods=['POST'])
def sendFeedback_request():

    return ""


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


@userData_bp.route('/changeFCM_token', methods=['POST'])
def changeFCM_token():

    return ""
