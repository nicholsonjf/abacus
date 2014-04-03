# -*- coding: utf-8 -*-
from flask import Flask, jsonify, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abacus.db'
db = SQLAlchemy(app)

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
        return '{}, {}'.format(self.num1, self.num2)

@app.route('/_add_numbers')
def add_numbers():
    a = request.args.get('a', 0, type=int)
    b = request.args.get('b', 0, type=int)
    my_nums = Nums(num1=a, num2=b)
    my_nums.sum()
    db.session.add(my_nums)
    db.session.commit()
    return jsonify(result=my_nums.num3)
    

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0')
