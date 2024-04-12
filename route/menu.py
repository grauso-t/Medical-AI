from flask import Blueprint, render_template, session, jsonify
import route.utils as utils

menu_blueprint = Blueprint("menu", __name__, template_folder="../templates")

@menu_blueprint.route("/dashboard")
def dashboard():
    if 'user' in session and session['user'] is not None:
        return render_template("dashboard.html", username=session['user'])
    else:
        return render_template("login.html")
    
@menu_blueprint.route("/account")
def account():
    if 'user' in session and session['user'] is not None:
        return render_template("info.html")
    else:
        return render_template("login.html")
    
@menu_blueprint.route('/loadata')
def loadata():
    observation = utils.create_observation(session)
    patient = utils.create_patient(session)
    return jsonify({"observation": observation, "patient": patient})