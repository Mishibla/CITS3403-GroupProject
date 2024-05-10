from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class User(db.Model,UserMixin):
    username=db.Column(db.String(100),primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    password_hash=db.Column(db.String(100),nullable=False)
    
    ads = db.relationship('Ad', backref='user', lazy='dynamic')
    def __repr__(self) -> str:
        return f'<{self.name} {self.username} {self.password_hash}>'
    def set_password(self, password):
        self.password_hash= generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def get_id(self):
        return self.username

@login.user_loader
def get_user(id):
    return User.query.get(id)

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
