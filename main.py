from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import json
import requests

app = Flask(__name__)
app.secret_key = "FitRiseGym"

db = TinyDB('stranke.json')
users = db.table('uporabniki')
User = Query()
table=db.table('Tabela')
uids = []
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Register', methods=['POST'])
def Register():

    Ime = request.form["username"]
    Geslo = request.form["password"]
    Uid = request.form["uid"]

@app.route("/Login", methods=["POST"])
def Login():
    
    Ime = request.form["username"]
    Geslo = request.form["password"]
    try:
        with open("stranke.json") as y:
            value = json.load(y)
    except json.JSONDecodeError:
        value = {"Tabela": {}}
    if any(x["Name"] == Ime for x in value["Tabela"].values()):
        for x in value["Tabela"].values():
            if x["Name"] == Ime and x["Password"] == Geslo:
                session['username'] = Ime
                return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Napačno geslo'})
    elif Ime == "admin" and Geslo == "admin":
        session['username'] = "admin"
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Uporabnik ne obstaja'})

@app.route('/panel')
def apanel():
    print(session.get('username'))
    if session.get('username') != 'admin':
        return redirect(url_for('login'))
    return render_template('panel.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/login')
def login():
    return render_template("prijava.html")

@app.route('/paketi')
def paketi():
    return render_template('paketi.html')

@app.route('/info')
def info():
    return render_template('info.html')

@app.route('/getEmail', methods=['GET'])
def getEmail():
    ime = request.args.get('username')
    email = request.args.get('email')
    print(ime, email)
    return jsonify({"rez": ime})

@app.route('/loged')
def loged():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('loged.html')

@app.route("/getNFC/<ID>")
def getNFC(ID):
    global uids
    uids.append(ID)
    print(ID)

    return "OK prebral kartico "



if __name__ == '__main__':
    app.run(debug=True, port=8080) 
