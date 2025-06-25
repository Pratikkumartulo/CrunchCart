user_data = {}

def addUser(username,email,gender,dob,password):
    if email in user_data:
        return False
    else:
        user_data[email] = {"username":username,
                            'gender':gender,
                            "dob":dob,
                            "password":password}
        return True

def validateUser(email,password):
    if email not in user_data:
        return False
    if user_data[email]['password'] == password:
        return True
    else:
        return False