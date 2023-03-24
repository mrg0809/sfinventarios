from model.handle_db import HandleDB
from werkzeug.security import generate_password_hash

class User():
    data_user = {}

    def __init__(self, data_user):
        self.db = HandleDB
        self.data_user = data_user

    def _pass_encrypt(self):
        self.data_user["password"] = generate_password_hash(self.data_user["password"], "pbkdf2:sha256:30", 30)