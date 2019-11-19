from flask import (
    Flask,
    flash,
    make_response,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

import database_functions as db
import mail

app = Flask(__name__)
app.secret_key = "c6869b1f-d527-451a-a135-ef25a8945d98"

user = 0

@app.route("/")
def home():
    """ Entry point to dashboard and login page. It checks cookies to decide where to go. """
    session_id = request.cookies.get("sessionID")
    kid = request.cookies.get("kid")
    if session_id and kid:
        if db.verify_user_login_cookies(kid, session_id):
            global user
            user = db.User(kid, session_id)
            session["state"] = "loggedIn"
            # TODO - Change to the user home page
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("sessionID", user.session_id)
            resp.set_cookie("kid", user.kid)
            return resp
        else:
            return render_template("login.html")
    else:
        return render_template("login.html")


@app.route("/validate_login", methods=["POST", "GET"])
def validate_login():
    if request.method == "GET":
        flash("!!! Unauthorized Access Denied !!!", "alert-warning")
        return redirect(url_for("home"))
    elif request.method == "POST":
        global user
        kid = (request.form["kid"]).strip()
        password = (request.form["password"]).strip()
        result = db.validate_login_credentials(kid, password)
        if result[0]:
            user = db.User(result[1])
            session["state"] = "loggedIn"
            resp = make_response(redirect(url_for("dashboard")))
            resp.set_cookie("sessionID", user.session_id)
            resp.set_cookie("kid", user.kid)
            return resp
        else:
            flash(result[1], result[2])
            return redirect(url_for("home"))



# Just for Designing Purpose
@app.route("/<foldername>/<filename>")
@app.route("/<filename>")
@app.route('/<foldername>/<sub_folder>/<filename>')
def open_any_file(foldername="", filename="", sub_folder=""):
    
    return render_template(
        filename,
    )


@app.route("/dashboard")
def dashboard():
    if "state" in session:
        if session["state"] == "loggedIn":
            global user
            return render_template('dashboard.html')
        else:
            flash("!!! Unauthorized Access Denied !!!", "alert-warning")
            return redirect(url_for("home"))
    else:
        flash("!!! Unauthorized Access Denied !!!", "alert-warning")
        return redirect(url_for("home"))


# Logout
@app.route("/logout")
def logout():
    if "state" in session:
        if session["state"] == "loggedIn":
            resp = make_response(redirect(url_for("home")))
            resp.set_cookie("kid", expires=0)
            resp.set_cookie("sessionID", expires=0)
            global user
            user.logout()
            del user
            session["state"] = "loggedOut"
            return resp
        else:
            flash("!!! Unauthorized Access Denied !!!", "alert-warning")
            return redirect(url_for("home"))
    else:
        flash("!!! Unauthorized Access Denied !!!", "alert-warning")
        return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)