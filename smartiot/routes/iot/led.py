from flask import Blueprint,render_template,request
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
iot_led_bp = Blueprint(
    'iot_led_bp',
    __name__    
)

@iot_led_bp.route("/led",methods=['POST'])
def led_ON_OFF():
    content = request.get_json()
    if content['led'] == "0":
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(8, GPIO.OUT, initial=GPIO.LOW) 
        GPIO.output(8, GPIO.LOW) 

        print("ledoff")
        return ""

    if content['led'] == "1":
        GPIO.setwarnings(False) 
        GPIO.setmode(GPIO.BOARD) 
        GPIO.setup(8, GPIO.OUT, initial=GPIO.HIGH)        
        GPIO.output(8, GPIO.HIGH) 

        print("ledon")
        return ""
