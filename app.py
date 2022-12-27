import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Create SQLITE Database - myDb
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.sqlite3'
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

#Models
class Books(db.Model):
    id = db.Column('book_id',db.Integer,primary_key = True)
    book_name = db.Column(db.String(30))
    author = db.Column(db.String(30))
    year_published= db.Column(db.Integer)
    book_type= db.Column(db.Integer)
    book_status = db.Column(db.String(30))
    books = db.relationship('Loans', backref='books')


    def __init__(self, book_name,author,year_published,book_type,book_status):
        self.book_name = book_name
        self.author = author
        self.year_published = year_published
        self.book_type = book_type
        self.book_status = book_status
       

 
class Customers(db.Model):
    id = db.Column('customer_id',db.Integer,primary_key = True)
    customer_name = db.Column(db.String(50))
    city = db.Column(db.String(50))
    age = db.Column(db.Integer)
    customer_status = db.Column(db.String(10))
    customers = db.relationship('Loans', backref='customers')

    def __init__(self, customer_name, city,age,customer_status):
        self.customer_name = customer_name
        self.city = city
        self.age = age
        self.customer_status = customer_status


class Loans(db.Model):
    id = db.Column('loan_id',db.Integer,primary_key = True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.customer_id'))
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    loandate = db.Column(db.String(50))
    returndate = db.Column(db.String(50))
    loan_status = db.Column(db.String(50))
    loan_activate = db.Column(db.String(30))

    def __init__(self, customer_id,book_id, loandate, returndate,loan_status,loan_activate):     
        self.customer_id = customer_id
        self.book_id = book_id
        self.loandate = loandate
        self.returndate = returndate
        self.loan_status = loan_status
        self.loan_activate = loan_activate
       
#Book Views
@app.route('/books/<id>',methods = ['GET','PUT'])
@app.route('/books/',methods = ['POST','GET'])
def crud_books(id=-1): 

    if request.method == 'POST': 
        request_data = request.get_json()
        book_name = request_data["book_name"]
        author = request_data["author"]
        year_published = request_data["year_published"]
        book_type = request_data["book_type"]
        book_status = request_data["book_status"]
        newBook= Books(book_name,author,year_published,book_type,book_status)
        db.session.add (newBook)
        db.session.commit()
        return ("A book was added")
        
    if request.method == 'GET':
        res=[]
        for book in Books.query.all():
            res.append({"book_id":book.id,
                        "book_name":book.book_name,
                        "author":book.author,
                        "year_published":book.year_published,
                        "book_type":book.book_type,
                        "book_status":book.book_status
                        })
        return (json.dumps(res))

    if request.method == 'PUT':
            request_data = request.get_json()
            upd_book = Books.query.get(id)
            if upd_book:
                upd_book.book_status =request_data["book_status"]
                db.session.commit()
            return "A book was update "

#Customers Views
@app.route('/customers/<id>',methods = ['DELETE','PUT'])
@app.route('/customers/',methods = ['POST','GET'])
def crud_customers(id=-1): 

    if request.method == 'POST': 
        request_data = request.get_json()
        customer_name = request_data["customer_name"]
        city = request_data["city"]
        age = request_data["age"]
        customer_status = request_data["customer_status"]
        newCustomer= Customers(customer_name,city,age,customer_status)
        db.session.add (newCustomer)
        db.session.commit()
        return ("A customer was added")

    if request.method == 'GET':
        res=[]
        for customer in Customers.query.all():
            res.append({"customer_id":customer.id,
                        "customer_name":customer.customer_name,
                        "city":customer.city,"age":customer.age,
                        "customer_status":customer.customer_status})
        return (json.dumps(res))
        
    if request.method == 'DELETE':
        del_customer= Customers.query.get(id)
        db.session.delete(del_customer)
        db.session.commit()
        return "A customer was deleted"

    if request.method == 'PUT':
            request_data = request.get_json()
            upd_customer = Customers.query.get(id)
            if upd_customer:
                upd_customer.customer_status =request_data["customer_status"]
                db.session.commit()
            return "A customer was update "

#Loans Views
@app.route('/loans/<id>',methods = ['DELETE','PUT'])
@app.route('/loans/',methods = ['POST','GET'])
def crud_loans(id=-1): 

    if request.method == 'POST': 
        request_data = request.get_json()
        customer_id = request_data["customer_id"]
        book_id = request_data["book_id"]
        loandate = request_data["loandate"]
        returndate = request_data["returndate"]
        loan_status = request_data["loan_status"]
        loan_activate = request_data["loan_activate"]
        newLoan= Loans(customer_id,book_id,loandate,returndate,loan_status,loan_activate)
        db.session.add (newLoan)
        db.session.commit()
        return "A loan was added"

    if request.method == 'GET': 
        res=[]
        for loan,book,customer in db.session.query(Loans,Books,Customers).join(Books).join(Customers):
            res.append({"loan_id":loan.id,
                        "customer_id":loan.customer_id,
                        "book_id":loan.book_id,
                        "book_id":book.id,
                        "book_type":book.book_type,
                        "book_name":book.book_name,
                        "book_status":book.book_status,
                        "loandate":loan.loandate,
                        "returndate":loan.returndate,
                        "loan_status":loan.loan_status,                   
                        "customer_name":customer.customer_name,
                        "loan_activate":loan.loan_activate                   
                        })
        return (json.dumps(res))   

    if request.method == 'PUT':
            request_data = request.get_json()
            upd_loan = Loans.query.get(id)
            if upd_loan:
                upd_loan.loan_activate =request_data["loan_activate"]
                db.session.commit()
            return "A loan was update "

if __name__ == '__main__':
     with app.app_context():db.create_all()
     app.run(debug = True)

