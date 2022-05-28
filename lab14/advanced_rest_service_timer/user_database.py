users = {}


def get_user_login(ip):
    for key, value in users.items():
        if value[1] == ip:
            return key