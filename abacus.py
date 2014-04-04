# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required
from flask_mail import Mail

# config
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'super-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abacus.db'
db = SQLAlchemy(app)
app.config['MAIL_SERVER'] = 'mailhost.etrade.com'
mail = Mail(app)


# many to many helper table
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))


# setup Flask-security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)



# data model for creating and adding numbers
class Nums(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Integer)
    num2 = db.Column(db.Integer)
    num3 = db.Column(db.Integer)

    def __init__(self, num1, num2):
        self.num1 = num1
        self.num2 = num2

    def sum(self):
        self.num3 = self.num1 + self.num2
        return self.num3

    def __repr__(self):
        return 'num1{}, num2{}'.format(self.num1, self.num2)


# homepage
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# add two numbers and return jsonified result
@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    my_nums = Nums(num1=a, num2=b)
    my_nums.sum()
    db.session.add(my_nums)
    db.session.commit()
    return jsonify(result=my_nums.num3)
    

# flask webserver
if __name__ == '__main__':
    app.run(host='0.0.0.0')
