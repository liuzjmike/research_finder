from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired


def signup():
    class F(FlaskForm):
        first_name = StringField()
        last_name = StringField()
        netid = StringField()
        email = StringField()
        password = StringField()
        department = StringField()
        website = StringField()
        role = RadioField('Professor or Student?', choices=[('professor', 'Professor'), ('student', 'Student')])
        title = StringField()
        status = StringField()
        start_year = StringField()
        opening = StringField()
    return F()


def login():
    class F(FlaskForm):
        netid = StringField()
        password = StringField()
    return F()
