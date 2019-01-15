from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
iot_led_bp = Blueprint(
    'iot_led_bp',
    __name__    
)

@iot_led_bp.route("/led",methods=['POST'])
def led_ON_OFF():
    led_pin = 7
    content = request.get_json()
    led = content['led']
    userid = content['userId']
    permisson =""
   
    if led == "0":
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW) 
        GPIO.output(led_pin, GPIO.LOW) 

        print("ledoff")

        #response
        return json_response( 
        message="Led is ON",
        permission ="granted",
        status = 200
        ) 

    if led == "1":
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.HIGH)        
        GPIO.output(led_pin, GPIO.HIGH) 

        print("ledon")

        #response
        return json_response( 
        message="Led is ON",
        permission ="granted",
        status = 200
        ) 
