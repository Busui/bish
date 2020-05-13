"""first

Revision ID: 1ab26c57aa4f
Revises: 
Create Date: 2020-05-11 22:35:56.045543

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ab26c57aa4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('doctor_code',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('code', sa.String(length=16), nullable=True),
    sa.Column('is_use', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_doctor_code_code'), 'doctor_code', ['code'], unique=True)
    op.create_index(op.f('ix_doctor_code_is_use'), 'doctor_code', ['is_use'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('doctor_code', sa.String(length=16), nullable=True),
    sa.Column('doctor', sa.Boolean(), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('avatar', sa.String(length=256), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('phone_number', sa.String(length=24), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('title', sa.String(length=512), nullable=True),
    sa.Column('about_me', sa.Text(), nullable=True),
    sa.Column('male', sa.Boolean(), nullable=True),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('job', sa.String(length=64), nullable=True),
    sa.Column('last_seen', sa.DateTime(), nullable=True),
    sa.Column('blood_type', sa.String(length=8), nullable=True),
    sa.Column('marital_status', sa.String(length=8), nullable=True),
    sa.Column('blood_sugar', sa.Integer(), nullable=True),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('blood_pressure', sa.String(length=32), nullable=True),
    sa.Column('work_unit', sa.String(length=256), nullable=True),
    sa.Column('home_address', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_doctor_code'), 'user', ['doctor_code'], unique=True)
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_phone_number'), 'user', ['phone_number'], unique=True)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('case',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('casename', sa.String(length=256), nullable=True),
    sa.Column('username', sa.String(length=64), nullable=True),
    sa.Column('doctor_name', sa.String(length=64), nullable=True),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('past_medical_history', sa.String(length=512), nullable=True),
    sa.Column('others_past_medical_history', sa.String(length=128), nullable=True),
    sa.Column('hereditary_disease', sa.String(length=512), nullable=True),
    sa.Column('others_hereditary_disease', sa.String(length=128), nullable=True),
    sa.Column('is_allergy', sa.Boolean(), nullable=True),
    sa.Column('allergy_source', sa.Text(), nullable=True),
    sa.Column('allergy_feature', sa.Text(), nullable=True),
    sa.Column('operation', sa.Text(), nullable=True),
    sa.Column('is_eating_habit_health', sa.Boolean(), nullable=True),
    sa.Column('eating_habit_detials', sa.Text(), nullable=True),
    sa.Column('eating_specials', sa.String(length=256), nullable=True),
    sa.Column('eating_flavor', sa.String(length=256), nullable=True),
    sa.Column('drink_frequency', sa.String(length=32), nullable=True),
    sa.Column('wine_age', sa.Integer(), nullable=True),
    sa.Column('drink_intake_daily', sa.Integer(), nullable=True),
    sa.Column('dring_specials', sa.String(length=64), nullable=True),
    sa.Column('smoking', sa.String(length=64), nullable=True),
    sa.Column('smoking_age', sa.Integer(), nullable=True),
    sa.Column('smoking_intake_daily', sa.Integer(), nullable=True),
    sa.Column('time_to_fall_asleep', sa.String(length=64), nullable=True),
    sa.Column('time_to_get_up', sa.String(length=64), nullable=True),
    sa.Column('poop', sa.Text(), nullable=True),
    sa.Column('pee', sa.Text(), nullable=True),
    sa.Column('menstrual_time', sa.String(length=64), nullable=True),
    sa.Column('menstrual_cycle', sa.Text(), nullable=True),
    sa.Column('menstrual_flow', sa.String(length=32), nullable=True),
    sa.Column('has_child', sa.Boolean(), nullable=True),
    sa.Column('female_others_symptom', sa.Text(), nullable=True),
    sa.Column('male_others_symptom', sa.Text(), nullable=True),
    sa.Column('physique_health_plan', sa.Text(), nullable=True),
    sa.Column('chinese_medicine_suggestions', sa.Text(), nullable=True),
    sa.Column('chronic_health_plan', sa.Text(), nullable=True),
    sa.Column('physique', sa.String(length=256), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_case_casename'), 'case', ['casename'], unique=False)
    op.create_index(op.f('ix_case_doctor_name'), 'case', ['doctor_name'], unique=False)
    op.create_index(op.f('ix_case_username'), 'case', ['username'], unique=False)
    op.create_table('experience',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('followers',
    sa.Column('patient_id', sa.Integer(), nullable=True),
    sa.Column('doctor_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['doctor_id'], ['user.id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['user.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('followers')
    op.drop_table('experience')
    op.drop_index(op.f('ix_case_username'), table_name='case')
    op.drop_index(op.f('ix_case_doctor_name'), table_name='case')
    op.drop_index(op.f('ix_case_casename'), table_name='case')
    op.drop_table('case')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_phone_number'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_index(op.f('ix_user_doctor_code'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_doctor_code_is_use'), table_name='doctor_code')
    op.drop_index(op.f('ix_doctor_code_code'), table_name='doctor_code')
    op.drop_table('doctor_code')
    # ### end Alembic commands ###
