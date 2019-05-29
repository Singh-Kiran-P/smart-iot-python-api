from flask import Flask
from flask_json import FlaskJSON, JsonError, json_response, as_json
import ptvsd


app = Flask(__name__)
app.config.from_pyfile('bin/config/flask_config.cfg')
FlaskJSON(app)

from smartiot.routes.index import index_bp

#auth
from smartiot.routes.auth.login import login_bp
from smartiot.routes.auth.register import register_bp
from smartiot.routes.auth.confirm import confirm_email_bp

#sensor imports
from smartiot.routes.iot.led import iot_led_bp
from smartiot.routes.iot.pir_sensor import iot_pir_bp
from smartiot.routes.iot.ultraSonic import iot_ultraSonic_bp
from smartiot.routes.iot.temp_sensor import iot_temp_bp


app.register_blueprint(index_bp)

#auth
app.register_blueprint(register_bp,url_prefix='/api/users/')
app.register_blueprint(login_bp,url_prefix='/api/users/')#CHECK
app.register_blueprint(confirm_email_bp,url_prefix='/api/users/')

#settings iot sensors and stuff
app.register_blueprint(iot_led_bp,url_prefix='/api/iot')#CHECK
app.register_blueprint(iot_pir_bp,url_prefix='/api/iot')
app.register_blueprint(iot_ultraSonic_bp,url_prefix='/api/iot')#CHECK
app.register_blueprint(iot_temp_bp,url_prefix='/api/iot')

from pyfcm import FCMNotification

push_service = FCMNotification(
    api_key="AAAAwTL24fI:APA91bEDQy3avVBNw2XcFLztyZ7UTFKd1RtRmf_h7V51McuyPwZp4fM0K68nYoPy1hH46FBAnVEhkkHsK8EVocHNMU9N9CSGddlB2HuhKiGJ6zN0cFhlWlTqgS37IcWgIFZJ2UurhJXy")

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "eZeTsZDEjs4:APA91bF3i-N25eU7h7Jdpa-va8sFHyQXNEa1aCrI3AtaEA5tmqo2bZj04eIrKg-vqpuwJ2Zs_IcIL-b8Kt9o3bNbF0cIi8Ix641jBTw1e2M82J40NPeeCeBckJISr-s_8J8Aa2ELpJ-H"
message_title = "Server"
message_body = "SmartIot server is started"
result = push_service.notify_single_device(
    registration_id=registration_id, message_title=message_title, message_body=message_body)

print(result)

