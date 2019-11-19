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

app = Flask(__name__)

@app.route("/")
def home():
    """ Entry point to dashboard and login page. It checks cookies to decide where to go. """
    session_id = request.cookies.get("sessionID")
    email = request.cookies.get("email")
    if session_id and email:
        if db.verify_user_login_cookies(email, session_id):
            global user
            user = db.User(email, session_id)
            session["state"] = "loggedIn"
            # TODO - Change to the user home page
            resp = make_response(redirect(url_for("app.dashboard")))
            resp.set_cookie("sessionID", user.session_id)
            resp.set_cookie("email", user.email)
            return resp
        else:
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")

# Just for Designing Purpose
@app.route("/<foldername>/<filename>")
@app.route("/<filename>")
@app.route('/<foldername>/<sub_folder>/<filename>')
def open_any_file(foldername="", filename="", sub_folder=""):
    
    return render_template(
        filename,
    )


if __name__ == '__main__':
    app.run(debug=True)