from smartiot import app
app.config.from_pyfile('bin/config/flask_config.cfg')
if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(host="0.0.0.0",port="8080")
    # app.run()
