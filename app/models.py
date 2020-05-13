from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from datetime import datetime
from flask import current_app
from flask_login import current_user

from app import db
from app import login


# 辅助表
relationships = db.Table('followers',
    db.Column('patient_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('doctor_id', db.Integer, db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    doctor_code = db.Column(db.String(16), index=True, unique=True)
    doctor = db.Column(db.Boolean, default=False)
    experiences = db.relationship('Experience', backref='user', lazy=True)
    username = db.Column(db.String(64), index=True, unique=True)
    avatar = db.Column(db.String(256))
    email = db.Column(db.String(120), index=True, unique=True)
    phone_number = db.Column(db.String(24), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    title = db.Column(db.String(512))   # 获得称号
    about_me = db.Column(db.Text)
    male = db.Column(db.Boolean)
    age = db.Column(db.Integer)
    job = db.Column(db.String(64))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    blood_type = db.Column(db.String(8))
    marital_status = db.Column(db.String(8))
    blood_sugar = db.Column(db.Integer)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    blood_pressure = db.Column(db.String(32))
    work_unit = db.Column(db.String(256))
    home_address = db.Column(db.String(256))
    cases = db.relationship('Case', backref='user', lazy=True)
    doctors = db.relationship(
        'User', secondary=relationships,
        primaryjoin=(relationships.c.patient_id == id),
        secondaryjoin=(relationships.c.doctor_id == id),
        backref=db.backref('patients', lazy='dynamic'), lazy='dynamic')

    @property
    def is_doctor(self):
        return self.doctor

    def load_doctors(self):
        return User.query.filter_by(doctor=True).all()
    
    def load_users(self):
        return User.query.filter_by(doctor=False).all()
    
    def follow(self, user):
        if not self.is_following(user):
            self.doctors.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.doctors.remove(user)

    def is_following(self, user):
        return self.doctors.filter(
            relationships.c.doctor_id == user.id).count() > 0

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_username(self):
        return self.username

    @property
    def is_admin(self):
        return current_user.get_username() == current_app.config.get('FLASK_ADMIN')

    def __repr__(self):
        if self.doctor:
            response = '<Doctor {}>'.format(self.username)    
        else:
            response = '<User {}>'.format(self.username)
        return response


class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    doctor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# 医生通过病人获取病历
class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    casename= db.Column(db.String(256), index=True)
    username = db.Column(db.String(64), index=True)
    doctor_name = db.Column(db.String(64), index=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    past_medical_history = db.Column(db.String(512))
    others_past_medical_history = db.Column(db.String(128))
    hereditary_disease = db.Column(db.String(512))
    others_hereditary_disease = db.Column(db.String(128))
    is_allergy = db.Column(db.Boolean)
    allergy_source = db.Column(db.Text)
    allergy_feature = db.Column(db.Text)
    operation = db.Column(db.Text)
    is_eating_habit_health = db.Column(db.Boolean)
    eating_habit_detials = db.Column(db.Text)
    eating_specials = db.Column(db.String(256))
    eating_flavor = db.Column(db.String(256))
    drink_frequency = db.Column(db.String(32))
    wine_age = db.Column(db.Integer)
    drink_intake_daily = db.Column(db.Integer)
    dring_specials = db.Column(db.String(64))
    smoking = db.Column(db.String(64))
    smoking_age = db.Column(db.Integer)
    smoking_intake_daily = db.Column(db.Integer)
    time_to_fall_asleep = db.Column(db.String(64))
    time_to_get_up = db.Column(db.String(64))
    symptom = db.String(db.String(256))
    poop = db.Column(db.Text)
    pee = db.Column(db.Text)
    menstrual_time = db.Column(db.String(64))
    menstrual_cycle = db.Column(db.Text)
    menstrual_flow = db.Column(db.String(32))
    menstrual_color = db.String(db.String(64))
    has_child = db.Column(db.Boolean)
    female_others_symptom = db.Column(db.Text)
    male_others_symptom = db.Column(db.Text)
    physique_health_plan = db.Column(db.Text)
    chinese_medicine_suggestions = db.Column(db.Text)
    chronic_health_plan = db.Column(db.Text)
    physique = db.Column(db.String(256))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)


class DoctorCode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16), index=True, unique=True)
    is_use = db.Column(db.Boolean, index=True, default=False)

    def is_set(code):
        return DoctorCode.query.get(code)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))