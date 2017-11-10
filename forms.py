from flask_wtf import FlaskForm
from wtforms import StringField, RadioField
from wtforms.validators import DataRequired

class SignUpFormFactory:
    @staticmethod
    def signup():
        class F(FlaskForm):
            first_name = StringField()
            last_name = StringField()
            netid = StringField()
            email = StringField()
            password = StringField()
            major = StringField()
            interests = StringField()
            website = StringField()
            member = RadioField('Professor or Student?', choices=[('professor','Professor'),('student','Student')])
            title = StringField()
            status = StringField()
            start_year = StringField()
            opening = StringField()
        return F()
    @staticmethod
    def login():
        class F(FlaskForm):
            email = StringField()
            password = StringField()
        return F()
