

from datetime import datetime
from zoneinfo import ZoneInfo
from app.models import User, Ad
from app import db

class AccountCreationError(Exception):
    pass

def create_account(all_data):
    unique_username = all_data[0]
    existing_user = User.query.filter_by(username=unique_username).first()
    if existing_user:
        raise AccountCreationError(f'{unique_username} has already been created, please enter a unique username')
    if len(unique_username) > 29:
        raise AccountCreationError(f'Username is too long: max 29 characters, current length {len(unique_username)} characters')
    if len(all_data[1]) > 29:
        raise AccountCreationError(f'Display name is too long: max 29 characters, current length {len(all_data[1])} characters')
    if len(all_data[2]) > 19:
        raise AccountCreationError(f'Password is too long: max 19 characters, current length {len(all_data[2])} characters')  
    
    account = User(username=all_data[0], name=all_data[1], email=all_data[3], phone=all_data[4])
    account.set_password(all_data[2])
    db.session.add(account)
    db.session.commit()

def create_user(username, name, password, email):
    user = User(username=username, name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(username):
    return User.query.get(username)
