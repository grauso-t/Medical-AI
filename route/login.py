from flask import Blueprint, request, render_template, session
import hashlib
from tinydb import TinyDB, Query

login_blueprint = Blueprint("login", __name__, template_folder="../templates")

@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":        
        username = request.form.get("username")
        password = hashlib.sha1(request.form.get("password").encode()).hexdigest()

        db = TinyDB("..\\medical-ai\\static\\database\\accounts.json")
        User = Query()
        result = db.search(User.username == username)

        if result:
            stored_password = result[0]['password']
            
            if stored_password == password:
                session['user'] = username
                session['fhir_url'] = result[0]['fhir_url']
                session['openai-key'] = result[0]['openai-key']
                db.close()
                return render_template("dashboard.html", username=session['user'])

        error = "Invalid username or password"
        return render_template("login.html", error=error)
    else:
        if 'user' in session and session['user'] is not None:
            return render_template("dashboard.html", username=session['user'])
        else:
            return render_template("login.html")

@login_blueprint.route("/logout")
def logout():
    session.pop('user', None)
    error = "Disconnected"
    return render_template("login.html", error=error)

@login_blueprint.route('/info_form', methods=['POST'])
def info_form():
    if request.method == 'POST' and 'user' in session and session['user'] is not None:
        username = session['user']
        password = hashlib.sha1(request.form.get("password").encode()).hexdigest()
        fhir_url = request.form['fhir_url']
        openai_key = request.form['openai-key']
        
        session['fhir_url'] = fhir_url
        session['openai-key'] = openai_key
        
        db = TinyDB("..\\medical-ai\\static\\database\\accounts.json")
        
        # Check if the user exists
        user_query = Query()
        user = db.search(user_query.username == username)
        
        # If user exists, update the record, otherwise insert a new record
        if user:
            db.update({'password': password, 'fhir_url': fhir_url, 'openai-key': openai_key}, user_query.username == username)
            db.close()
            return render_template("dashboard.html", username=username)
        else:
            return render_template("info.html")
    elif 'user' in session and session['user'] is None:
        return render_template("login.html")