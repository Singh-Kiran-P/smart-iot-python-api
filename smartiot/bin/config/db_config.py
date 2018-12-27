from smartiot import app
from flask_mysqldb import MySQL

#config Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'singh,,'
app.config['MYSQL_DB'] = 'smartiot'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init mysql
mysql=MySQL(app)