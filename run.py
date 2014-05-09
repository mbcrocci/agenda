import os
from flask import Flask, render_template, redirect, request, flash, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from wtforms import Form, TextField, validators
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
# app.config['SQLALCHEMY_MIGRATE_REPO'] = os.path.join(basedir, 'db_repository')
db = SQLAlchemy(app)

app.secret_key = 'maurizio' # just to test


@app.route('/')
def index():
	return render_template('index.html')


# Contact database object and respective functions
class Contact(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(120), unique=True)
	email = db.Column(db.String(40))
	number = db.Column(db.String(15))

	def __init__(self, name, email, number):
		self.name = name
		self.email = email
		self.number = number

	def __repr__(self):
		return '<Contact %s %s %s>' %(self.name, self.email, self.number)

class New_Contact_Form(Form):
	name = TextField('Name', [validators.Length(min=4, max=120)])
	email = TextField('Email', [validators.Length(max=40)])
	number = TextField('Number', [validators.Length(min=9, max=15)])

@app.route('/add_contact', methods=['GET', 'POST'])
def add_contact():
	form = New_Contact_Form(request.form)
	if request.method == 'POST' and form.validate():
		contact = Contact(form.name.data, form.email.data, form.number.data)
		db.session.add(contact)
		db.session.commit()
		flash('New contact added')
		return redirect(url_for('index'))

	return render_template('add.html', form=form)

@app.route('/show_contacts')
def show_contacts():
	contacts = Contact.query.all()
	return render_template('show.html', contacts=contacts)


if __name__ == '__main__':
	app.run(debug=True)