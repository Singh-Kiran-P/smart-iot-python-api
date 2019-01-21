from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,send_file
from flask_json import FlaskJSON, JsonError, json_response, as_json
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired


index_bp = Blueprint(
    'index',
    __name__    
)

@index_bp.route("/")
def index():
    return render_template('home.html')

@index_bp.route("/download/smartiotapk")
def downloadAPK():
    try:    
        return send_file('routes/downloads/smartiot.apk', attachment_filename='smart_0.1.apk')
    except Exception as e:
        return str(e)