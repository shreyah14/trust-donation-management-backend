from flask import Flask, request, jsonify
from flask_cors import CORS

from models import db, Donor, Donation, Expense

app = Flask(__name__)

CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Backend Running"


@app.route('/add-donor', methods=['POST'])
def add_donor():

    data = request.json

    donor = Donor(
        name=data['name'],
        address=data['address'],
        mobile=data['mobile'],
        id_type=data['id_type'],
        id_number=data['id_number']
    )

    db.session.add(donor)

    db.session.commit()

    return jsonify({
        "message": "Donor Added Successfully"
    })


@app.route('/donors', methods=['GET'])
def get_donors():

    donors = Donor.query.all()

    output = []

    for donor in donors:

        output.append({
            "id": donor.id,
            "name": donor.name,
            "mobile": donor.mobile,
            "address": donor.address,
            "id_type": donor.id_type,
            "id_number": donor.id_number
        })

    return jsonify(output)

@app.route('/add-donation', methods=['POST'])
def add_donation():

    data = request.json

    donation_count = Donation.query.count() + 1

    receipt_no = f"RCPT-{donation_count:04}"

    donation = Donation(
        receipt_no=receipt_no,
        donor_name=data['donor_name'],
        amount=data['amount'],
        payment_mode=data['payment_mode'],
        donation_type=data['donation_type'],
        donation_date=data['donation_date']
    )

    db.session.add(donation)

    db.session.commit()

    return jsonify({
        "message": "Donation Saved",
        "receipt_no": receipt_no
    })


@app.route('/donations', methods=['GET'])
def get_donations():

    donations = Donation.query.all()

    output = []

    for donation in donations:

        output.append({
            "id": donation.id,
            "receipt_no": donation.receipt_no,
            "donor_name": donation.donor_name,
            "amount": donation.amount,
            "payment_mode": donation.payment_mode,
            "donation_type": donation.donation_type,
            "donation_date": donation.donation_date
        })

    return jsonify(output)

@app.route('/add-expense', methods=['POST'])
def add_expense():

    data = request.json

    expense = Expense(
        expense_type=data['expense_type'],
        amount=data['amount'],
        payment_mode=data['payment_mode'],
        expense_date=data['expense_date'],
        description=data['description']
    )

    db.session.add(expense)

    db.session.commit()

    return jsonify({
        "message": "Expense Added Successfully"
    })


@app.route('/expenses', methods=['GET'])
def get_expenses():

    expenses = Expense.query.all()

    output = []

    for expense in expenses:

        output.append({
            "id": expense.id,
            "expense_type": expense.expense_type,
            "amount": expense.amount,
            "payment_mode": expense.payment_mode,
            "expense_date": expense.expense_date,
            "description": expense.description
        })

    return jsonify(output)

@app.route('/expense/<int:id>', methods=['GET'])
def get_single_expense(id):

    expense = Expense.query.get(id)

    if not expense:

        return jsonify({
            "message": "Expense not found"
        }), 404

    return jsonify({
        "id": expense.id,
        "expense_type": expense.expense_type,
        "amount": expense.amount,
        "payment_mode": expense.payment_mode,
        "expense_date": expense.expense_date,
        "description": expense.description
    })


@app.route('/update-expense/<int:id>', methods=['PUT'])
def update_expense(id):

    expense = Expense.query.get(id)

    if not expense:

        return jsonify({
            "message": "Expense not found"
        }), 404

    data = request.json

    expense.expense_type = data['expense_type']
    expense.amount = data['amount']
    expense.payment_mode = data['payment_mode']
    expense.expense_date = data['expense_date']
    expense.description = data['description']

    db.session.commit()

    return jsonify({
        "message": "Expense Updated Successfully"
    })

@app.route('/donation/<int:id>', methods=['GET'])
def get_single_donation(id):

    donation = Donation.query.get(id)

    if not donation:

        return jsonify({
            "message": "Donation not found"
        }), 404

    return jsonify({

        "id": donation.id,

        "receipt_no": donation.receipt_no,

        "donor_name": donation.donor_name,

        "amount": donation.amount,

        "payment_mode": donation.payment_mode,

        "donation_type": donation.donation_type,

        "donation_date": donation.donation_date
    })

@app.route('/delete-donation/<int:id>', methods=['DELETE'])
def delete_donation(id):

    donation = Donation.query.get(id)

    if not donation:

        return jsonify({
            "message": "Donation not found"
        }), 404

    db.session.delete(donation)

    db.session.commit()

    return jsonify({
        "message": "Donation Deleted Successfully"
    })

@app.route('/update-donation/<int:id>', methods=['PUT'])
def update_donation(id):

    donation = Donation.query.get(id)

    if not donation:

        return jsonify({
            "message": "Donation not found"
        }), 404

    data = request.json

    donation.donor_name = data['donor_name']

    donation.amount = data['amount']

    donation.payment_mode = data['payment_mode']

    donation.donation_type = data['donation_type']

    donation.donation_date = data['donation_date']

    db.session.commit()

    return jsonify({
        "message": "Donation Updated Successfully"
    })

if __name__ == '__main__':
    app.run(debug=True)