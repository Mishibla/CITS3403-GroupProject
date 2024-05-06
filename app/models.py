from app import db

class User(db.Model):
    username=db.Column(db.String(100),primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    
    ad_id = db.Column(db.Integer, db.ForeignKey('ad.ad_id'), nullable=True)

    ad=db.relationship('Ad',back_populates='user_name')

class Ad(db.Model):
    ad_id=db.Column(db.Integer, primary_key=True)
    ad_title=db.Column(db.String(100),nullable=False)

    user_name=db.relationship(User,back_populates='ad')
