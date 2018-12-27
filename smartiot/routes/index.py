from flask import Blueprint,render_template

index_bp = Blueprint(
    'index',
    __name__    
)

@index_bp.route("/")
def index():
    return "<h1>MY SMART IOT GIP</h1>"  bvb