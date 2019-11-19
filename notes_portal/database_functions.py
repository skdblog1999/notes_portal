import db
from werkzeug.security import check_password_hash, generate_password_hash
import uuid


class User:
    """ It contains all the properties of user """

    def __init__(self, kid, session_id=0):
        self.kid = kid
        self.user_data = db.users.find_one({"_id": kid})
        if session_id:
            self.user_data["sessions"].remove(session_id)
        else:
            self.session_id = ""
        self.create_session()

    def create_session(self):
        self.session_id = str(uuid.uuid4())
        self.user_data["sessions"].append(self.session_id)
        self.update_user_data({"sessions": self.user_data["sessions"]})

    def update_user_data(self, data):
        db.users.update_one({"_id": self.kid}, {"$set": data})

    def get_user_data(self):
        self.user_data = db.users.find_one({"_id": self.kid})
        return self.user_data

    def logout(self):
        self.user_data["sessions"].remove(self.session_id)
        self.update_user_data({"sessions": self.user_data["sessions"]})


def validate_login_credentials(kid, password):
    """ Validates the user login credentials """
    user_info = db.users.find_one({"_id": kid})
    if user_info:
        if (
            check_password_hash(user_info["password"], password)
        ):
            return True, kid
        else:
            return False, "Wrong Password".title(), "alert-warning"
    else:
        return False, "No such user exists".title(), "alert-warning"


def verify_user_login_cookies(kid, session_id):
    """ Verifies user using cookies, if present """
    result = db.users.find_one({"_id": kid})
    if session_id in result["sessions"]:
        return True
    else:
        return False
