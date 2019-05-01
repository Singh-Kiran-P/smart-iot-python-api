from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json
from smartiot.bin.config.db_config import mysql
from smartiot.routes.route_Permissions.userPermissions import getPermissions
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time

iot_led_bp = Blueprint(
    'iot_led_bp',
    __name__    
)

#define led oin
led01_pin = 7

@iot_led_bp.route("/led",methods=['POST'])
def led_ON_OFF():
    
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
        if action == "0":
            #mysql
            #execute query
            sql ="INSERT INTO logs(info,value,dataType,deviceName,deviceId,userId) VALUES('',%s,%s,%s,'1',%s)"
            print(str(sql))
            #create a cursur             
            cur = mysql.connection.cursor()
            result  = cur.execute(sql,("off","state",endpoint,userid))
            #commit to Datebase
            mysql.connection.commit()

         

            return ledOff("granted")
            print('granted')
            



        if action == "1":
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

            return ledOn("granted")
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
        message="Permission denied for this user",
        status = 403
        ) 
        print('denied')
    return"" 



# led process
def ledOn(per):
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(led01_pin, GPIO.OUT, initial=GPIO.HIGH) 
    GPIO.output(led01_pin, GPIO.HIGH) 

    

    print("ledon")

    #response
    return json_response( 
    permission = per,
    message="Led is ON",
    status = 200
    ) 

def ledOff(per):
    GPIO.setwarnings(False) 
    GPIO.setmode(GPIO.BOARD) 
    GPIO.setup(led01_pin, GPIO.OUT, initial=GPIO.LOW) 
    GPIO.output(led01_pin, GPIO.LOW) 

    print("ledoff")

    #response
    return json_response( 
    permission = per,
    message="Led is OFF",
    status = 200
    ) 


