from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Donor(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(200))

    address = db.Column(db.String(500))

    mobile = db.Column(db.String(20))

    id_type = db.Column(db.String(20))

    id_number = db.Column(db.String(50))

class Donation(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    receipt_no = db.Column(db.String(50))

    donor_name = db.Column(db.String(200))

    amount = db.Column(db.Float)

    payment_mode = db.Column(db.String(50))

    donation_type = db.Column(db.String(50))

    donation_date = db.Column(db.String(50))

class Expense(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    expense_type = db.Column(db.String(100))

    amount = db.Column(db.Float)

    payment_mode = db.Column(db.String(50))

    expense_date = db.Column(db.String(50))

    description = db.Column(db.String(300))