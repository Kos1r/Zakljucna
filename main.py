from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from tinydb import TinyDB, Query
from datetime import datetime, timedelta
import json
import requests
import smtplib
from email.mime.text import MIMEText
from itsdangerous import URLSafeTimedSerializer
from email.mime.multipart import MIMEMultipart
import os
from flask import send_file
import threading
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import statistics
import smtplib

app = Flask(__name__)
app.secret_key = "FitRiseGym"

def send_async_email(message):
    # locen thread za response uporabniku pri registraciji brez delaya
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login("fitriseslovenija@gmail.com", "ijvr ayvt irxd ekap")
            smtp.send_message(message)
            print("Email uspešno poslan v ozadju.")
    except Exception as e:
        print(f"Napaka pri pošiljanju maila v ozadju: {e}")

db = TinyDB('stranke.json', ensure_ascii=False, encoding='UTF-8')
training_logs = db.table('TrainingLogs')
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
    Name = request.form.get("name", "").strip()
    Lastname = request.form.get("lastname", "").strip()
    Email = request.form.get("username", "").strip()
    Geslo = request.form.get("password", "")

    if db.table('Tabela').search(User.email == Email):
        return jsonify({"success": False, "error": "Uporabnik s tem e-naslovom že obstaja"})

    user_data = {
        "name": Name,
        "lastname": Lastname,
        "email": Email,
        "Password": Geslo,
        "Uid": "", 
        "Duration": "0",
        "Registered": datetime.now().strftime('%d-%m-%Y')
    }
    
    s = URLSafeTimedSerializer(app.secret_key)
    token = s.dumps(user_data, salt='email-confirm')
    confirm_url = url_for('confirm_registration', token=token, _external=True)

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head><meta charset="UTF-8"></head>
    <body style="margin: 0; padding: 0; font-family: sans-serif; background-color: #050505; color: #ffffff;">
        <table width="100%" border="0" cellspacing="0" cellpadding="0" style="background-color: #050505; padding: 60px 20px;">
            <tr>
                <td align="center">
                    <div style="max-width: 550px; border: 1px solid #c00; padding: 50px 40px; background-color: #1a1a1a; border-radius: 6px;">
                        <h1 style="color: #c00; text-transform: uppercase; letter-spacing: 6px; border-bottom: 1px solid #333; padding-bottom: 20px;">FITRISE</h1>
                        <p style="font-size: 17px; line-height: 1.7; text-align: left; color: #eee;">
                            Pozdravljeni, <strong>{Name} {Lastname}</strong>,<br><br>
                            Vaš profil je skoraj pripravljen. Za aktivacijo kliknite spodnji gumb:
                        </p>
                        <div style="text-align: center; margin: 40px 0;">
                            <a href="{confirm_url}" style="background-color: #111; color: #fff; padding: 16px 32px; text-decoration: none; border: 1px solid #c00; text-transform: uppercase; letter-spacing: 2px; border-radius: 4px;">
                                Potrdi registracijo
                            </a>
                        </div>
                        <p style="font-size: 11px; color: #777; border-top: 1px solid #333; padding-top: 20px;">
                            Povezava: {confirm_url}
                        </p>
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """

    text_body = f"Pozdravljeni {Name},\n\nPotrdite registracijo tukaj: {confirm_url}"

    message = MIMEMultipart("alternative")
    message["Subject"] = "FitRise - potrditev računa"
    message["From"] = "fitriseslovenija@gmail.com"
    message["To"] = Email
    message.attach(MIMEText(text_body, "plain"))
    message.attach(MIMEText(html_body, "html"))

    # posiljanje v ozadju
    email_thread = threading.Thread(target=send_async_email, args=(message,))
    email_thread.start()

    return jsonify({'success': True})
# Account confirmation
@app.route('/confirm_registration/<token>')
def confirm_registration(token):
    try:
        s = URLSafeTimedSerializer(app.secret_key)
        #expires after 5 min
        data = s.loads(token, salt='email-confirm', max_age=300)
    except:
        return "Povezava je neveljavna ali je potekla."

    if table.search(User.email == data['email']):
        return render_template("prijava.html", 
                               alert_msg="Ta račun je že bil potrjen. Prosimo, prijavite se.")

    try:
        duration = datetime.now() + timedelta(days=int(data['veljavnost']))
        duration_str = duration.strftime('%d-%m-%Y')
    except (KeyError, ValueError):
        duration_str = "Nimate še aktivne karte"

    table.insert({
        "name": data['name'],
        "lastName": data['lastname'],
        "email": data['email'], 
        "Password": data['Password'], 
        "Uid": data['Uid'], 
        "Duration": duration_str, 
        "Registered": datetime.now().strftime('%d-%m-%Y')
    })

    return render_template("prijava.html", alert_msg="Registracija uspešna! Zdaj se lahko prijavite.")

@app.route("/Login", methods=["POST"])
def Login():
    
    Email = request.form["username"]
    Geslo = request.form["password"]
    try:
        with open("stranke.json") as y:
            value = json.load(y)
    except json.JSONDecodeError:
        value = {"Tabela": {}}
    if any(x["email"] == Email for x in value["Tabela"].values()):
        for x in value["Tabela"].values():
            if x["email"] == Email and x["Password"] == Geslo:
                session['username'] = Email
                return jsonify({'success': True})
        return jsonify({'success': False, 'error': 'Napačno geslo'})
    elif Email == "admin" and Geslo == "admin":
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

@app.route('/register')
def register():
    return render_template("registracija.html")

@app.route('/paketi')
def paketi():
    return render_template('paketi.html')

@app.route('/loged')
def loged():
    if 'username' not in session:
        return redirect(url_for('login'))

    format_datuma = "%d-%m-%Y"
    danes = datetime.now()
    trenutni_email = session['username']

    if trenutni_email == "admin":
        uporabniki = table.all()
        for u in uporabniki:
            u['is_expired'] = True
            if u.get('Duration') and u.get('Duration') != "0":
                try:
                    datum_v = datetime.strptime(u['Duration'], format_datuma)
                    if datum_v >= danes: u['is_expired'] = False
                except: pass
        return render_template('panel.html', uporabniki=uporabniki)

    user_data = table.get(User.email == trenutni_email)
    if not user_data: return "Napaka"

    date_str = user_data.get("Duration", "0")
    dan, ure = 0, 0
    try:
        dur_date = datetime.strptime(date_str, format_datuma)
        razlika = dur_date - danes
        dan = max(0, razlika.days)
        ure = max(0, razlika.seconds // 3600)
    except: pass

    user_logs = training_logs.search(User.email == trenutni_email)
    
    durations = [log['duration'] for log in user_logs if log['duration'] > 5] # filtriraj skene pod 5 min
    avg_dur = round(statistics.mean(durations), 1) if durations else 0
    
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    weekly_stats = [0] * 7
    for log in user_logs:
        log_date = datetime.strptime(log['date'], '%d-%m-%Y')
        if (danes - log_date).days <= 7:
            day_idx = log_date.weekday()
            weekly_stats[day_idx] += 1

    cnt = len(user_logs)

    stats = {
        "avg_duration": avg_dur,
        "goal_progress": min(int((cnt / 30) * 100), 100),
        "weekly_data": weekly_stats,
        "labels": ["Pon", "Tor", "Sre", "Čet", "Pet", "Sob", "Ned"]
    }

    return render_template('loged.html', cnt=cnt, dan=dan, ure=ure, date=date_str, stats=stats)

@app.route("/getNFC/<ID>")
def getNFC(ID):
    global uids
    user = table.get(User.Uid == ID)
    
    if not user:
        if ID not in registration:
         print(f"Nova neregistrirana kartica zaznana: {ID}")
         return "Unregistered card", 404

    ime = user['name']
    email = user['email']
    now = datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')

    # vstop/izstop
    if ID in uids:
        uids.remove(ID)
        entry_data = scanCount.get((User.Uid == ID))
        if entry_data and "last_entry" in entry_data:
            entry_time = datetime.strptime(entry_data["last_entry"], '%Y-%m-%d %H:%M:%S')
            duration = (now - entry_time).total_seconds() / 60 
            
            training_logs.insert({
                "email": email,
                "date": now.strftime('%d-%m-%Y'),
                "weekday": now.strftime('%a'),
                "duration": round(duration, 1)
            })
        print(f"User {ime} LEFT. Duration: {round(duration, 1)} min")
    else:
        #prisel
        uids.append(ID)
        
        curr_sc = scanCount.get(User.Uid == ID)
        if curr_sc:
            new_count = curr_sc.get("count", 0) + 1
            scanCount.update({"count": new_count, "last_entry": now_str}, User.Uid == ID)
        else:
            scanCount.insert({"Name": ime, "Uid": ID, "email": email, "count": 1, "last_entry": now_str})
        
        print(f"User {ime} ENTERED at {now_str}")

    return "OK"

@app.route('/numberOfPeople', methods=['GET'])
def numberOfPeople():
    return jsonify({"number": len(uids)})


@app.route('/admin/update_user', methods=['POST'])
def update_user():
    if session.get('username') != 'admin':
        return redirect(url_for('login'))
    
    original_email = request.form.get('original_email')
    nov_email = request.form.get('username')
    novo_ime = request.form.get('name')
    nov_priimek = request.form.get('lastname')
    nov_uid = request.form.get('uid')
    izbran_paket = request.form.get('paket_tip')
    akcija = request.form.get('action')

    user = table.get(User.email == original_email)
    
    if user:
        format_datuma = '%d-%m-%Y'
        new_data = {
            'name': novo_ime,
            'lastName': nov_priimek,
            'email': nov_email,
            'Uid': nov_uid,
            'Paket': izbran_paket
        }

        if akcija == 'save_all':
            flash(f"Podatki za {nov_email} so bili uspešno posodobljeni.", "success")
            
        elif akcija == 'podaljsaj':
            danes = datetime.now()
            trenutna_veljavnost_str = user.get('Duration', '')
            try:
                if trenutna_veljavnost_str and trenutna_veljavnost_str != "0":
                    trenutna_dt = datetime.strptime(trenutna_veljavnost_str, format_datuma)
                    zacetni_datum = trenutna_dt if trenutna_dt > danes else danes
                else:
                    zacetni_datum = danes
            except ValueError:
                zacetni_datum = danes
                
            nov_datum = (zacetni_datum + timedelta(days=30)).strftime(format_datuma)
            new_data['Duration'] = nov_datum
            flash(f"Članstvo za {nov_email} podaljšano do {nov_datum}.", "success")

        table.update(new_data, User.email == original_email)
    else:
        flash("Napaka: Uporabnik ni bil najden.", "danger")

    return redirect(url_for('loged'))


if __name__ == '__main__':
    app.run(debug=True, port=5000) 
