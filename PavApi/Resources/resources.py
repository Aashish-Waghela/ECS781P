import datetime
from flask import jsonify, request
from PavApi.Models.models import UserModel, FeedModel
from flask_restful import Resource, reqparse
from PavApi import app
from flask_jwt_extended import (create_access_token, jwt_required)

class UserRegistration(Resource):
    def post(self):

        Name = request.form.get('Name')
        RoleName = request.form.get('RoleName')
        EmailID = request.form.get('EmailID')
        PhoneNumber = request.form.get('PhoneNumber')
        Status = request.form.get('Status')
        Password = request.form.get('Password')

        data = {
            'Name': str(Name),
            'RoleName': str(RoleName),
            'EmailID': str(EmailID),
            'PhoneNumber': str(PhoneNumber),
            'Status': str(Status),
            'Password': str(Password)
        }

        if UserModel.find_by_username(data['EmailID']):
            return {
                'Data': "null",
                'Message': "User already exists"
            }, 409

        new_user = UserModel(
            Name = data['Name'],
            RoleName=data['RoleName'],
            EmailID=data['EmailID'],
            PhoneNumber=data['PhoneNumber'],
            Status=data['Status'],
            Password = UserModel.generate_hash(data['Password'])
        )

        try:
            new_user.save_to_db()
            return {
                'Data': "null",
                'Message': "User registered successfully"
            }, 201
        except Exception as e:
            return {
                'Data': "null",
                'Message': str(e)
            }, 500


class UserLogin(Resource):
    def post(self):
        EmailID = request.form.get('EmailID')
        Password = request.form.get('Password')

        data = {
            'EmailID': str(EmailID),
            'Password': str(Password)
        }
        current_user = UserModel.find_by_username(data['EmailID'])

        if not current_user:
            return {
                        'Data': "null",
                       'Message': 'User {} doesn\'t exist'.format(data['EmailID'])
                   }, 401

        try:
            if UserModel.verify_hash(data['Password'], current_user.Password):
                access_token = create_access_token(identity=data['EmailID'])
                return {
                           'UserID': str(current_user.UserID),
                           'Name': current_user.Name,
                           'RoleName': current_user.RoleName,
                           'EmailID': current_user.EmailID,
                           'PhoneNumber': current_user.PhoneNumber,
                           'Status': current_user.Status,
                           'access_token': access_token
                       }, 200
            else:
                return {
                           'Data': "null",
                           'Message': 'Invalid Password'
                       }, 401
        except Exception as e:
            return {
                       'Data': "null",
                       'Message': str(e)
                   }, 500


class UserUpdate(Resource):
    @jwt_required()
    def put(self):

        Name = request.form.get('Name')
        RoleName = request.form.get('RoleName')
        EmailID = request.form.get('EmailID')
        PhoneNumber = request.form.get('PhoneNumber')
        Status = request.form.get('Status')
        Password = request.form.get('Password')

        data = {
            'Name': str(Name),
            'RoleName': str(RoleName),
            'EmailID': str(EmailID),
            'PhoneNumber': str(PhoneNumber),
            'Status': str(Status),
            'Password': str(UserModel.generate_hash(Password))
        }

        current_user = UserModel.find_by_username(data['EmailID'])

        if not current_user:
            return {
                       'Data': "null",
                       'Message': 'User {} doesn\'t exist'.format(data['EmailID'])
                   }, 401



        Name=data['Name'] if data['Name'] != 'None' else current_user.Name
        RoleName=data['RoleName'] if data['RoleName'] != 'None' else current_user.RoleName
        EmailID=data['EmailID'] if data['EmailID'] != 'None' else current_user.EmailID
        PhoneNumber=data['PhoneNumber'] if data['PhoneNumber'] != 'None' else current_user.PhoneNumber
        Status=data['Status'] if data['Status'] != 'None' else current_user.Status
        Password = data['Password'] if data['Password'] != 'None' else current_user.Password

        try:
            UserModel.update_to_db(Name=Name, RoleName=RoleName, EmailID=EmailID, PhoneNumber=PhoneNumber, Status=Status, Password=Password)
            return {
                       'Data': "null",
                       'Message': "User details updated successfully"
                   }, 201
        except Exception as e:
            return {
                       'Data': "null",
                       'Message': str(e)
                   }, 500



class UserDelete(Resource):
    @jwt_required()
    def delete(self):
        EmailID = request.form.get('EmailID')

        data = {
            'EmailID': str(EmailID),
        }

        current_user = UserModel.find_by_username(data['EmailID'])

        if not current_user:
            return {
                       'Data': "null",
                       'Message': 'User {} doesn\'t exist'.format(data['EmailID'])
                   }, 401

        try:
            UserModel.delete_by_emailID(data['EmailID'])
            return {
                       'Data': "null",
                       'Message': '{} deleted'.format(EmailID)
                   }, 200

        except Exception as e:
                return {
                           'Data': "null",
                           'Message': str(e)
                       }, 500

class FeedList(Resource):
    @jwt_required()
    def get(self):

        RoleName = str(request.args.get('RoleName'))
        print(RoleName)
        try:
            if RoleName == "None":
                return {
                           'Data': "null",
                           'Message': "Data can't be accessed without specifying role name"
                       }, 200
            elif RoleName == "CEO":
                return FeedModel.find_by_RoleName("CEO")
            elif RoleName == "CIO":
                return FeedModel.find_by_RoleName("CIO")
        except Exception as e:
            return {
                       'Data': "null",
                       'Message': str(e)
                   }, 500


    @jwt_required()
    def post(self):
        AccessRole = request.form.get('AccessRole')
        Title = request.form.get('Title')
        Preview = request.form.get('Preview')
        Body = request.form.get('Body')
        Link = request.form.get('Link')
        Image = request.form.get('Image')
        Severity = request.form.get('Severity')
        Industry = request.form.get('Industry')
        Time = request.form.get('Time')
        Region = request.form.get('Region')
        Category = request.form.get('Category')

        data = {
            'AccessRole': str(AccessRole),
            'Title': str(Title),
            'Preview': str(Preview),
            'Body': str(Body),
            'Link': str(Link),
            'Image': str(Image),
            'Severity': str(Severity),
            'Industry': str(Industry),
            'Time': str(Time),
            'Region': str(Region),
            'Category': str(Category),
            '': str()
        }

        if FeedModel.find_by_Title(data['Title']):
            return {
                       'Data': "null",
                       'Message': "Feed already exists"
                   }, 409

        new_feed = FeedModel(
            AccessRole=data['AccessRole'],
            Title=data['Title'],
            Preview=data['Preview'],
            Body=data['Body'],
            Link=data['Link'],
            Image=data['Image'],
            Severity=data['Severity'],
            Industry=data['Industry'],
            Time=data['Time'],
            Region=data['Region'],
            Category=data['Category']
        )

        try:
            new_feed.save_to_db()
            return {
                       'Data': "null",
                       'Message': "Feed created successfully"
                   }, 201
        except Exception as e:
            return {
                       'Data': "null",
                       'Message': str(e)
                   }, 500


class FeedDetails(Resource):
    def get(self):
        FeedID = request.args.get('FeedID')

        data = {
            'FeedID': int(FeedID)
        }

        try:
            current_feed = FeedModel.find_by_feedId(data['FeedID'])

            if not current_feed:
                return {
                           'Data': "null",
                           'Message': 'Feed {} doesn\'t exist'.format(data['FeedID'])
                       }, 409
        except Exception as e:
            return {
                       'Data': "null",
                       'Message': str(e)
                   }, 500

        return {
            "Data" : {
                'FeedID': current_feed.FeedID,
                'AccessRole': current_feed.AccessRole,
                'Title': current_feed.Title,
                'Preview': current_feed.Preview,
                'Body': current_feed.Body,
                'Link': current_feed.Link,
                'Image': current_feed.Image,
                'Severity': current_feed.Severity,
                'Industry': current_feed.Industry,
                'Time': current_feed.Time,
                'Region': current_feed.Region,
                'Category': current_feed.Category
            },
            "Message" : "Feed details fetched"
        }, 200

