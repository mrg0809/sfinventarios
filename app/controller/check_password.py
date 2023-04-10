from model.handle_db import HandleDB
from werkzeug.security import check_password_hash


def check_user(username, password):
    user = HandleDB()
    filter_user = user.get_user(username)
    if filter_user:
        check_password = check_password_hash(filter_user[2], password)
        if filter_user[2] == password:
            return filter_user
    return None



