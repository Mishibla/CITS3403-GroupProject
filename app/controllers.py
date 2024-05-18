

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

class AdCreationError(Exception):
    pass

def create_ad(data, user):
    try:
        price = float(data[3])
    except ValueError:
        raise AdCreationError('Enter price in valid format')

    length_description = len(data[-1])
    if length_description > 499:
        raise AdCreationError(f'Description is too long: max 499 characters, current length {length_description} characters')

    last_ad_id = db.session.query(db.func.max(Ad.ad_id)).scalar()
    if last_ad_id is None:
        last_ad_id = 1
    else:
        last_ad_id += 1

    new_ad = Ad(
        ad_id=last_ad_id, 
        ad_title=data[0],
        game_type=data[1], 
        game_rank=data[2], 
        price=price,
        skins=bool(data[4]), 
        exclusive=bool(data[5]), 
        Extra_Descrip=data[6], 
        user_username=user, 
        created_at=datetime.now(ZoneInfo('Asia/Shanghai'))
    )
    db.session.add(new_ad)
    db.session.commit()
    return last_ad_id


def create_user(username, name, password, email):
    user = User(username=username, name=name, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return user

def get_user(username):
    return User.query.get(username)
