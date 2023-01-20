from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_sqlalchemy import SQLAlchemy

class User:
    def __init__(self, id, num,nom,prenom,pseudo,email, password,cert,keyy,is_connected):
        self.id = id
        self.num_card = num
        self.nom = nom
        self.prenom = prenom
        self.pseudo = pseudo
        self.email = email
        self.password = password
        self.certpath = cert
        self.keypath = keyy
        self.is_connected=is_connected

    def __repr__(self):
        return f'<User: {self.email}>'




