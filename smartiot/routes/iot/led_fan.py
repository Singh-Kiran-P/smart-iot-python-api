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

#confi GPIO
#endpoint led01 -->Room1
led01_pin = 24
#endpoint led02-->Room2
led02_pin = 17
#endpoint led03-->room3
led03_pin = 27
#endpoitn fan01
fan01_relay_pin = 20
#endpoitn fanMain
fan02_relay_pin = 16

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM) 
GPIO.setup(led01_pin, GPIO.OUT) 
GPIO.setup(led02_pin, GPIO.OUT) 
GPIO.setup(fan01_relay_pin, GPIO.OUT)
GPIO.setup(fan02_relay_pin, GPIO.OUT)
GPIO.output(led01_pin, GPIO.LOW)
GPIO.output(led02_pin, GPIO.LOW)
GPIO.output(fan01_relay_pin, GPIO.HIGH)
GPIO.output(fan02_relay_pin, GPIO.HIGH)

#route -> api/iot/led
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

    print(str(permissions) +"helloo" )

    if permissions is "granted":
        if action is "0":
            #mysql
            #execute query
            sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId,createdOn) VALUES('',%s,%s,%s,'1',%s,%s)"
            print(str(sql))
            #create a cursur             
            cur = mysql.connection.cursor()
            result  = cur.execute(sql,("off","state",endpoint,userid,dataTime))
            #commit to Datebase
            mysql.connection.commit()

         

            return ledOff("granted",firebasetoken,endpoint)
            print('granted')
            



        if action is "1":
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

            return ledOn("granted",firebasetoken,endpoint)
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


#route -> api/iot/led
@iot_led_bp.route("/fan",methods=['POST'])
def fanON_OFF():

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

    print(str(permissions) +"helloo" )

    if permissions is "granted":
        if action is "0":
            #mysql
            #execute query
            sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId,createdOn) VALUES('',%s,%s,%s,'1',%s,%s)"
            print(str(sql))
            #create a cursur             
            cur = mysql.connection.cursor()
            result  = cur.execute(sql,("off","state",endpoint,userid,dataTime))
            #commit to Datebase
            mysql.connection.commit()

         

            return ledOff("granted",firebasetoken,endpoint)
            print('granted')
            



        if action is "1":
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

            return ledOn("granted",firebasetoken,endpoint)
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
        print('denied#################################################################')
        #response
        return json_response( 
        message="Permission denied for this user",
        status = 403
        ) 
      
    return"" 
# led process
def ledOn(per,token,endpoint):
    if endpoint == "led01":
        GPIO.output(led01_pin, GPIO.HIGH) 



        print("ledon01")



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
        message="Led01 is ON",
        status = 200
        ) 
    if endpoint == "led02":
        
        GPIO.output(led02_pin, GPIO.HIGH) 
        print(endpoint)



        print("led02_pin")



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
            message_body = "led02_pin is ON         "+str(datetime.datetime.now())
            result = push_service.notify_single_device(
            registration_id=registration_id, message_title=message_title, message_body=message_body)



        #response
        return json_response( 
        permission = per,
        message="led02_pin is ON",
        status = 200
        )         
    if endpoint == "all":
        GPIO.output(led01_pin, GPIO.HIGH) 
        GPIO.output(led02_pin, GPIO.HIGH) 
        #response
        return json_response( 
        permission = "granted",
        message="ALL Eindpoints ON",
        status = 200
        )  
    
    #fan 
    if endpoint == "fan01":
        
        GPIO.output(fan01_relay_pin, GPIO.LOW) 
        print(endpoint)



        print("fan01")



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
            message_body = "Fan01 is ON         "+str(datetime.datetime.now())
            result = push_service.notify_single_device(
            registration_id=registration_id, message_title=message_title, message_body=message_body)



        #response
        return json_response( 
        permission = per,
        message="Fan01 is ON",
        status = 200
        )         
         #fan 
    if endpoint == "fan_main":
        
        GPIO.output(fan02_relay_pin, GPIO.LOW) 
        print(endpoint)



        print("fan01")



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
            message_body = "Main fan is ON         "+str(datetime.datetime.now())
            result = push_service.notify_single_device(
            registration_id=registration_id, message_title=message_title, message_body=message_body)



        #response
        return json_response( 
        permission = per,
        message="Main fan is ON",
        status = 200
        )         
    #response

    return json_response( 
    permission = "Denied",
    message="Eindpoint not found",
    status = 200
    )     
def ledOff(per,token,endpoint):
    if endpoint == "led01":
        GPIO.output(led01_pin, GPIO.LOW) 

        print("ledoff01")

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
        message="Led01 is OFF",
        status = 200
        ) 
    if endpoint == "led02":
        GPIO.output(led02_pin, GPIO.LOW) 

        print("led02_pin")

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
            message_body = "led02_pin is OFF        " + str(datetime.datetime.now())
            result = push_service.notify_single_device(
            registration_id=registration_id, message_title=message_title, message_body=message_body)



        #response
        return json_response( 
        permission = per,
        message="led02_pin is OFF",
        status = 200
        ) 
    if endpoint == "all":
        GPIO.output(led01_pin, GPIO.LOW) 
        GPIO.output(led02_pin, GPIO.LOW) 
        #response
        return json_response( 
        permission = "granted",
        message="ALL Eindpoints OFF",
        status = 200
        )  
    
    if endpoint == "fan01":
        GPIO.output(fan01_relay_pin, GPIO.HIGH) 
        

        print("fan01")

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
            message_body = "fan01 is OFF        " + str(datetime.datetime.now())
            result = push_service.notify_single_device(
            registration_id=registration_id, message_title=message_title, message_body=message_body)



        #response
        return json_response( 
        permission = per,
        message="fan01 is OFF",
        status = 200
        ) 
    #response
    if endpoint == "fan_main":
        GPIO.output(fan02_relay_pin, GPIO.HIGH) 
        

        print("fanMain")

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
            message_body = "Main fan is OFF        " + str(datetime.datetime.now())
            result = push_service.notify_single_device(
            registration_id=registration_id, message_title=message_title, message_body=message_body)



        #response
        return json_response( 
        permission = per,
        message="Main fan is OFF",
        status = 200
        ) 
    #response
    return json_response( 
    permission = "Denied",
    message="Eindpoint not found",
    status = 200
    ) 


#route -> api/iot/led
@iot_led_bp.route("/mainKill",methods=['DELETE'])
def kill():

    GPIO.output(led01_pin, GPIO.LOW)
    GPIO.output(led02_pin, GPIO.LOW)
    GPIO.output(fan01_relay_pin, GPIO.HIGH)
    GPIO.output(fan02_relay_pin, GPIO.HIGH)

    return json_response( 
    permission = "",
    message="Kill switch activated",
    status = 200
    ) 






