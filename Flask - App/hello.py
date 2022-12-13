from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app=Flask(__name__)

app.config['SECRET_KEY']="ashina"
#initialise our database
db=SQLAlchemy(app)
#point to where our database is
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///customer.db'

class Customers(db.Model):
    name=db.Column(db.String(200),nullable=False)
    phone=db.Column(db.Integer(),nullable=False,unique=True)
    user_id=db.Column(db.Integer(),primary_key=True, unique=True)
    date_added=db.Column(db.DateTime(),default=datetime.utcnow)


class CustomerForm(FlaskForm):
    name=StringField("Customer Name",validators=[DataRequired()])
    phone = IntegerField("Phone No: ",validators=[DataRequired()])
    user_id = IntegerField("User Id : ",validators=[DataRequired()])
    submit = SubmitField("Submit ")

@app.route('/')
def index():
   
    queried_users=Customers.query.order_by(Customers.date_added)
    return render_template('index.html',queried_users=queried_users)

@app.route('/form', methods=["GET","POST"])
def form():
    form=CustomerForm()
    name=None
    phone=None
    user_id=None
    if (form.validate_on_submit()):
        customer = Customers.query.filter_by(user_id=form.user_id.data).first()
        if customer is None:
            customer = Customers(name= form.name.data,phone=form.phone.data,user_id=form.user_id.data)
            db.session.add(customer)
            db.session.commit()
        name= form.name.data
        phone=form.phone.data
        user_id=form.user_id.data
        form.name.data=''
        form.phone.data=''
        form.user_id.data=''
    return render_template('form.html',name=name,phone=phone,user_id=user_id,form=form)


if __name__ == '__main__':
    app.run()