from flask import Blueprint,render_template,request,flash,redirect,url_for
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,logout_user,current_user

from . import db
from .models import User

auth = Blueprint('auth',__name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        print(email,password)
        if not email and not password:
            flash('Fill the fields!',category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                if check_password_hash(user.password,password):
                    flash('Login Successfully',category='success')
                    login_user(user,remember=True)
                    return redirect(url_for('views.home'))
                else:
                    flash('Invalid password! try again',category='error')
            else:
                flash('Email doest not exists!',category='error')

    return render_template('signin.html',user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')

        if not email and not username and not password:
            flash('Fill the fields!',category='error')
        else:
            user = User.query.filter_by(email=email).first()
            if user:
                flash('With this Email user already exists!',category='error')
            elif len(username) < 4:
                flash('Email should be greater than 4 characters!',category='error')
            elif len(email) < 6:
                flash('Username should be greater than 4 characters!',category='error')
            elif password != confirmPassword:
                flash('Passwords not match!',category='error')
            elif len(password) < 8:
                flash('Password must be at least 6 Characters!',category='error')
            else:
                new_user = User(username=username,email=email,password=generate_password_hash(password,method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Account created!',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))

    return render_template('signup.html',user=current_user)