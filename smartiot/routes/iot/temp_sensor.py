from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from smartiot.bin.config.db_config import mysql
from smartiot.routes.route_Permissions.userPermissions import getPermissions
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

iot_temp_bp = Blueprint(
    'iot_temp_bp',
    __name__    
)

@iot_temp_bp.route("/temp",methods=['GET'])
def tempMeture():
    return json_response(
        id = "temp01",
        meture = 18.6
    )


