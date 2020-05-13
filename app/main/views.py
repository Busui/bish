from app.main import main_bp
from flask import render_template
from flask import url_for
from flask import current_app
from flask import redirect
from flask import request
from flask import flash
from werkzeug.urls import url_parse
from flask_login import login_required
from flask_login import current_user
from app.models import User
from .forms import SearchUserForm


@main_bp.route('/')
def index():
    return render_template('main/index.html')

@main_bp.route('/home')
def home():
    return 'home'

@main_bp.route('/doctor_profile', methods=['GET', 'POST'])
@login_required
def doctor_profile():
    return render_template('main/doctor_profile.html', avatar_url = url_for('static', filename = current_user.avatar))


@main_bp.route('/user_profile', methods=['GET', 'POST'])
@login_required
def user_profile():
    return render_template('main/user_profile.html', avatar_url = url_for('static', filename = current_user.avatar))

@main_bp.route('/patient_recorded', methods=['GET', 'POST'])
@login_required
def patient_recorded():
    '''
    1. 展示用户列表：
        1.2 已服务过的用户
    2. 手动输入病人（手机号，姓名）
        2.1 用户不存在？医生帮忙新建用户，提供初始化密码
    3. 病人信息录入
    '''
    patients = current_user.load_users()
    print(patients)
    return render_template('main/patient_recorded.html', patients = patients)

@main_bp.route('/search_user', methods=['GET', 'POST'])
@login_required
def search_user():
    form = SearchUserForm()
    if form.validate_on_submit():
        patient = User.query.filter_by(username = form.user_input.data).first()
        if not patient:
            patient = User.query.filter_by(phone_number = form.user_input.data).first()
        if patient:
            return render_template('main/show_search_result.html', patient = patient)
        flash('用户不存在，请注册！')
        return redirect(url_for('auth.register_user'))
    return render_template('main/search_user.html', form = form)

@main_bp.route('/load_doctors', methods=['GET'])
@login_required
def load_doctors():
    doctors = current_user.load_doctors()
    return render_template('main/load_doctors.html', doctors=doctors)
