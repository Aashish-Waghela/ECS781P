from flask import Flask
import PavApi
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)
app.config['BUNDLE_ERRORS'] = True
# import PavApi.Views.views
import config
wsgi_app = app.wsgi_app
api = Api(app)

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()


import PavApi.Views.views, PavApi.Models.models, PavApi.Resources.resources

api.add_resource(PavApi.Resources.resources.UserRegistration, '/registration')
api.add_resource(PavApi.Resources.resources.UserLogin, '/login')
api.add_resource(PavApi.Resources.resources.AllUsers, '/users')
api.add_resource(PavApi.Resources.resources.Task, '/task')
api.add_resource(PavApi.Resources.resources.FeedList, '/feedlist')
api.add_resource(PavApi.Resources.resources.FeedDetails, '/feeddetails')