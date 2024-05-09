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
    game_type=db.Column(db.String(100),nullable=False)
    game_rank=db.Column(db.String(100),nullable=False)
    price=db.Column(db.Float,nullable=False)
    skins=db.Column(db.Boolean, default=False, nullable=False)
    exclusive=db.Column(db.Boolean,default=False,nullable=False)
    Extra_Descrip=db.Column(db.String,nullable=True)
    

    user_username = db.Column(db.String(100), db.ForeignKey('user.username'), nullable=False)
    def __repr__(self) -> str:
        return f'<{self.ad_id} {self.ad_title}{self.game_type}{self.game_rank}{self.price}{self.skins}{self.exclusive}{self.Extra_Descrip}>'
