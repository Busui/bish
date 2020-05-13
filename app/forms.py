from flask_wtf import FlaskForm
from wtforms import IntegerField
from wtforms import SubmitField
from wtforms.validators import DataRequired

class DoctorcodeForm(FlaskForm):
    count = IntegerField('医生码的数量', validators=[DataRequired(), ])
    submit = SubmitField('创建')