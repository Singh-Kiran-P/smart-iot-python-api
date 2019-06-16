from smartiot import app
from smartiot.bin.config.db_config import mysql
from flask import Flask,render_template,flash,redirect,session,url_for,logging,request,Blueprint,json,session
from flask_json import FlaskJSON, JsonError, json_response, as_json



email =""
permission =""

def getPermissions(fUserId,fEndpointName):
    if fUserId is "1":
        return "granted"
    print(str(fUserId) +" "+str(fEndpointName))

    sql =  ""   
    sql += "SELECT users.email,route_permissions.permission FROM users"
    sql +=" INNER JOIN endpoints on users.id = endpoints.userId"
    sql +=" INNER JOIN route_permissions on endpoints.permissionId = route_permissions.id"
    sql +=" WHERE users.id = "+str(fUserId)+" AND endpoints.name = '"+str(fEndpointName)+"'"
    

    print (str(sql))

    #mysql
    #create a cursur 
    cur = mysql.connection.cursor()

    result  = cur.execute(sql)
    print(result)
    if result > 0:
        #get stored hash
        data = cur.fetchone()     
        email = data['email']
        permission = data['permission']

        if permission in "granted":
            print(str(permission))
            return "granted"
        if permission in "denied":
            return "denied"


    if result == 0:
        return "denied"





