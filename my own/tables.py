from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
#=========================== Admin Schema =====================================

class Admin_Sign_Up(db.Model):
    __tablename__ = "admin_sign_up"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name = db.Column(db.String,nullable=False,unique=True)
    email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False,unique=True)
    security_key=db.Column(db.String,nullable=True,unique=True)

class User_Sign_Up(db.Model):
    __tablename__ = "user_sign_up"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    user_name = db.Column(db.String,nullable=False,unique=True)
    email=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False,unique=True)
    role=db.Column(db.String,nullable=False,unique=False)
    industry=db.Column(db.String,nullable=True,unique=False)
    security_key=db.Column(db.String,nullable=True,unique=True)

class Camp(db.Model):   # model for storing camps created by sponsors
    __tablename__ = "camp"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String,nullable=False,unique=False)
    camp_name=db.Column(db.String,nullable=False,unique=False)
    camp_details=db.Column(db.String,nullable=False,unique=False)
    price=db.Column(db.String,nullable=False,unique=False)
    start_date=db.Column(db.String,nullable=True,unique=False)
    end_date=db.Column(db.String,nullable=True,unique=False)
    category=db.Column(db.String,nullable=False,unique=False)
    expected_followers=db.Column(db.String,nullable=False,unique=False)
    expected_reach=db.Column(db.String,nullable=False,unique=False)

class Influ_Camp(db.Model):  # model for storing camps selected by influencers
    __tablename__ = "influ_camp"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    camp_id=db.Column(db.Integer,nullable=False,unique=False)
    username = db.Column(db.String,nullable=False,unique=False)
    spon_username=db.Column(db.String,nullable=False,unique=False)
    camp_name=db.Column(db.String,nullable=False,unique=False)
    camp_details=db.Column(db.String,nullable=False,unique=False)
    price=db.Column(db.String,nullable=False,unique=False)
    start_date=db.Column(db.String,nullable=True,unique=False)
    end_date=db.Column(db.String,nullable=True,unique=False)
    category=db.Column(db.String,nullable=False,unique=False)
    expected_followers=db.Column(db.String,nullable=True,unique=False)
    expected_reach=db.Column(db.String,nullable=True,unique=False)

class Message(db.Model):
    __tablename__ = "message"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    sender=db.Column(db.String,nullable=False,unique=False) #username or id of the sender 
    recipient=db.Column(db.String,nullable=False,unique=False)  #username or id of the recepient
    content=db.Column(db.String,nullable=False,unique=False)

class SponMessage(db.Model):
    __tablename__ = "sponmessage"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    sender=db.Column(db.String,nullable=False,unique=False) #username or id of the sender 
    recipient=db.Column(db.String,nullable=False,unique=False)  #username or id of the recepient
    content=db.Column(db.String,nullable=False,unique=False)

class Influencer_Like(db.Model): #model for storing Influencer Preferences 
    __tablename__ = "influencer_like"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String,nullable=False,unique=False)
    niche=db.Column(db.String,nullable=False,unique=False) 
    reach=db.Column(db.String,nullable=False,unique=False)
    followers=db.Column(db.String,nullable=False,unique=False)
    motto=db.Column(db.String,nullable=False,unique=False)
    exp=db.Column(db.String,nullable=False,unique=False)

class Ad(db.Model):   # model for storing ads created by sponsors
    __tablename__ = "ad"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String,nullable=False,unique=False)
    ad_name=db.Column(db.String,nullable=False,unique=False)
    camp_name=db.Column(db.String,nullable=False,unique=False)
    ad_details=db.Column(db.String,nullable=False,unique=False)
    ad_aud=db.Column(db.String,nullable=False,unique=False)
    ad_price=db.Column(db.String,nullable=False,unique=False)
    ad_duration=db.Column(db.String,nullable=False,unique=False)

class F_Ad(db.Model):  # model for storing all flagged ads
    __tablename__ = "f_ad"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String,nullable=False,unique=False)
    ad_name=db.Column(db.String,nullable=False,unique=False)
    camp_name=db.Column(db.String,nullable=False,unique=False)
    ad_details=db.Column(db.String,nullable=False,unique=False)
    ad_aud=db.Column(db.String,nullable=False,unique=False)
    ad_price=db.Column(db.String,nullable=False,unique=False)
    ad_duration=db.Column(db.String,nullable=False,unique=False)

class F_Camp(db.Model):   # model for storing all flagged camps
    __tablename__ = "f_camp"
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String,nullable=False,unique=False)
    camp_name=db.Column(db.String,nullable=False,unique=False)
    camp_details=db.Column(db.String,nullable=False,unique=False)
    price=db.Column(db.String,nullable=False,unique=False)
    start_date=db.Column(db.String,nullable=True,unique=False)
    end_date=db.Column(db.String,nullable=True,unique=False)
    category=db.Column(db.String,nullable=False,unique=False)
    expected_followers=db.Column(db.String,nullable=False,unique=False)
    expected_reach=db.Column(db.String,nullable=False,unique=False)