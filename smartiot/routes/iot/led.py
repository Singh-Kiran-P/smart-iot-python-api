from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
from smartiot.bin.config.db_config import mysql
from smartiot.routes.route_Permissions.userPermissions import getPermissions

iot_led_bp = Blueprint(
    'iot_led_bp',
    __name__    
)

#define led oin
led_pin = 7

@iot_led_bp.route("/led",methods=['POST'])
def led_ON_OFF():
    
    try:
        content = request.get_json()
        led = content['led']
        userid = content['userId']
        endpoint = content['endPoint']
    except:
        #response
        return json_response( 
        message="Internal server error",
        status = 500
        )  
    permissions = getPermissions(userid,endpoint)

    print(str(permissions))

    if permissions is "granted":
        if led == "0":
            return ledOff()
            print('granted')


        if led == "1":
            return ledOn()
            print('granted')


    if permissions is "denied":
        #response
        return json_response( 
        message="Permission denied for this user",
        status = 403
        ) 
        print('denied')
    return"" 



# led process
def ledOn():
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH) 
    GPIO.output(led_pin, GPIO.HIGH) 

    

    print("ledon")

    #response
    return json_response( 
    message="Led is ON",
    status = 200
    ) 

def ledOff():
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.output(led_pin, GPIO.LOW) 

    print("ledoff")

    #response
    return json_response( 
    message="Led is OFF",
    status = 200
    ) 


