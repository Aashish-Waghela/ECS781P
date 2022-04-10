import os
from PavApi import app
import urllib

environemnt = "Production"
connection_string = ('Driver={ODBC Driver 17 for SQL Server};'
                     'Server=tcp:ecs781pserver.database.windows.net,1433;'
                     'Database=ECS781P-DB;'
                     'Uid=emsadmin;'
                     'Pwd=Aashish@123;'
                     'Encrypt=yes;'
                     'TrustServerCertificate=no;'
                     'Connection Timeout=30;')
secret_key = "secret"
jwt_secret = "jwt_secret"

if environemnt == "Debug":
    app.config["DEBUG"] = True
    app.config["DEVELOPMENT"] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key
    app.config['JWT_SECRET_KEY'] = jwt_secret
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

elif environemnt == "Production":
    app.config["DEBUG"] = False
    app.config["DEVELOPMENT"] = False
    params = urllib.parse.quote_plus(connection_string)
    app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect={}".format(params)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = secret_key
    app.config['JWT_SECRET_KEY'] = jwt_secret