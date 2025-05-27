from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import json
import requests

app = Flask(__name__)
app.secret_key = "FitRiseGym"

db = TinyDB('stranke.json')
User = Query()
table=db.table('Tabela')
scanCount = db.table('ScanCount')

uids = []
registration = []
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/Register', methods=['POST'])
def Register():

    Ime = request.form["username"].strip()
    Geslo = request.form["password"]
    veljavnost = request.form["veljavnost"]
    Uid = request.form["uid"]

    duration = datetime.now() + timedelta(days = int(veljavnost))
    duration = duration.strftime('%d-%m-%Y')
    print(Ime, Geslo, veljavnost, Uid)
    user = db.table('Tabela').search(User.Name == Ime)
    print(user)
    identification = db.table('Tablela').search(User.Uid == Uid)
    if user:
        return jsonify({"success": False, "error": "Uporabnik je ze v sistemu"})
    elif identification:
        return jsonify({"success": False, "error": "Kartica je ze v sistemu"})
    else:
        if Ime == "" or Geslo == "" or Uid == "" or veljavnost == "":
            return jsonify({"success": False, 'error': 'Vsa polja morajo biti izpolnena'})
        else:
            table.insert({"Name": Ime, "Password": Geslo, "Uid": Uid, "Duration": duration, "Registered": datetime.now().strftime('%d-%m-%Y')})
            return jsonify({'success': True})

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
    global registration
    registrated = db.table('Tabela').search(User.Uid == ID)
    try:
        with open('stranke.json', 'r') as f:
            data = json.load(f)
        ime = ""
        for i, user in data['Tabela'].items():
            if user['Uid'] == ID:
                ime = user['Name']
                break
    except Exception as e:
        print(e)

    if not registrated:
        registration.append(ID)
    else:
        if ID in uids:
            uids.remove(ID)
        else:
            uids.append(ID)
            scanCount.insert({"Name": ime,"Uid": ID, "count": 1})
    print(ID)
    print(f"Registered: {uids}")
    print(f"Unregistered: {registration}")
    return "OK prebral kartico "

@app.route('/numberOfPeople', methods=['GET'])
def numberOfPeople():
    return jsonify({"number": len(uids)})



if __name__ == '__main__':
    app.run(debug=True, port=5000) 
