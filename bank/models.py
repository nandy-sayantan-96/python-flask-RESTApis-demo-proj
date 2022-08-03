from bank import db
from sqlalchemy.exc import IntegrityError
from sqlalchemy import and_


class Transactions(db.Model):
    rrn = db.Column(db.Integer(), primary_key=True)
    txn_date = db.Column(db.String(length=20), nullable=False)
    txn_number = db.Column(db.String(length=20), nullable=False)
    account_number = db.Column(db.Integer(), nullable=False)
    bank_name = db.Column(db.String(length=100), nullable=False)
    account_holder_name = db.Column(db.String(length=100), nullable=False)
    txn_type = db.Column(db.String(length=20), nullable=False)
    txn_amount = db.Column(db.Numeric(), nullable=False)


    def __repr__(self) -> str:
        return f'{{rrn: {self.rrn} - txn_date: {self.txn_date} - txn_number: {self.txn_number} - account_number: {self.account_number} - bank_name: {self.bank_name} - account_holder_name: {self.account_holder_name} - txn_type: {self.txn_type} - txn_amount: {self.txn_amount}}}'

    def save_to_db(self):
        db.session.add(self)
        try:
            db.session.commit()
            return True, "Success"
        except IntegrityError as err:
            db.session.rollback()
            if "UNIQUE constraint failed: transactions.rrn" in str(err.args[0]):
                return False, 'Record with same primary key already exists in db'
            else:
                return False, 'Integrity error occured during data insertion in db'
        except Exception as e:
            return False, 'Unknown error occured during data insertion in db'


    @classmethod
    def count_data(cls):
        try:
            return cls.query.count()
        except:
            # -1 will indicate the table doesn't exist in the db
            return -1


    @classmethod
    def count_banks(cls):
        try:
            return cls.query.with_entities(cls.bank_name).distinct().count()
        except:
            return -1


    @classmethod
    def get_transactions_in_date_range(cls,start_date,end_date):
        try:
            count = cls.query.with_entities(cls.txn_date).filter(and_(cls.txn_date >= start_date, cls.txn_date <= end_date)).count()
            return count
        except:
            # -1 will indicate some unexpected error has occurred
            return -1


    @classmethod
    def get_customer_names(cls):
        customer_names = []
        try:
            for account_holder_name in cls.query.with_entities(cls.account_holder_name).distinct():
                customer_names.append(account_holder_name[0])
            return True, customer_names
        except:
            return False, customer_names


    @classmethod
    def get_transactions_summary(cls):
        transactions = []
        try:
            for txn_type in cls.query.with_entities(cls.txn_type):
                transactions.append(txn_type[0])
            return True, transactions
        except:
            return False, transactions


    @classmethod
    def get_transaction_amount_summary(cls):
        transactions = {}
        try:
            for txn_details in cls.query.with_entities(cls.txn_type, cls.txn_amount):
                transactions[txn_details[0]] = transactions.get(txn_details[0],0) + float(txn_details[1])
            return True, transactions
        except:
            return False, transactions


    @classmethod
    def get_total_transaction_amount(cls):
        transaction_amount = 0
        try:
            for txn_amount in cls.query.with_entities(cls.txn_amount):
                transaction_amount += float(txn_amount[0])
            return True, transaction_amount
        except:
            return False, transaction_amount

