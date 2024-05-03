from flask import render_template
from app import app
@app.route('/')
@app.route('/account')
def account():
    return render_template("accountpage.html")

@app.route('/account/create')
def create():
    return render_template("requestpage.html")
