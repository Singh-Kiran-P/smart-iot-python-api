from flask import Flask

app = Flask(__name__)
app.debug = True


from smartiot.routes.auth.register import register_bp
from smartiot.routes.index import index_bp
from smartiot.routes.iot.led import iot_led_bp

app.register_blueprint(register_bp)
app.register_blueprint(index_bp)
app.register_blueprint(iot_led_bp,url_prefix='/iot')