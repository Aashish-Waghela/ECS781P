from PavApi import db
from passlib.hash import pbkdf2_sha256 as sha256

class UserModel(db.Model):
    __tablename__ = 'Users'

    UserID = db.Column(db.Integer, primary_key = True)
    Name = db.Column(db.String(120), nullable = False)
    RoleName = db.Column(db.String(120), nullable = False)
    EmailID = db.Column(db.String(120), unique=True, nullable=False)
    PhoneNumber = db.Column(db.String(120), nullable=False)
    Status = db.Column(db.String(120), nullable=False)
    Password = db.Column(db.String(120), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, EmailID):
        return cls.query.filter_by(EmailID = EmailID).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
            'Name': x.Name,
            'RoleName': x.RoleName,
            'EmailID': x.EmailID,
            'PhoneNumber': x.PhoneNumber,
            'Status': x.Status,
            'Password': x.Password
            }
        return {'users': list(map(lambda x: to_json(x), UserModel.query.all()))}

    @classmethod
    def delete_all(cls):
        try:
            num_rows_deleted = db.session.query(cls).delete()
            db.session.commit()
            return {
                'Data': "null",
                'Message': '{} row(s) deleted'.format(num_rows_deleted)
            }
        except:
            return {
                'Data': "null",
                'Message': 'Something went wrong'
            }

    @staticmethod
    def generate_hash(Password):
        return sha256.hash(Password)

    @staticmethod
    def verify_hash(Password, hash):
        return sha256.verify(Password, hash)
