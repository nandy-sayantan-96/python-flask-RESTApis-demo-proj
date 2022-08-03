from bank.models import Transactions
import datetime


class Data:
    def allowed_file(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv'


    def parseCSV(self, file_path):
        try:
            log_response = {'success_count': 0, 'failure_count': 0, 'row_error_msg': []}
            with open(file_path, 'r') as f:
                line_count = 1
                for line in f:
                    #Skipping the first line of the file
                    if line_count > 1:
                        line = line.strip()
                        txn_date, narration, txn_amount = line.split(',')
                        txn_number, rrn, account_number, bank_name, account_holder_name, txn_type = narration.split('/')[1:]
                        rrn = int(rrn.split(':')[1])
                        transaction_object = Transactions(rrn=rrn, txn_number=txn_number, account_number=account_number, bank_name=bank_name, account_holder_name=account_holder_name, txn_type=txn_type, txn_date=txn_date, txn_amount=txn_amount)
                        status, msg = transaction_object.save_to_db()
                        if status:
                            log_response['success_count'] += 1
                        else:
                            log_response['failure_count'] += 1
                            log_response['row_error_msg'].append(f'Error while insertion of contents in line {line_count}, error message - {msg}')
                    line_count += 1
            return log_response
        except Exception as e:
            print(str(e))
            raise e


    def validate_date_string(self, date_string):
        try:
            datetime.datetime.strptime(date_string, '%Y-%m-%d')
            return True
        except ValueError:
            return False

