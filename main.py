from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from tinydb import TinyDB, Query
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key = "FitRiseGym" 

db = TinyDB('stranke.json')
users = db.table('uporabniki')
User = Query()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            user = users.get(User.username == username)
            
            if user:
                if user['password'] == password:
                    session['username'] = username

                    return jsonify({'success': True})
                    
                else:
                    return jsonify({'success': False, 'error': 'Napačno geslo'})
            else:
                users.insert({'username': username, 'password': password})

                session['username'] = username
                return jsonify({'success': True})
                
        except Exception as e:
            print(f"Napaka pri prijavi: {str(e)}")
            return jsonify({'success': False, 'error': 'Prišlo je do napake'})
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    
    
    session.pop('username', None)
    return redirect(url_for('login'))



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
    ime = request.form['username']
    email = request.form['email']
    print(ime, email)



if __name__ == '__main__':
    app.run(debug=True, port = 8080) 
