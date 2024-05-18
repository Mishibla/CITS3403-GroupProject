

from app.models import User, Ad
from app import db

class AccountCreationError(Exception):
    pass

def create_account(form):
    unique_username = form.username.data
    existing_user = User.query.filter_by(username=unique_username).first()
    if existing_user:
        raise AccountCreationError(f'{unique_username} has already been created, please enter a unique username')
    if len(form.username.data) > 29:
        raise AccountCreationError(f'Username is too long: max 29 characters, current length {len(form.username.data)} characters')
    if len(form.display_name.data) > 29:
        raise AccountCreationError(f'Display name is too long: max 29 characters, current length {len(form.display_name.data)} characters')
    if len(form.password.data) > 19:
        raise AccountCreationError(f'Password is too long: max 19 characters, current length {len(form.password.data)} characters')  
    
    account = User(username=form.username.data, name=form.display_name.data, email=form.email.data, phone=form.phone.data)
    account.set_password(form.password.data)
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
