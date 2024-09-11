from flask import Blueprint, render_template,request, flash,redirect,url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user,current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth' , __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash('logged in successfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password',category='danger')
        else:
            flash('Email does not exist.',category='danger')
    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        last_name = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists',category='danger')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters',category='danger')
        elif len(first_name) < 2:
            flash('FirstName must be greater than3 characters',category='danger')
        elif(password1!=password2):
            flash('passwords don\'t match.',category='danger')
        elif(len(password1)<7):
            flash('password must have atleast 7 characters',category='danger')
        else:
            new_user = User(email=email,first_name=first_name,last_name = last_name,password=generate_password_hash(password1))
            db.session.add(new_user)
            print(new_user)
            db.session.commit()
            login_user(new_user,remember=True)
            flash('Account is created', category='success')
           
            return redirect(url_for('views.home'))
    return render_template("signup.html",user=current_user)

@auth.route('/admin')
def admin():
    users = User.query.order_by(User.id).all()
    if current_user.email == "seetharamvijay3@gmail.com":
        return render_template("admin.html",users=users)
    else:
        return "You are not autherized to view this page"