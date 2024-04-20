from flask import Flask, render_template, session
import route.login as login
import route.menu as menu
import route.bot as bot
import os

app = Flask(__name__, template_folder="../templates")
app.register_blueprint(login.login_blueprint)
app.register_blueprint(menu.menu_blueprint)
app.register_blueprint(bot.bot_blueprint)

app.secret_key = os.urandom(24)

@app.route("/")
@app.route("/index")
def index():
    if 'user' in session and session['user'] is not None:
        return render_template("dashboard.html", username=session['user'])
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)