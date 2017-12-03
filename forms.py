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

class ProfileEdit:
    def form(person, isStudent):
        class F(FlaskForm):
            first_name = StringField(default=person.first_name)
            last_name = StringFiled(default=person.last_name)
            netid = StringField(default=person.netid)
            email = StringField(default=person.email)
            password = StringField()
            confirmPassword = StringField()
            if isStudent:
                # get student object
                student = db.session.query(models.Student)\
                    .filter(models.Student.netid == person.netid)
                status = StringField(default=student.status)
                start_year = StringField(default=student.start_year)
            else:
                faculty = db.session.query(models.Faculty)\
                    .filter(models.Faculty.netid == person.netid)
                title = StringField(default=faculty.title)
                opening = StringField(default=faculty.opening)

            interests = db.session.query(models.Interest)\
                .filter(models.Interest.netid == person.netid).all()
            interest_list = ''
            for field in interests:
                interest_list += field
                interest_list += '\n'
            interest_text = StringField(default=interest_list)
            return F()
