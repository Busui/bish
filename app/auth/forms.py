from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import BooleanField
from wtforms import SubmitField
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from flask_wtf.file import FileAllowed
from wtforms.validators import ValidationError
from wtforms.validators import DataRequired
from wtforms.validators import Email
from wtforms.validators import EqualTo

from app.models import User
from app.models import DoctorCode

class RegistrationForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    avatar = FileField('头像', validators=[FileAllowed(['png'], 'png Images only!')])
    phone_number = StringField('手机号', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    doctor_code = StringField('医生码')
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复输入密码', validators=[DataRequired(),
                                           EqualTo('password')])
    male = BooleanField('男的请打勾')
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被注册')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('该邮箱已被注册')
    
    def validate_phone_number(self, phone_number):
        phone_number = User.query.filter_by(phone_number=phone_number.data).first()
        if phone_number is not None:
            raise ValidationError('该手机已被注册')
    
    def validate_doctor_code(self, doctor_code):
        if doctor_code.data:
            doctorcode = DoctorCode.query.filter_by(code=doctor_code.data).first()
            print(doctorcode)
            if doctorcode:
                if doctorcode.is_use:
                    raise ValidationError('该医生码已被使用')
                else:
                    doctorcode.is_use = True
            else:
                raise ValidationError('该医生码无效')
        else:
            pass

class RegistrationUserForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired()])
    phone_number = StringField('手机号', validators=[DataRequired()])
    email = StringField('邮箱', validators=[DataRequired(), Email()])
    password = PasswordField('密码', validators=[DataRequired()])
    password2 = PasswordField(
        '重复输入密码', validators=[DataRequired(),
                                           EqualTo('password')])
    male = BooleanField('男的请打勾')
    submit = SubmitField('注册')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('该用户名已被注册')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('该邮箱已被注册')
    
    def validate_phone_number(self, phone_number):
        phone_number = User.query.filter_by(phone_number=phone_number.data).first()
        if phone_number is not None:
            raise ValidationError('该手机已被注册')
    
class LoginForm(FlaskForm):
    username = StringField('账号', validators=[DataRequired()])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我')
    submit = SubmitField('登入')