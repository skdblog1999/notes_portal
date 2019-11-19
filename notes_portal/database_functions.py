import db


class User:
    """ It contains all the properties of user """

    def __init__(self, email, session_id=0):
        self.email = email
        self.user_data = db.users.find_one({"email": email})
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
        db.users.update_one({"email": self.email}, {"$set": data})

    def get_user_data(self):
        self.user_data = db.users.find_one({"email": self.email})
        return self.user_data

    def logout(self):
        self.user_data["sessions"].remove(self.session_id)
        self.update_user_data({"sessions": self.user_data["sessions"]})