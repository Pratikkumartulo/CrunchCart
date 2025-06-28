from flask import session
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
    
def addSession(email):
    session['email'] = email

def isLoggedIn():
    if 'email' in session and session['email'] in user_data:
        Curruser = {k: v for k, v in user_data[session['email']].items() if k != 'password'}
        Curruser['email'] = session['email']
        return Curruser
    else:
        return None
    
def logoutUser():
    session.pop('email', None)
    return True