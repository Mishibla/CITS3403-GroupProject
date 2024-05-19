from datetime import datetime
from zoneinfo import ZoneInfo
from flask import flash,redirect, render_template,url_for,request,send_from_directory, jsonify, Flask
from flask_login import login_user, logout_user, login_required, current_user
from app import db 
from app.forms import AdForm,RegisterForm,LoginForm, MessageForm
from app.models import User,Ad, Message
from app.controllers import AccountCreationError,create_account

from app.blueprints import main
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route('/')

@main.route('/homepage')
def homepage():
    return render_template("Homepage.html")


@main.route('/buyaccount')
def buyaccount():
    skins = request.args.get('skins')
    exclusive = request.args.get('exclusive')
    price_asc = request.args.get('price_asc')
    price_desc = request.args.get('price_desc')
    rank_asc = request.args.get('rank_asc')
    rank_desc = request.args.get('rank_desc')
    game_type = request.args.get('game_type')

    # Base query
    query = Ad.query

    # Apply filters based on checkboxes
    if skins:
        query = query.filter(Ad.skins == True)
    if exclusive:
        query = query.filter(Ad.exclusive == True)

    if price_asc and not price_desc:
        query = query.order_by(Ad.price.asc())
    if price_desc and not price_asc:
        query = query.order_by(Ad.price.desc())

    if rank_asc and not rank_desc:
        print(query)
        query = query.order_by(Ad._rankid.asc())
    if rank_desc and not rank_asc:
        query = query.order_by(Ad._rankid.desc())

    if game_type:
        query = query.filter(Ad.game_type == game_type)

    print(query)  # Debugging statement
    # Execute the query
    ad_data = query.all()

    return render_template("Sellpage.html", allads=ad_data, title='Buypage')

@main.route('/login', methods=['get','post'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('loginpage.html', form=form, title='login')
    if form.validate_on_submit():
        unique_username = form.log_username.data
        user = User.query.get(unique_username)
        if not user:
            flash(f'No user found with username {unique_username}', 'error')
            return render_template('loginpage.html', form=form, title='login')
        if not user.check_password(form.log_password.data):
            flash('Invalid password. Please try again.', 'error')
            return render_template('loginpage.html', form=form)
        login_user(user)
        print(login_user(user))
        return redirect(url_for('main.account'))
    return render_template('loginpage.html', form=form, title='login')

@main.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("main.homepage"))

@main.route('/register')
def register(): 
    form=RegisterForm()
    return render_template('registeraccount.html',form=form, title='register')

@main.route('/submit_register', methods=['GET', 'POST'])
def register_account():
    form = RegisterForm()
    all_data=[form.username.data,form.display_name.data, form.password.data,form.email.data,form.phone.data]
    if request.method == 'POST' and form.validate_on_submit():
        try:
            create_account(all_data)
        except AccountCreationError as e:
            flash(e, 'error')
            return render_template("registeraccount.html", form=form, title='Register Account')
        return redirect(url_for("main.login"))
    else:
        print(form.errors)
    return render_template("registeraccount.html", form=form, title='Register Account')
    
@main.route('/account')
@login_required
def account():
    userid = current_user.username
    user_details=User.query.get(userid)
    return render_template("accountpage.html", title='Account', user_details=user_details)

@main.route('/createad')
@login_required
def create():
    form = AdForm()
    return render_template("requestpage.html",form=form, title='Create ad')

@main.route('/submit-ad', methods=['GET', 'POST'])
def submit_ad():
    form = AdForm()
    type_of_game=form.games.data
    form.rank.choices=get_rank(type_of_game)
    form_data=[form.titlerequest.data,form.games.data,form.rank.data,form.price.data,form.skin.data,form.exclusive_skin.data,form.description.data]
    unsuccessful_submit = False
    try:
        float(form_data[3])==float
    except:
        flash('Enter price in valid format')
    length_title=len(form_data[0])
    length_description=len(form_data[-1])
    if length_description>499:
        flash(f'Description is too long: max 499 characters, current length {length_description} characters')
    if not form.validate_on_submit():
        unsuccessful_submit = True
        if form.skin.data=='No':
            form.skin.data=False
        print(form.skin.data)
        return render_template("requestpage.html",form=form, unsuccessful_submit=unsuccessful_submit, title='Requestpage')
    if 'images' in request.files:
        images = request.files.getlist('images')
    try:
        last_ad_id = Ad.query.with_entities(Ad.ad_id).order_by(Ad.ad_id.desc()).first()[0] + 1
    except:
        last_ad_id = 1
    ad_folder = os.path.join('app', 'static', 'uploads', str(last_ad_id))  # Using last_ad_id as the folder name
    os.makedirs(ad_folder, exist_ok=True)
    for i, image in enumerate(images):
            if image.filename == '':
                continue
            if image and allowed_file(image.filename):
                extension = image.filename.rsplit('.', 1)[1].lower()
                filename = f'{last_ad_id}_{i + 1}.{extension}'
                image_path = os.path.join(ad_folder, filename)
                image.save(image_path)
    if current_user.is_authenticated:
        user = current_user.username
    try:
        last_ad_id = Ad.query.with_entities(Ad.ad_id).order_by(Ad.ad_id.desc()).first()[0]+1
    except:
        last_ad_id=1
    new_ad=Ad(ad_id=last_ad_id, ad_title=form_data[0],game_type=form_data[1], game_rank=form_data[2], price=form_data[3],skins=bool(form_data[4]), exclusive=form_data[5], Extra_Descrip=form_data[6], user_username=user, created_at=datetime.now(ZoneInfo('Asia/Shanghai')), image_folder=str(last_ad_id))
    db.session.add(new_ad)
    db.session.commit()
    return redirect(f'/ads/{last_ad_id}')


@main.route('/ads/<int:ad_id>')
def show_ad(ad_id):
    print('Entering show_ad function', flush=True)
    form = MessageForm()
    displayedit=False
    displaydelete=False
    button_change=False
    ad_details = Ad.query.get(ad_id)
    ownerid= ad_details.user_username
    if not current_user.is_authenticated:
        return render_template('adtemplate.html', ad=ad_details, success=button_change, title='Ad')
    if current_user.is_authenticated:
        userid = current_user.username
    user = User.query.get(userid)
    wish=user.wishlist
    if ownerid== userid:
        displaydelete=True
        displayedit=True
    if wish==None:
        button_change=False
    elif str(ad_id)==wish:
        button_change=True
    else:
        wishlist_ids = str(wish).split(',')
        if str(ad_id) in wishlist_ids:
                button_change = True
    return render_template('adtemplate.html', ad=ad_details, success=button_change, displaydelete=displaydelete, displayedit=displayedit, form=form, title='Ad')



@main.route('/submit-wishlist',  methods=['GET', 'POST'])
@login_required
def adlike():
    ad_id = request.form['ad_id']
    userid=current_user.username
    print(ad_id)
    print(userid)
    if not current_user.is_authenticated:
        flash('You must be logged in to add or remove to wishlist.', 'error')
        return redirect(f'/ads/{ad_id}')
    if current_user.is_authenticated:
        user = User.query.get(userid)
        print(user)
        current_wishlist=user.wishlist

        if current_wishlist == None:
            user.wishlist=str(ad_id)
        elif str(ad_id) in str(current_wishlist).split(','):
            numbers_str=str(ad_id)
            numbers_list = numbers_str.split(',')

            filtered_numbers = [num for num in numbers_list if num != str(ad_id)]

            if filtered_numbers:
                user.wishlist = ','.join(filtered_numbers)
            else:
                user.wishlist = None 
        else:
            update_wishlist=str(current_wishlist)+','+str(ad_id)
            update_wishlist = update_wishlist.replace(" ", "")
            noduplicate=set(update_wishlist.split(','))
            my_string = ', '.join(f"{item}" for item in noduplicate)
            my_string = my_string.replace(" ", "")
            print(my_string)
            user.wishlist=my_string

        db.session.commit()

        return redirect(f'/ads/{ad_id}')

    return redirect(f'/ads/{ad_id}')

@main.route('/submit-deletead',  methods=['GET', 'POST'])
def deletead():
    ad_id = request.form['ad_id']
    userid=request.form['user']
    current_ad=Ad.query.get(ad_id)
    db.session.delete(current_ad)
    db.session.commit()
    flash('Ad deleted successfully!', 'success')
    return redirect(url_for('main.manageads'))

@main.route('/submit-editad/<int:ad_id>', methods=['GET', 'POST'])
@login_required
def edit_ad(ad_id):
    print(ad_id)
    ad = Ad.query.get(ad_id)
    form = AdForm()
    type_of_game=ad.game_type
    form.rank.choices=get_rank(type_of_game)
    form.skin.data= str(ad.skins)
    print(form.data)
    if request.method == 'POST':
        try:
            float(form.price.data)==float
        except:
            flash('Enter price in valid format')
        length_description=len(form.description.data)
        if length_description>499:
            flash(f'Description is too long: max 499 characters, current length {length_description} characters')
        if form.validate_on_submit():
            print("Form validated successfully")
            ad.ad_title = form.titlerequest.data
            ad.game_type = form.games.data
            ad.game_rank = form.rank.data
            ad.price = form.price.data
            ad.skins = bool(form.skin.data)
            ad.exclusive = form.exclusive_skin.data
            ad.Extra_Descrip = form.description.data
            print(ad.price)
            db.session.commit()
            flash('Ad updated successfully!', 'success')
            return redirect(url_for('main.show_ad', ad_id=ad.ad_id))
        else:
            print("Form validation failed")
            print(f"Form errors: {form.errors}")
            flash(f"Form validation failed: {form.errors}", 'danger')
    else:
        type_of_game=ad.game_type
        form.rank.choices=get_rank(type_of_game)
        form.titlerequest.data = ad.ad_title
        form.games.data=ad.game_type
        form.rank.data=ad.game_rank
        form.price.data= ad.price
        form.skin.data= str(ad.skins)
        form.exclusive_skin.data= ad.exclusive
        form.description.data= ad.Extra_Descrip
    
    return render_template("editad.html", form=form, title='Edit Ad', ad=ad, unsuccessful_submit=True)

@main.route('/wishlist')
@login_required
def wishlist():
    if current_user.is_authenticated:
        user = current_user.username
        user_details = User.query.get(user)
        wish = user_details.wishlist

        if wish:
            # Ensure wish is a string before splitting
            if isinstance(wish, int):
                wish = str(wish)

            # Convert the comma-separated string to a list of ad_ids
            ad_ids = wish.split(',')

            # Query the Ad table to get ads with those ad_ids
            ad_data = Ad.query.filter(Ad.ad_id.in_(ad_ids)).all()
        else:
            ad_data = []

        return render_template('wishlist.html', title='Wishlist', ad_data=ad_data)
    return redirect(url_for('main.login'))

@main.route('/manageads')
@login_required
def manageads():
    if current_user.is_authenticated:
        user = current_user.username

        query = Ad.query
        query = query.filter(Ad.user_username == user)

        ad_data = query.all()
        return render_template("manageads.html", title='Manage Ads', ad_data=ad_data)
    return redirect(url_for('main.login'))

@main.route('/submit-editad/<username>', methods=['GET', 'POST'])
@login_required
def edit_account(username):
    print(username)
    user_details = User.query.get(username)
    if not user_details:
        flash(f'User {username} not found.', 'danger')
        return redirect(url_for('main.account'))
        
    form = RegisterForm()
    print(form.data)

    if request.method == 'POST':
        print('Form has been posted')
        if len(form.display_name.data) > 29:
            flash(f'Display name is too long: max 29 characters, current length {len(form.display_name.data)} characters', 'error')
        if len(form.password.data) > 19:
            flash(f'Password is too long: max 19 characters, current length {len(form.password.data)} characters', 'error')
        if form.validate_on_submit():
            print('Form validated successfully')
            user_details.name = form.display_name.data
            user_details.set_password(form.password.data)
            user_details.email = form.email.data
            user_details.phone = form.phone.data
            db.session.commit()
            flash('Account updated successfully!', 'success')
            return redirect(url_for('main.account'))
        else:
            print("Form validation failed")
            print(f"Form errors: {form.errors}")
            flash(f"Form validation failed: {form.errors}", 'danger')
    else:
        form.username.data = user_details.username
        form.display_name.data = user_details.name
        form.email.data = user_details.email
        form.phone.data = user_details.phone

    return render_template("editaccount.html", form=form, title='Edit account', user_details=user_details)

@main.route('/submit-message',methods=['GET', 'POST'])
@login_required
def submit_message():
    ad_id = request.form['ad_id']
    print(ad_id)
    userid=request.form['user']
    print(userid)
    try:
        last_message_id = Message.query.with_entities(Message.message_id).order_by(Message.message_id.desc()).first()[0]+1
    except:
        last_message_id=1
    form = MessageForm()
    if len(form.message.data)>50:
        flash(f'Message is too long: max 50 characters, current length {len(form.message.data)} characters')
    if form.validate_on_submit():
        new_message=Message(message_id=last_message_id, id_ad=ad_id, user_interested=userid, message=form.message.data, created_message=datetime.now(ZoneInfo('Asia/Shanghai')))
        print(new_message)
        db.session.add(new_message)
        db.session.commit()
    else:
        print("Form validation failed")
        print(f"Form errors: {form.errors}")
        flash(f"Form validation failed: {form.errors}", 'danger')
    flash('Message sent successfully')
    return redirect(f'/ads/{ad_id}')

@main.route('/messageinbox')
@login_required
def messageinbox():
    userid = current_user.username
    userinfo=User.query.get(userid)
    owner_ad=[str(ad.ad_id) for ad in userinfo.ads.all()]
    message_data=Message.query.all()
    combined=[]
    for mess in message_data:
        if str(mess.id_ad) in owner_ad:
            interest_ad=mess.id_ad
            urlad=f'/ads/{str(interest_ad)}'
            title= Ad.query.get(interest_ad).ad_title
            interestmessage=mess.message
            interestdate= mess.created_message

            userinterest=mess.user_interested
            user_deets=User.query.get(userinterest)
            name_user= user_deets.name
            email_user= user_deets.email
            phone_user= user_deets.phone

            combined.append([urlad,title,interestmessage,interestdate, name_user, email_user, phone_user])
    print(combined)
    return render_template('messageinbox.html', data=combined,title='Messages')




csranks=['SILVER','GOLD NOVA','MASTER GUARDIAN','LEGENDARY']
owranks=['BRONZE','SILVER','GOLD','PLATNIUM','DIAMOND','MASTER','GRANDMASTER','CHAMPIONS','TOP500']
leagueranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
valranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','ASCENDANT','IMMORTAL','RADIANT']
gamesapp={'CSGO':csranks,'Overwatch':owranks,'League':leagueranks,'Valorant':valranks}
def get_rank(gametype):
    return(gamesapp.get(gametype))





