from start import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean(), default=False)
    confirmed_at = db.Column(db.DateTime())
    accounts = db.relationship('Account', backref='user', lazy=True)

    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    affiliates = db.relationship("User")

    def __repr__(self):
        return '<User %r>' % self.email


class Account(db.Model):
    __tablename__ = 'account'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    settings = db.Column(db.Text(), nullable=False)
    timetables = db.relationship('TimeTable', backref='account', lazy=True)
    running = db.relationship('Running', backref='account', lazy=True)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    started = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    credit = db.Column(db.Integer, default=0)

    subscription = db.Column(db.String(10), nullable=False, unique=True)
    paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Account %r>' % self.username


def list():
    return [Account, User]
