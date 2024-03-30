from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from .models import User, users_schema
from werkzeug.security import generate_password_hash, check_password_hash
from . import db   # means from __init__.py import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email1=email).first()
        if user.invitee:
            flash('Invitees cannot login.', category='error')
        elif user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.profile'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email1=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email1=email, name=name, password=generate_password_hash(
                password1, method='pbkdf2:sha256'), invitee=False)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.profile'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/invitee-sign-up', methods=['GET', 'POST'])
def invitee_sign_up():
    '''
    Sign up from invitation ID
    '''
    if request.method == 'POST':
        invite_id = request.form.get('invite-id')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(invite_id=invite_id).first()

        if user:
        # found ID
            if user.password == None:
                # invitee has not set password
                if password1 != password2:
                    flash('Passwords don\'t match.', category='error')
                elif len(password1) < 7:
                    flash('Password must be at least 7 characters.', category='error')
                else:
                    user.password = generate_password_hash(password1, method='pbkdf2:sha256')
                    db.session.commit()
                    login_user(user, remember=True)
                    flash('Account created!', category='success')
                    return redirect(url_for('views.profile'))
                
            elif user.password != None:
                # invitee has already set password
                if check_password_hash(user.password, password1):
                    flash('Logged in successfully!', category='success')
                    login_user(user, remember=True)
                    return redirect(url_for('views.profile'))
                else:
                    flash('Incorrect password, try again.', category='error')
        else:
            flash('Incorrect invitation ID.', category='error')
                
            
    return render_template("invitee_sign_up.html", user=current_user)


@auth.route('/user', methods=['GET'])
def get_users():
    all_users = User.query.all()
    res = users_schema.dump(all_users)
    print(res)
    return jsonify(res)