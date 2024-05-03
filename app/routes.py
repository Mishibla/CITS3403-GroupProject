from flask import render_template
from app import app
@app.route('/')
@app.route('/account')
def account():
    return render_template("accountpage.html")
csranks=['SILVER','GOLD NOVA','MASTER GUARDIAN','LEGENDARY']
owranks=['BRONZE','SILVER','GOLD','PLATNIUM','DIAMOND','MASTER','GRANDMASTER','CHAMPIONS','TOP500']
leagueranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','EMERALD','DIAMOND','MASTER','GRANDMASTER','CHALLENGER']
valranks=['IRON','BRONZE','SILVER','GOLD','PLATINUM','DIAMOND','ASCENDANT','IMMORTAL','RADIANT']
@app.route('/account/create')
def create():
    games={'CSGO':csranks,'Overwatch':owranks,'League':leagueranks,'Valorant':valranks}
    return render_template("requestpage.html")
