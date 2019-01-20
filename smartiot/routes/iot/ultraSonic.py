from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from smartiot.bin.config.db_config import mysql
from smartiot.routes.route_Permissions.userPermissions import getPermissions
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

iot_ultraSonic_bp = Blueprint(
    'iot_ultra-sonic_bp',
    __name__    
)

#define led oin
led_pin = 7

@iot_ultraSonic_bp.route("/ultra",methods=['POST'])
def ultraSonic():
     
    try:
        content = request.get_json()
        action = content['action']
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
        print('granted')
        if action == "measure":
            #mysql
            #execute query
            sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId) VALUES('',%s,%s,%s,'2',%s)"
            print(str(sql))
            GPIO.cleanup()
            #get data from sensor 
            distance = measure_average() 
            d=round(distance ,2)
            print( "Distance : {0} cm".format(d))
            distance_cm = format(d)
            #create a cursur             
            cur = mysql.connection.cursor()
            result  = cur.execute(sql,(distance_cm,"proximity",endpoint,userid))
            #commit to Datebase
            mysql.connection.commit()

         

            return json_response(
                distance = distance_cm,
                message = "Distance in cm",
                status  =200
                )
           
            



        if action == "":#other fuctions
            #mysql
            #execute query
            sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId) VALUES('',%s,%s,%s,'1',%s)"
            print(str(sql))
            #create a cursur             
            cur = mysql.connection.cursor()
            result  = cur.execute(sql,("on","state",endpoint,userid))
            #commit to Datebase
            mysql.connection.commit()

            #close connection
            cur.close()

            return 
            print('granted')


    if permissions is "denied":

        #mysql
        #execute query
        sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId) VALUES(%s,'','',%s,'1',%s)"
        print(str(sql))
        #create a cursur             
        cur = mysql.connection.cursor()
        result  = cur.execute(sql,("Permission Denied",endpoint,userid))
        #commit to Datebase
        mysql.connection.commit()
        #close connection
        cur.close()

        #response
        return json_response( 
        distance = "",
        message="Permission denied for this user",
        status = 403
        ) 
        print('denied')
    


# measure distance

def measure():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD) 
    GPIO_TRIGGER = 15
    GPIO_ECHO    = 16
    print ("Ultrasonic Measurement")
    GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # Trigger
    GPIO.setup(GPIO_ECHO,GPIO.IN)      # Echo
    # Set trigger to False (Low)
    GPIO.output(GPIO_TRIGGER, False)

    # This function measures a distance
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2

    return distance

def measure_average():
    # This function takes 3 measurements and
    # returns the average.
    distance1=measure()
    time.sleep(0.1)
    distance2=measure()
    time.sleep(0.1)
    distance3=measure()
    distance = distance1 + distance2 + distance3
    distance = distance / 3
    return distance

  

