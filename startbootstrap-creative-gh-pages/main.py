from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_bootstrap import Bootstrap
from datetime import datetime
import requests
import smtplib
from markupsafe import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,PasswordField,ValidationError
from wtforms.validators import DataRequired,Email,Length
import sqlite3
import smtplib
from flask_sqlalchemy import SQLAlchemy
import os
my_email = "nathantay1408@gmail.com"
password = "zjjixkftjtkrxwdg"

connection = smtplib.SMTP("smtp.gmail.com")


app = Flask(__name__)#this would allow flask to know which file its based on which is this python file
app.secret_key = "meme"
bootstrap = Bootstrap(app)
db = sqlite3.connect("email-collection.db",check_same_thread=False)


cursor = db.cursor()

##CREATE TABLE
if not sqlite3.OperationalError:
 cursor.execute("CREATE TABLE email (Name varchar(250) NOT NULL UNIQUE, Email varchar(250) NOT NULL)")


class ContactForm(FlaskForm):
    email = StringField(label='Email', validators=[DataRequired(), Email()])
    password = PasswordField(label='Name', validators=[DataRequired(), Length(min=2)])
    submit = SubmitField(label="submit")




@app.route("/")
def homepage():
    return render_template("index.html")
@app.route("/index")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")

@app.route("/CCA")
def cca():
    return render_template("activites.html")

@app.route("/services")

def services():
    return render_template("services.html")

@app.route("/contact",methods=['GET', 'POST'])

def contact():

    Contact_form = ContactForm()
    Contact_form.validate_on_submit()

    if Contact_form.validate_on_submit():
            splitted = Contact_form.email.data.split("@")
            print(splitted[1])
            params = (Contact_form.password.data,Contact_form.email.data)
            Name=Contact_form.password.data
            Emaill=Contact_form.email.data

            cursor.execute(f"INSERT INTO email (Name,Email) VALUES (?,?)",(Name,Emaill))
            db.commit()
            with smtplib.SMTP("smtp.gmail.com") as connection:
             connection.starttls()
             connection.login(user=my_email, password=password)
             connection.sendmail(from_addr=my_email,
                                to_addrs=Emaill,
                                msg="Subject:Portfolio\n\nYo,thanks for the interest")
             connection.close()

    return render_template("Contact.html",form=Contact_form)


if __name__ == "__main__":
    app.run(debug=True)