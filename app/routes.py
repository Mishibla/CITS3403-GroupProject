from flask import flash,redirect, render_template,url_for
from app import app,db 
from app.forms import AdForm,RegisterForm
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

@app.route('/signin')
def signin():
    return render_template('loginpage.html')

@app.route('/register')
def register():
    form=RegisterForm()
    return render_template('registeraccount.html',form=form)

@app.route('/submit_register', methods=['GET', 'POST'])
def register_account():
    form = RegisterForm()
    if not form.validate_on_submit():
        return render_template("registeraccount.html",form=form)
    return redirect(location=url_for("signin"))
    
@app.route('/account')
def account():
    return render_template("accountpage.html")

@app.route('/account/create')
def create():
    form = AdForm()
    return render_template("requestpage.html",form=form)


@app.route('/submit-ad', methods=['GET', 'POST'])
def submit_ad():
    form = AdForm()
    type_of_game=form.games.data
    form.rank.choices=get_rank(type_of_game)
    form_data=[form.titlerequest.data,form.games.data,form.rank.data,form.price.data,form.skin.data,form.exclusive_skin.data,form.description.data]
    print(form_data)
    user_count = Ad.query.count()
    new_id=user_count+1
    print(new_id)
    try:
        float(form_data[3])==float
    except:
        flash('Enter price in valid format')
    length_title=len(form_data[0])
    length_description=len(form_data[-1])
    if len(form_data[0]) > 49:
        length_title = len(form_data[0])
        flash(f'Title is too long: max 49 characters, current length {length_title} characters')
    if len(form_data[-1]) > 499:
        length_description = len(form_data[-1])
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


