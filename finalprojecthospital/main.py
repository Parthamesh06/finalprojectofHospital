import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for session management
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'galgotias_appointments.db')
db = SQLAlchemy(app)


print("This is basedir", basedir)

class Appointments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    mobile = db.Column(db.String(15))

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/make_an_appointment", methods=['POST', 'GET'])
def make_an_appointment():
    if request.method == 'GET':
        return render_template("make_an_appointment.html")
    # Access form data using request.form
    name = request.form.get('name')
    location = request.form.get('location')
    mobile = request.form.get('mobile')

    error_message = None

    if len(mobile) != 10:
        error_message = "Mobile number must be 10 digits long."
        mobile = "" if not mobile else mobile + " - " + error_message  # Concatenate error message with mobile number if not 10 digits long

    if error_message:
        return render_template("index.html", error_message=error_message, name=name, location=location, mobile=mobile)

    # If the mobile number is valid, proceed with storing the data or other operations
    # Add your database operations here



    new_entry = Appointments(name = name, location = location, mobile = mobile)
    db.session.add(new_entry)
    db.session.commit()
    flash('Your response has been submitted!')
    return redirect(url_for("submitted"))

@app.route('/submitted')
def submitted():
    return render_template('submitted.html')

@app.route("/thank_you")
def thank_you():
    return render_template("thankyou.html")


 

# Add route for the About Us page
@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)