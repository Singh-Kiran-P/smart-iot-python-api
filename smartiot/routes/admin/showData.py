from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask, Response, render_template, flash, redirect, session, url_for, logging, request, Blueprint, json
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import json

from werkzeug.security import generate_password_hash, check_password_hash

from passlib.hash import sha256_crypt


adminShowData_bp = Blueprint(
    'adminShowData_bp',
    __name__
)


@adminShowData_bp.route('/showUsers_perms', methods=['GET'])
def showUsers_permissons():

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "SELECT users.id as userId,users.name,route_permissions.permission,endpoints.name as permissionEndpoint " +
        "FROM ((users inner JOIN endpoints ON users.id = endpoints.userId) " +
        "inner JOIN route_permissions on endpoints.permissionId = route_permissions.id)")
    jsondata = []

    data = cur.fetchall()
    print(data)
    for row in data:
        jsondata.append(row)

    print(jsondata)

    return Response(json.dumps(jsondata), mimetype='application/json')


@adminShowData_bp.route('/showUsers', methods=['GET'])
def showUsers():

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "SELECT id,name,email,username,password,role,firebase_token,confirmed FROM users")

    jsondata = []
    data = cur.fetchall()

    for row in data:
        jsondata.append(row)

    return Response(json.dumps(jsondata), mimetype='application/json')


@adminShowData_bp.route('/showLogs', methods=['GET'])
def showLogs():

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "SELECT users.name, users.role,logs.info as Permission ,logs.value,logs.deviceName as Eindpoint,devices.name,logs.createdOn from logs inner JOIN devices on logs.deviceId = devices.id INNER JOIN users on logs.userId = users.id ORDER BY `logs`.`createdOn` DESC")

    jsondata = []
    data = cur.fetchall()

    for row in data:
        jsondata.append(row)

    return Response(json.dumps(jsondata), mimetype='application/json')


@adminShowData_bp.route('/showDevices', methods=['GET'])
def showDevices():

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "SELECT * FROM devices")

    jsondata = []
    data = cur.fetchall()

    for row in data:
        jsondata.append(row)

    return Response(json.dumps(jsondata), mimetype='application/json')


@adminShowData_bp.route('/showFeedback', methods=['GET'])
def showFeedback():

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "SELECT * FROM feedback")

    jsondata = []
    data = cur.fetchall()

    for row in data:
        jsondata.append(row)

    return Response(json.dumps(jsondata), mimetype='application/json')

#DON'T WORKS !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
@adminShowData_bp.route('/showFeedback_requests', methods=['GET'])
def showFeedback_requests():

    # create a cursur
    cur = mysql.connection.cursor()

    result = cur.execute(
        "SELECT id,name,email,username,password,role,firebase_token,confirmed FROM users")

    jsondata = []
    data = cur.fetchall()

    for row in data:
        jsondata.append(row)

    return Response(json.dumps(jsondata), mimetype='application/json')
