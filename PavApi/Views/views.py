from PavApi import app
from flask import jsonify
import os

@app.route('/')
def index():
    return jsonify({'message': "Hello!"})

@app.route('/Article1')
def Article1():
    return app.send_static_file('Article1.html')

@app.route('/Article2')
def Article2():
    return app.send_static_file('Article2.html')

@app.route('/Article3')
def Article3():
    return app.send_static_file('Article3.html')

@app.route('/Article4')
def Article4():
    return app.send_static_file('Article4.html')

@app.route('/Article5')
def Article5():
    return app.send_static_file('Article5.html')

@app.route('/Article6')
def Article6():
    return app.send_static_file('Article6.html')

@app.route('/Article7')
def Article7():
    return app.send_static_file('Article7.html')

# return jsonify({
# 'environemnt': os.environ["environemnt"],
# 'connection_string': os.environ["connection_string"],
# 'secret_key': os.environ["secret"],
# 'jwt_secret': os.environ["jwt_secret"]})