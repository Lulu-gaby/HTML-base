from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, ChangeUsernameForm, ChangeEmailForm, ChangePasswordForm

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Введены неверные данные')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods=['GET','POST'])
@login_required
def account():
    username_form = ChangeUsernameForm()
    email_form = ChangeEmailForm()
    password_form = ChangePasswordForm()

    if username_form.submit_username.data and username_form.validate_on_submit():
        current_user.username = username_form.new_username.data
        db.session.commit()
        flash('Имя пользователя обновлено!', 'success')
        return redirect(url_for('account'))

    if email_form.submit_email.data and email_form.validate_on_submit():
        current_user.email = email_form.new_email.data
        db.session.commit()
        flash('Email обновлён!', 'success')
        return redirect(url_for('account'))

    if password_form.submit_password.data and password_form.validate_on_submit():
        if not bcrypt.check_password_hash(current_user.password, password_form.old_password.data):
            flash('Неверный старый пароль', 'danger')
        else:
            hashed = bcrypt.generate_password_hash(password_form.new_password.data).decode('utf-8')
            current_user.password = hashed
            db.session.commit()
            flash('Пароль обновлён!', 'success')
            return redirect(url_for('account'))
    return render_template('account.html', title='Аккаунт', username_form=username_form, email_form=email_form, password_form=password_form)