from smartiot import app
from flask_mysqldb import MySQL

# #.env setting up
# import os
# from os.path import join, dirname,abspath
# from dotenv import load_dotenv

# dotenv_path = join(dirname(__file__), 'venv/.env')
# print(dotenv_path)

# # Accessing variables.


# host = os.getenv('MYSQL_HOST')
# user = os.getenv('MYSQL_USER')
# password = os.getenv('MYSQL_PASSWORD')
# db = os.getenv('MYSQL_DB')
# print(user)

#config Mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'singh,,'
app.config['MYSQL_DB'] = 'smartiot'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init mysql
mysql=MySQL(app)