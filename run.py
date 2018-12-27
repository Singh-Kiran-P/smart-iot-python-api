from smartiot import app


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True,host='0.0.0.0')