from app import db

class User(db.Model):
    username=db.Column(db.String(100),primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    
    ads = db.relationship('Ad', backref='user', lazy='dynamic')
    def __repr__(self) -> str:
        return f'<{self.name} {self.username}>'

class Ad(db.Model):
    ad_id=db.Column(db.Integer, primary_key=True)
    ad_title=db.Column(db.String(100),nullable=False)
    user_username = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)
    def __repr__(self) -> str:
        return f'<{self.ad_id} {self.ad_title}>'
