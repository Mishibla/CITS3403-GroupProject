from datetime import datetime
from zoneinfo import ZoneInfo
from flask import flash,redirect, render_template,url_for,request
from flask_login import login_user, logout_user, login_required, current_user
from app import app,db 
from app.forms import AdForm,RegisterForm,LoginForm
from app.models import User,Ad
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_foldername():
    i = 1
    while True:
        filename = f"ad{i}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.exists(filepath):
            return filepath
        i += 1
@app.route('/')

#test root to see if the database is working
#@app.route('/titleofad')
#def titleofad():
    #ads_of_chris = Ad.query.all() 
    #print("Hello World")
    #print(ads_of_chris)
    #tests=ads_of_chris)
    #return render_template("adtemplate.html",ad=ads_of_chris)

@app.route('/homepage')
def homepage():
    return render_template("Homepage.html")

@app.route('/buyaccount')
def buyaccount():
    ad_data=Ad.query.all()
    urllist={}
    for indvidual_ad in ad_data:
        ads=indvidual_ad.ad_id
        urlstring='/ads/'+str(ads)
        urllist[ads]=urlstring
    #print(urllist, ad=ads)
    titlelist=[]
    for title in ad_data:
        titlelist.append(title.ad_title)
    return render_template("Sellpage.html",ad=urllist, alltitles=titlelist)

@app.route('/login', methods=['get','post'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('loginpage.html', form=form)
    if form.validate_on_submit():
        unique_username = form.log_username.data
        user = User.query.get(unique_username)
        if not user:
            flash(f'No user found with username {unique_username}', 'error')
            return render_template('loginpage.html', form=form)
        if not user.check_password(form.log_password.data):
            flash('Invalid password. Please try again.', 'error')
            return render_template('loginpage.html', form=form)
        login_user(user)
        print(login_user(user))
        return redirect(url_for('account'))
    return render_template('loginpage.html', form=form, title='login')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("homepage"))

@app.route('/register')
def register(): 
    form=RegisterForm()
    return render_template('registeraccount.html',form=form, title='register')

@app.route('/submit_register', methods=['GET', 'POST'])
def register_account():
    form = RegisterForm()
    if request.method == 'POST':
        unique_username = form.username.data
        if User.query.get(unique_username):
            flash(f'{unique_username} has already been created, please enter a unique username', 'error')
            return render_template('registeraccount.html', form=form)

        if len(form.username.data) > 29:
            flash(f'Username is too long: max 29 characters, current length {len(form.username.data)} characters', 'error')
        if len(form.display_name.data) > 29:
            flash(f'Display name is too long: max 29 characters, current length {len(form.display_name.data)} characters', 'error')
        if len(form.password.data) > 19:
            flash(f'Password is too long: max 19 characters, current length {len(form.password.data)} characters', 'error')
        
        if not form.validate_on_submit():
            return render_template("registeraccount.html", form=form)
        
        account = User(username=form.username.data, name=form.display_name.data, email=form.email.data, phone=form.phone.data)
        account.set_password(form.password.data)  
        db.session.add(account)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("registeraccount.html", form=form)
    
@app.route('/account')
@login_required
def account():
    userid = current_user.username
    user_details=User.query.get(userid)
    return render_template("accountpage.html", title='Account', user_details=user_details)

@app.route('/createad')
@login_required
def create():
    form = AdForm()
    return render_template("requestpage.html",form=form, title='Create ad')

@app.route('/submit-ad', methods=['GET', 'POST'])
def submit_ad():
    form = AdForm()
    type_of_game = form.games.data
    form.rank.choices = get_rank(type_of_game)
    form_data = [
        form.titlerequest.data,
        form.games.data,
        form.rank.data,
        form.price.data,
        form.skin.data,
        form.exclusive_skin.data,
        form.description.data
    ]
    unsuccessful_submit = False
    try:
        float(form_data[3]) == float
    except:
        flash('Enter price in valid format')
    length_title = len(form_data[0])
    length_description = len(form_data[-1])
    if length_description > 499:
        flash(f'Description is too long: max 499 characters, current length {length_description} characters')
    if not form.validate_on_submit():
        unsuccessful_submit = True
        if form.skin.data == 'No':
            form.skin.data = False
        print(form.skin.data)
        return render_template("requestpage.html", form=form, unsuccessful_submit=unsuccessful_submit)
    
    # Handling file uploads
    if 'images' in request.files:
        images = request.files.getlist('images')
        ad_folder = generate_unique_foldername()
        os.makedirs(ad_folder, exist_ok=True)
        for image in images:
            if image.filename == '':
             continue
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(ad_folder, filename)
                image.save(image_path)
                form_data.append(os.path.join(ad_folder.split('/')[-1], filename))  # Storing relative path to the image
            else:
                flash('Invalid file type')
                return redirect(request.url)

    if current_user.is_authenticated:
        user = current_user.username
    try:
        last_ad_id = Ad.query.with_entities(Ad.ad_id).order_by(Ad.ad_id.desc()).first()[0] + 1
    except:
        last_ad_id = 1
    new_ad = Ad(
        ad_id=last_ad_id,
        ad_title=form_data[0],
        game_type=form_data[1],
        game_rank=form_data[2],
        price=form_data[3],
        skins=bool(form_data[4]),
        exclusive=form_data[5],
        Extra_Descrip=form_data[6],
        user_username=user,
        created_at=datetime.now(ZoneInfo('Asia/Shanghai'))
    )
    print(new_ad)
    db.session.add(new_ad)
    db.session.commit()
    return redirect(f'/ads/{last_ad_id}')

@app.route('/ad-images/<ad_folder>')
def get_first_ad_image(ad_folder):
    UPLOADS_PATH = 'static/uploads'  

    
    if not ad_folder or '..' in ad_folder:
        abort(404)

    ad_folder_path = os.path.join(UPLOADS_PATH, ad_folder)
    if not os.path.isdir(ad_folder_path):
        abort(404)

    # Get the list of files in the ad folder
    files = os.listdir(ad_folder_path)

    # Find the first image file 
    for filename in files:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return send_from_directory(ad_folder_path, filename)

    # If no image file is found, return a default image or handle the situation as needed
    abort(404)

#<img src="/ad-images/ad1"> will call on the first image in that folder for use


@app.route('/ads/<int:ad_id>')
def show_ad(ad_id):
    displayedit=False
    displaydelete=False
    button_change=False
    ad_details = Ad.query.get(ad_id)
    ownerid= ad_details.user_username
    if not current_user.is_authenticated:
        return render_template('adtemplate.html', ad=ad_details, success=button_change)
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
        wishlist_ids = wish.split(',')
        if str(ad_id) in wishlist_ids:
                button_change = True
     # Fetching image filenames from the ad folder
    image_folder = ad_details.image_folder
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_folder)
    ad_images = os.listdir(image_path)
    
    print(ad_details)
    print(ad_details.ad_id)
    return render_template('adtemplate.html', ad=ad_details, success=button_change, displaydelete=displaydelete, displayedit=displayedit, ad_images=ad_images)



@app.route('/submit-wishlist',  methods=['GET', 'POST'])
@login_required
def adlike():
    ad_id = request.form['ad_id']
    userid=request.form['user']
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
        elif str(ad_id) in current_wishlist.split(','):
            numbers_str=str(ad_id)
            numbers_list = numbers_str.split(',')

            filtered_numbers = [num for num in numbers_list if num != str(ad_id)]

            if filtered_numbers:
                user.wishlist = ','.join(filtered_numbers)
            else:
                user.wishlist = None 
        else:
            update_wishlist=current_wishlist+','+str(ad_id)
            update_wishlist = update_wishlist.replace(" ", "")
            noduplicate=set(update_wishlist.split(','))
            my_string = ', '.join(f"{item}" for item in noduplicate)
            my_string = my_string.replace(" ", "")
            print(my_string)
            user.wishlist=my_string

        db.session.commit()

        return redirect(f'/ads/{ad_id}')

    return redirect(f'/ads/{ad_id}')

@app.route('/submit-deletead',  methods=['GET', 'POST'])
def deletead():
    ad_id = request.form['ad_id']
    print(ad_id)
    userid=request.form['user']
    current_ad=Ad.query.get(ad_id)
    db.session.delete(current_ad)
    db.session.commit()
    flash('Ad deleted successfully!', 'success')
    return redirect(url_for('manageads'))

@app.route('/submit-editad/<int:ad_id>', methods=['GET', 'POST'])
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
            return redirect(url_for('show_ad', ad_id=ad.ad_id))
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

@app.route('/wishlist')
@login_required
def wishlist():
    if current_user.is_authenticated:
        user = current_user.username
        user_details= User.query.get(user)
        wish= user_details.wishlist
        urllist={}
        if wish==None:
            urllist=False
        else:
            for ad in wish.split(','):
                urlstring='/ads/'+ad
                urllist[ad]=urlstring
    return render_template('wishlist.html', wishes=urllist, title='Wishlist')

@app.route('/manageads')
@login_required
def manageads():
    if current_user.is_authenticated:
        urllist={}
        user = current_user.username
        user_details= User.query.get(user)
        ads=user_details.get_ad_ids_str()
        if ads==None:
            urllist=False
        else:
            for ad in list(ads):
                urlstring='/ads/'+ad
                urllist[ad]=urlstring
    return render_template("manageads.html", title='Manage Ads', ad=urllist)


@app.route('/submit-editad/<username>', methods=['GET', 'POST'])
@login_required
def edit_account(username):
    print(username)
    user_details = User.query.get(username)
    if not user_details:
        flash(f'User {username} not found.', 'danger')
        return redirect(url_for('account'))
        
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
            return redirect(url_for('account'))
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



csranks=['SILVER','GOLD NOVA','MASTER GUARDIAN','LEGENDARY']
owranks=['BRONZE','SILVER','GOLD','PLATNIUM','DIAMOND','MASTER','GRANDMASTER','CHAMPIONS','TOP500']
leagueranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
valranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','ASCENDANT','IMMORTAL','RADIANT']
gamesapp={'CSGO':csranks,'Overwatch':owranks,'League':leagueranks,'Valorant':valranks}
def get_rank(gametype):
    return(gamesapp.get(gametype))



