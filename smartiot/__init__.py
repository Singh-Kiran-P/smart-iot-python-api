from flask import Flask
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__)
app.debug = True
FlaskJSON(app)

from smartiot.routes.auth.register import register_bp
from smartiot.routes.auth.login import login_bp
from smartiot.routes.index import index_bp
from smartiot.routes.iot.led import iot_led_bp
from smartiot.routes.iot.pir_sensor import iot_pir_bp


app.register_blueprint(register_bp,url_prefix='/api/users/')
app.register_blueprint(index_bp)
app.register_blueprint(iot_led_bp,url_prefix='/api/iot')
app.register_blueprint(iot_pir_bp,url_prefix='/api/iot')
app.register_blueprint(login_bp,url_prefix='/api/users/')