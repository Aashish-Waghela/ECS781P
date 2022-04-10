import datetime
from flask import jsonify, request
from PavApi.Models.models import UserModel
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
                           'Password': current_user.Password,
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

class AllUsers(Resource):
    @jwt_required()
    def get(self):
        return jsonify(UserModel.return_all()), 200
    # @jwt_required
    # def get(self):
    #     return jsonify({
    #         'user_id': '1',
    #         'username': 'Chirag DK',
    #         'email_id': 'placeholder@email.com',
    #         'role': 'Auditor',
    #         'status': 'active',
    #         'access_token': 'access_token',
    #         'refresh_token': 'refresh_token',
    #         'message': 'Logged in as'
    #     }), 200

    def delete(self):
        return UserModel.delete_all()

class Task(Resource):
    @jwt_required()
    def get(self):

        duration = request.args.get('duration')

        data = {
            'duration':str(duration)
        }
        if data['duration'] == "today":
            return {
                "today": [
                    {
                        "clientid": "cm98",
                        "client-name": "maruthi",
                        "assignmentid": "as234",
                        "assignment-name": "bimal-audit",
                        "taskgroup-id": "tg765",
                        "taskgroup-name": "anshul's team",
                        "taskid": "t345",
                        "taskname": "bimal-showroom-audit",
                        "taskdate": "28-4-2020",
                        "taskstatus": "Not Started",
                        "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task",
                        "taskdetails": "Scan this car and check for Vin related documents"
                    },
                    {
                        "clientid": "cm99",
                        "client-name": "hyundai",
                        "assignmentid": "as334",
                        "assignment-name": "nexa-audit",
                        "taskgroup-id": "tg865",
                        "taskgroup-name": "mainak's team",
                        "taskid": "t355",
                        "taskname": "nexa-showroom-audit",
                        "taskdate": "28-4-2020",
                        "taskstatus": "In-Progress",
                        "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task",
                        "taskdetails": "Scan this car and comment on condition of car"
                    }
                ]
            }
        elif data['duration'] == "week":
            return {
                "week": {
                    "7-5-2020": [
                        {
                            "taskid": "t345",
                            "taskname": "bimal-showroom-audit",
                            "taskdate": "28-4-2020",
                            "taskstatus": "Not Started",
                            "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task"
                        },
                        {
                            "taskid": "t355",
                            "taskname": "nexa-showroom-audit",
                            "taskdate": "28-4-2020",
                            "taskstatus": "Started",
                            "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task. To Test if the expandable view is working."
                        },
                        {
                            "taskid": "t345",
                            "taskname": "bimal-showroom-audit",
                            "taskdate": "28-4-2020",
                            "taskstatus": "In Progress",
                            "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task"
                        },
                        {
                            "taskid": "t355",
                            "taskname": "nexa-showroom-audit",
                            "taskdate": "28-4-2020",
                            "taskstatus": "Completed",
                            "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task"
                        },
                        {
                            "taskid": "t355",
                            "taskname": "nexa-showroom-audit",
                            "taskdate": "28-4-2020",
                            "taskstatus": "Delayed",
                            "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task. To Test if the expandable view is working."
                        }
                    ],
                    "6-5-2020": [
                        {
                            "taskid": "t345",
                            "taskname": "bimal-showroom-audit",
                            "taskdate": "28-4-2020",
                            "taskstatus": "Not Started",
                            "taskdescription": "Short description for quick update. Description can be expanded and card when clicked, opens a detailed view of the task"
                        }
                    ]
                }
            }


class FeedList(Resource):
    def get(self):
        return {
            "Feed": [
                {
                    "id": "1",
                    "title": "Mask Up, Bangaluru",
                    "preview": "However, anybody who's been around town in the past few days would have noticed the casula attitude of most people...",
                    "link": "https://www.deccanherald.com/national/coronavirus-in-india-news-live-updates-total-cases-deaths-flights-trains-today-schedule-mumbai-delhi-kolkata-bengaluru-maharashtra-gujarat-west-bengal-tamil-nadu-covid-19-tracker-today-worldometer-update-lockdown-4-latest-news-838583.html",
                    "image": "https://inratiastorage.blob.core.windows.net/images/image(15).jpg",
                    "time": "7 hours ago",
                    "severity": "High",
                    "industry": "Energy"
                },
                {
                    "id": "2",
                    "title": "Start Flight Operation in Kolkata from May 30: Mamata Banerjee urges Centre",
                    "preview": "West Bengal Chief Minister Mamata Banerjee on Satirday appealed the Central Governemnt to defer flight operations ...",
                    "link": "https://www.deccanherald.com/business/business-news/stuff-ceo-buys-nz-media-company-from-australias-nine-for-61-cents-841575.html?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts",
                    "image": "https://inratiastorage.blob.core.windows.net/images/image(6).jpg",
                    "time": "3 days ago",
                    "severity": "Low",
                    "industry": "Energy"
                },
                {
                    "id": "3",
                    "title": "Start Flight Operation in Kolkata from May 30: Mamata Banerjee urges Centre",
                    "preview": "West Bengal Chief Minister Mamata Banerjee on Satirday appealed the Central Governemnt to defer flight operations ...",
                    "link": "https://zeenews.india.com/india/imd-predicts-heatwave-issued-red-alert-for-north-india-rains-likely-after-may-28-2285848.html?utm_campaign=fullarticle&utm_medium=referral&utm_source=inshorts",
                    "image": "https://inratiastorage.blob.core.windows.net/images/image(4).jpg",
                    "time": "23 days ago",
                    "severity": "Low",
                    "industry": "Energy"
                }
            ]
        }


class FeedDetails(Resource):
    def get(self):
        return {
            "id": "12345",
            "body": "First 100 characters of the body"
        }
