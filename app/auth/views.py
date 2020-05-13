import os

from app import db
from app.auth import auth_bp
from app.models import User
from app.models import DoctorCode
from .forms import RegistrationForm
from .forms import LoginForm
from .forms import RegistrationUserForm
from app.utils import allowed_file

from flask_login import current_user
from flask_login import login_user
from flask_login import logout_user
from flask import redirect
from flask import url_for
from flask import current_app
from flask import flash
from flask import request
from flask import render_template
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse



@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('用户名或密码有误')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Sign In', form=form)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        file = form.avatar.data
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['AVATAR_FOLDER'], filename))
        if not file:
            filename = 'default.png'
        if form.doctor_code.data:
            doctor = User(
                username=form.username.data, 
                doctor=True,
                avatar=filename,
                doctor_code=form.doctor_code.data,
                phone_number=form.phone_number.data, 
                email=form.email.data,
                male=form.male.data)
            doctor.set_password(form.password.data)
            db.session.add(doctor)
        else:
            user = User(
                username=form.username.data, 
                avatar=filename, 
                phone_number=form.phone_number.data, 
                email=form.email.data,
                male=form.male.data)
            user.set_password(form.password.data)
            db.session.add(user)
        db.session.commit()
        flash('恭喜，你已经成功注册')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register',
                           form=form)


@auth_bp.route('/register_user', methods=['GET', 'POST'])
def register_user():
    form = RegistrationUserForm()
    if form.validate_on_submit():
        filename = 'default.png'
        user = User(
            username=form.username.data, 
            avatar=filename,
            phone_number=form.phone_number.data, 
            email=form.email.data,
            male=form.male.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('已经成功注册')
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.patient_recorded')
        return redirect(next_page)
    return render_template('auth/register.html', title='Register',
                           form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))
