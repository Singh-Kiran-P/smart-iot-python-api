from flask import Blueprint,render_template,request
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
iot_pir_bp = Blueprint(
    'iot_pir_bp',
    __name__    
)

