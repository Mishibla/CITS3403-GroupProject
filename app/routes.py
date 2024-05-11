from flask import flash,redirect, render_template,url_for,request
from flask_login import login_user
from app import app,db 
from app.forms import AdForm,RegisterForm,LoginForm
from app.models import User,Ad

#counter will be used for ad_id primary key


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
    return render_template("Sellpage.html")

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
        return redirect(url_for('homepage'))
    return render_template('loginpage.html', form=form, title='login')

@app.route('/logout')
def logout():
    return None

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
        
        account = User(username=form.username.data, name=form.display_name.data)
        account.set_password(form.password.data)  
        db.session.add(account)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("registeraccount.html", form=form)
    
@app.route('/account')
def account():
    return render_template("accountpage.html", title='Account')

@app.route('/createad')
def create():
    form = AdForm()
    return render_template("requestpage.html",form=form, title='Create ad')

@app.route('/submit-ad', methods=['GET', 'POST'])
def submit_ad():
    form = AdForm()
    type_of_game=form.games.data
    form.rank.choices=get_rank(type_of_game)
    form_data=[form.titlerequest.data,form.games.data,form.rank.data,form.price.data,form.skin.data,form.exclusive_skin.data,form.description.data]
    #user_count = Ad.query.count()
    #new_id=user_count+1
    try:
        float(form_data[3])==float
    except:
        flash('Enter price in valid format')
    length_title=len(form_data[0])
    length_description=len(form_data[-1])
    if length_title > 49:
        flash(f'Title is too long: max 49 characters, current length {length_title} characters')
    if length_description > 499:
        flash(f'Description is too long: max 499 characters, current length {length_description} characters')
    if not form.validate_on_submit():
        return render_template("requestpage.html",form=form)
    return redirect(location=url_for("account"))

csranks=['SILVER','GOLD NOVA','MASTER GUARDIAN','LEGENDARY']
owranks=['BRONZE','SILVER','GOLD','PLATNIUM','DIAMOND','MASTER','GRANDMASTER','CHAMPIONS','TOP500']
leagueranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
valranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','ASCENDANT','IMMORTAL','RADIANT']
gamesapp={'CSGO':csranks,'Overwatch':owranks,'League':leagueranks,'Valorant':valranks}
def get_rank(gametype):
    return(gamesapp.get(gametype))


'''        for field, errors in form.errors.items():
            for error in errors:
                print(f"Error in {field}: {error}")
                flash(f"Error in {field}: {error}")
        form.games.data=None'''


