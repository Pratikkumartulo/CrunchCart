from db import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

def addContact(name, email,message):
    contact = Contact(
        name=name,
        email=email,
        message=message
    )
    db.session.add(contact)
    db.session.commit()
    return True

def getAllContact():
    contacts = Contact.query.all()
    allContacts = []
    for contact in contacts:
        temp = {}
        temp['id'] = contact.id
        temp['name'] = contact.name
        temp['email'] = contact.email
        temp['message'] = contact.message
        temp['timestamp'] = contact.timestamp.strftime('%Y-%m-%d %H:%M:%S') if contact.timestamp else None
        allContacts.append(temp)
    return allContacts


