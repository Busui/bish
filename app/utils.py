from random import choice
from string import ascii_uppercase as uc, digits as dg

from flask import current_app
from flask import request
from flask import redirect
from flask import url_for
from flask_login import current_user
from flask_admin.contrib.sqla import ModelView
from flask_admin import expose
from flask_admin import BaseView
from wtforms.validators import ValidationError

from app.models import DoctorCode
from app.forms import DoctorcodeForm
from app import db

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

class UserModelView(ModelView):
    page_size = 50
    can_view_details = True
    can_create = False
    can_edit = False
    column_exclude_list = ['password_hash', 'avatar',]
    column_editable_list = ['username', 'phone_number', 'email', 'male', 'doctor']

    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index', next=request.url))

class DoctorModelView(ModelView):
    page_size = 50
    can_view_details = True
    can_create = False
    can_edit = False
    column_exclude_list = ['password_hash', 'avatar',]
    column_editable_list = ['username', 'phone_number', 'email', 'male', ]

    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index', next=request.url))

class DoctorCodeModelView(ModelView):
    page_size = 50
    can_view_details = True
    can_create = True
    can_edit = True
    column_editable_list = ['is_use', ]

    @expose('/new/', methods=('GET', 'POST'))
    def create_view(self):
        form = DoctorcodeForm()
        if form.validate_on_submit():
            count = form.count.data
            for code in activation_code(count):
                if not DoctorCode.is_set(code):
                    doctor_code = DoctorCode(code=code)
                    db.session.add(doctor_code)
            db.session.commit()
            return redirect(url_for('doctorcode.index_view'))
        return self.render('admin/create_doctorcode.html', form=form)

    def is_accessible(self):
        return current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('main.index', next=request.url))

def activation_code(count):
    for i in range(count):
        part1 = ''.join(choice(uc) for j in range(3))   # 三个大写的英文
        part2 = ''.join(choice(dg) for j in range(3))   # 三个随机数字
        part3 = ''.join(choice(dg + uc) for j in range(4)) # 四个随机大写字母或者数字
        yield part1 + part2 + part3
