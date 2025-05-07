from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_from_directory
from tinydb import TinyDB, Query
from datetime import datetime
import os
import json
import requests

app = Flask(__name__)
app.secret_key = "FitRiseGym" 

db = TinyDB('stranke.json')
users = db.table('uporabniki')
User = Query()
table=db.table('Tabela')

@app.route('/')
def home():
    return render_template('prijava.html')

@app.route('/Register', methods=['POST'])
def Register():

    Ime = request.form["username"]

    Geslo = request.form["password"]
    try:
        with open("stranke.json") as y:
            value = json.load(y)
    except json.JSONDecodeError:
        value = {"Tabela": {}}
    if any(x["Name"] == Ime for x in value["Tabela"].values()):
        return render_template("prijava.html")
    table.insert({"Name": Ime, "Password": Geslo})
    return render_template("prijava.html")

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
                return render_template("index.html")
        return render_template("prijava.html", error="Napačno Ime ali Geslo")
    else:
        return render_template("prijava.html", error="Napačno Ime ali Geslo")

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    
    return render_template("prijava.html")



@app.route('/data')
def data():
    return "OK"

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



if __name__ == '__main__':
    app.run(debug=True, port = 8080) 
