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

class BaseInfoForm(FlaskForm):
    username = StringField("姓名", validators=[DataRequired()])

class SearchUserForm(FlaskForm):
    user_input = StringField("姓名或手机号", validators=[DataRequired()])
    submit = SubmitField("搜索")