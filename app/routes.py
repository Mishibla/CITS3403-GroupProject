from flask import redirect, render_template,url_for
from app import app 
from app.forms import AdForm
from app.models import User,Ad
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
@app.route('/account')
def account():
    return render_template("accountpage.html")

@app.route('/account/create')
def create():
    form = AdForm()
    return render_template("requestpage.html",form=form)

# Use this form in your route
@app.route('/submit', methods=['GET', 'POST'])
def submit_ad():
    form = AdForm()
    #if form.validate_on_submit():
        # Process the form data, e.g., save to database
        #return redirect(url_for('success_page'))
    return render_template('accountpage.html', form=form)

'''
@app.route('/submit', methods=['POST', 'GET'])
def submit():
    return redirect(url_for('account'))'''





