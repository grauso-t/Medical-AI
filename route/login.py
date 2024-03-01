from flask import Blueprint, request, render_template, session
import hashlib
from tinydb import TinyDB, Query

db = TinyDB("..\\medical-ai\\static\\database\\accounts.json")

login_blueprint = Blueprint("login", __name__, template_folder="../templates")

@login_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":        
        username = request.form.get("username")
        password = hashlib.sha1(request.form.get("password").encode()).hexdigest()

        User = Query()
        result = db.search(User.username == username)

        if result:
            stored_password = result[0]['password']
            
            if stored_password == password:
                session['user'] = username
                session['fhir_url'] = result[0]['fhir_url']
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