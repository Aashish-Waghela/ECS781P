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
    def update_to_db(cls, Name, RoleName, EmailID, PhoneNumber, Status, Password):

        cls.query.filter_by(EmailID = EmailID).update({
            cls.Name : Name,
            cls.RoleName : RoleName,
            cls.EmailID : EmailID,
            cls.PhoneNumber : PhoneNumber,
            cls.Status : Status,
            cls.Password : Password,
        },
        synchronize_session = False)
        db.session.commit()

    @classmethod
    def find_by_username(cls, EmailID):
        return cls.query.filter_by(EmailID = EmailID).first()

    @classmethod
    def delete_by_emailID(cls, EmailID):

        cls.query.filter_by(EmailID = EmailID).delete()
        db.session.commit()


    @staticmethod
    def generate_hash(Password):
        return sha256.hash(Password)

    @staticmethod
    def verify_hash(Password, hash):
        return sha256.verify(Password, hash)

class FeedModel(db.Model):
    __tablename__ = 'Feed'

    FeedID = db.Column(db.Integer, primary_key=True)
    AccessRole = db.Column(db.String, nullable = True)
    Title = db.Column(db.String(200), unique=True, nullable=False)
    Preview = db.Column(db.String(), nullable = False)
    Body = db.Column(db.String(), nullable=False)
    Link = db.Column(db.String(), nullable=False)
    Image = db.Column(db.String(), nullable=False)
    Severity = db.Column(db.String(), nullable=False)
    Industry = db.Column(db.String(), nullable=False)
    Time = db.Column(db.String(), nullable=False)
    Region = db.Column(db.String(), nullable=False)
    Category = db.Column(db.String(), nullable=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_feedId(cls, FeedID):
        return cls.query.filter_by(FeedID = FeedID).first()

    @classmethod
    def find_by_feedTitle(cls, Title):
        return cls.query.filter_by(Title=Title).first()

    @classmethod
    def return_all(cls):
        def to_json(x):
            return {
            'FeedID' : x.FeedID,
            'AccessRole': x.AccessRole,
            'Title': x.Title,
            'Preview': x.Preview,
            'Body': x.Body,
            'Link': x.Link,
            'Image': x.Image,
            'Severity': x.Severity,
            'Industry': x.Industry,
            'Time': x.Time,
            'Region': x.Region,
            'Category': x.Category
            }
        return {'Data': list(map(lambda x: to_json(x), FeedModel.query.all())),
                'Message': "Feed list fetched"}
