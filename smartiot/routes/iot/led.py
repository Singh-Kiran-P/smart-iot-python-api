from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from smartiot.bin.config.db_config import mysql
from smartiot.routes.route_Permissions.userPermissions import getPermissions
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
from pyfcm import FCMNotification
import datetime

iot_led_bp = Blueprint(
    'iot_led_bp',
    __name__    
)
now = datetime.datetime.now()
dataTime=now.strftime("%Y-%m-%d %H:%M")

#define led oin
led01_pin = 7

@iot_led_bp.route("/led",methods=['POST'])
def led_ON_OFF():
    
    try:
        content = request.get_json()
        action = content['action']
        userid = content['userId']
        firebasetoken = content['firebase_token']
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
        if action == "0":
            #mysql
            #execute query
            sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId,createdOn) VALUES('',%s,%s,%s,'1',%s,%s)"
            print(str(sql))
            #create a cursur             
            cur = mysql.connection.cursor()
            result  = cur.execute(sql,("off","state",endpoint,userid,dataTime))
            #commit to Datebase
            mysql.connection.commit()

         

            return ledOff("granted",firebasetoken)
            print('granted')
            



        if action == "1":
            #mysql
            #execute query
            sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId,createdOn) VALUES('',%s,%s,%s,'1',%s,%s)"
            print(str(sql))
            #create a cursur             
            cur = mysql.connection.cursor()
            result  = cur.execute(sql,("on","state",endpoint,userid,dataTime))
            #commit to Datebase
            mysql.connection.commit()

            #close connection
            cur.close()

            return ledOn("granted",firebasetoken)
            print('granted')


    if permissions is "denied":

        #mysql
        #execute query
        sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId,createdOn) VALUES(%s,'','',%s,'1',%s,%s)"
        print(str(sql))
        #create a cursur             
        cur = mysql.connection.cursor()
        result  = cur.execute(sql,("Permission Denied",endpoint,userid,dataTime))
        #commit to Datebase
        mysql.connection.commit()
        #close connection
        cur.close()

        #response
        return json_response( 
        message="Permission denied for this user",
        status = 403
        ) 
        print('denied')
    return"" 



# led process
def ledOn(per,token):
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(led01_pin, GPIO.OUT, initial=GPIO.HIGH) 
    GPIO.output(led01_pin, GPIO.HIGH) 



    print("ledon")



    #create a cursur 
    cur = mysql.connection.cursor()

    result  = cur.execute("SELECT * FROM users WHERE firebase_token = %s ",[token])

    if result > 0:
        print(token)
        #send notification to gsm firebase

        push_service = FCMNotification(
        api_key="AAAAwTL24fI:APA91bEDQy3avVBNw2XcFLztyZ7UTFKd1RtRmf_h7V51McuyPwZp4fM0K68nYoPy1hH46FBAnVEhkkHsK8EVocHNMU9N9CSGddlB2HuhKiGJ6zN0cFhlWlTqgS37IcWgIFZJ2UurhJXy")

        # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

        registration_id = token
        message_title = "Server notifications"
        message_body = "Led01 is ON         "+str(datetime.datetime.now())
        result = push_service.notify_single_device(
        registration_id=registration_id, message_title=message_title, message_body=message_body)



    #response
    return json_response( 
    permission = per,
    message="Led is ON",
    status = 200
    ) 

def ledOff(per,token):
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(led01_pin, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.output(led01_pin, GPIO.LOW) 

    print("ledoff")

    #create a cursur 
    cur = mysql.connection.cursor()

    result  = cur.execute("SELECT * FROM users WHERE firebase_token = %s ",[token])

    if result > 0:
        print(token)
        #send notification to gsm firebase

        push_service = FCMNotification(
        api_key="AAAAwTL24fI:APA91bEDQy3avVBNw2XcFLztyZ7UTFKd1RtRmf_h7V51McuyPwZp4fM0K68nYoPy1hH46FBAnVEhkkHsK8EVocHNMU9N9CSGddlB2HuhKiGJ6zN0cFhlWlTqgS37IcWgIFZJ2UurhJXy")

        # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

        registration_id = token
        message_title = "Server noti"
        message_body = "Led01 is OFF        " + str(datetime.datetime.now())
        result = push_service.notify_single_device(
        registration_id=registration_id, message_title=message_title, message_body=message_body)



    #response
    return json_response( 
    permission = per,
    message="Led is ON",
    status = 200
    ) 
