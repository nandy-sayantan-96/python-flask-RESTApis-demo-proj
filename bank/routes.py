from bank import app
from bank import global_response_template
from flask import request, jsonify
from bank.models import Transactions
from bank.data import Data
import os
from werkzeug.utils import secure_filename
from collections import Counter


@app.route('/post_data', methods=['POST'])
def post_data():
    response = global_response_template.copy()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            response['error'] = "No file found"
            return jsonify(response)
        file = request.files['file']
        # If the user does not select a file or submits an empty file without a filename.
        if file.filename == '':
            response['error'] = "No file selected"
            return jsonify(response)
        data_processing_obj = Data()
        if file and data_processing_obj.allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            try:
                logs = data_processing_obj.parseCSV(file_path)
                response['isSuccess'] = True
                response['response'] = 'File uploaded successfully..'
                response['logs'] = logs
            except Exception as e:
                response['error'] = "Unexpected error occurred while reading the file"
            finally:
                return jsonify(response)
        else:
            if not file:
                response['error'] = "Empty file uploaded"
            elif not data_processing_obj.allowed_file(file.filename):
                response['error'] = "Upload of only .csv files allowed"
            return jsonify(response)


@app.route('/records', methods=['GET'])
def records():
    response = global_response_template.copy()
    count = Transactions.count_data()
    if count == -1:
        response['error'] = "No table has been created yet in the db"
    else:
        response['isSuccess'] = True
        response['response'] = {'rows_count' : count}
    return jsonify(response)


@app.route('/banks', methods=['GET'])
def count_banks():
    response = global_response_template.copy()
    count = Transactions.count_banks()
    if count == -1:
        response['error'] = "Unexpected error occurred.."
    else:
        response['isSuccess'] = True
        response['response'] = {'banks_count' : count}
    return jsonify(response)


@app.route('/<from_date>/<to_date>', methods=['GET'])
def count_transactions_in_date_range(from_date, to_date):
    response = global_response_template.copy()
    data_processing_obj = Data()
    if data_processing_obj.validate_date_string(from_date) and data_processing_obj.validate_date_string(to_date):
        count = Transactions.get_transactions_in_date_range(from_date, to_date)
        if count == -1:
            response['error'] = "Unexpected error occurred.."
        else:
            response['isSuccess'] = True
            response['response'] = {'transactions_count' : count}
    else:
        response['error'] = "Incorrect data format, should be YYYY-MM-DD"
    return jsonify(response)


@app.route('/customer_names', methods=['GET'])
def get_customer_names():
    response = global_response_template.copy()
    status, customer_names = Transactions.get_customer_names()
    if not status:
        response['error'] = "Unexpected error occurred.."
    else:
        response['isSuccess'] = True
        response['response'] = {'customer_names' : [name.title() for name in customer_names]}
    return jsonify(response)


@app.route('/transactions_summary', methods=['GET'])
def get_transactions_summary():
    response = global_response_template.copy()
    status, transactions_summary = Transactions.get_transactions_summary()
    if not status:
        response['error'] = "Unexpected error occurred.."
    else:
        response['isSuccess'] = True
        transactions_summary_counter = Counter(transactions_summary)
        response['response'] = {'transactions_summary' : dict(transactions_summary_counter)}
    return jsonify(response)


@app.route('/transaction_amount_summary', methods=['GET'])
def get_transaction_amount_summary():
    response = global_response_template.copy()
    status, transactions_amount_summary = Transactions.get_transaction_amount_summary()
    if not status:
        response['error'] = "Unexpected error occurred.."
    else:
        response['isSuccess'] = True
        response['response'] = {'transactions_summary' : transactions_amount_summary}
    return jsonify(response)


@app.route('/total_transaction_amount', methods=['GET'])
def get_total_transaction_amount():
    response = global_response_template.copy()
    status, total_transactions_amount = Transactions.get_total_transaction_amount()
    if not status:
        response['error'] = "Unexpected error occurred.."
    else:
        response['isSuccess'] = True
        response['response'] = {'total_transactions_amount' : total_transactions_amount}
    return jsonify(response)

