from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, PasswordField, RadioField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, \
    Optional, StopValidation, TextAreaField, URL, ValidationError


def validate_title(form, field):
    if form.role.data == 'faculty' and field.data not in \
            ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer']:
        raise ValidationError(
            'Title must be in [Professor, Associate Professor, Assistant Professor, Lecturer]')


def validate_opening(form, field):
    if form.role.data == 'faculty':
        DataRequired()(form, field)


def validate_status(form, field):
    if form.role.data == 'student' and field.data not in \
            ['Undergraduate', 'Master', 'PhD', 'Post-Doc']:
        raise ValidationError(
            'Title must be in [Undergraduate, Master, PhD, Post-Doc]')


def validate_start_year(form, field):
    if form.role.data == 'student':
        if not field.data:
            raise StopValidation('Required Field.')
        if field.data < 1838:
            raise ValidationError(
                'Start year cannot be earlier than 1838.')


class SignupForm(FlaskForm):
    netid = StringField('NetID', [DataRequired()])
    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired()])
    confirm = PasswordField(
        'Confirm Password', [DataRequired(),
                             EqualTo('password', message='Passwords must match')])
    department1 = StringField('Department 1', [DataRequired()])
    department2 = StringField('Department 2')
    website = StringField('Website', [Optional(), URL()])
    resume = FileField('Resume')
    role = RadioField(
        'Role', [DataRequired()], choices=[('faculty', 'Faculty'), ('student', 'Student')])
    title = StringField('Title', [validate_title])
    opening = IntegerField('Opening', [validate_opening])
    status = StringField('Status', [validate_status])
    start_year = IntegerField('Start Year', [validate_start_year])


class LoginForm(FlaskForm):
    netid = StringField('NetID', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


def ProfileForm(person, faculty=None, student=None):
    int_fields = [interest.field for interest in person.interests]
    if faculty:
        role_default = 'faculty'
    elif student:
        role_default = 'student'
    else:
        role_default = None

    class F(FlaskForm):
        netid = StringField('NetID', [DataRequired()], default=person.netid)
        first_name = StringField(
            'First Name', [DataRequired()], default=person.first_name)
        last_name = StringField(
            'Last Name', [DataRequired()], default=person.last_name)
        email = StringField(
            'Email', [DataRequired(), Email()], default=person.email)
        interests = TextAreaField('Interests', default=', '.join(int_fields))
        # TODO: Set default for departments
        department1 = StringField('Department 1', [DataRequired()])
        department2 = StringField('Department 2')
        website = StringField(
            'Website', [Optional(), URL()], default=person.website)
        resume = FileField('Resume', default=person.resume)
        role = RadioField('Role', [DataRequired()],
                          choices=[('faculty', 'Faculty'),
                                   ('student', 'Student')],
                          default=role_default)
        title = StringField('Title', [validate_title],
                            default=faculty.title if faculty else None)
        opening = IntegerField('Opening', [validate_opening],
                               default=faculty.opening if faculty else None)
        status = StringField('Status', [validate_status],
                             default=student.status if student else None)
        start_year = IntegerField('Start Year', [validate_start_year],
                                  default=student.start_year if student else None)
    return F()

<<<<<<< HEAD
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
=======

class SearchForm(FlaskForm):
    department = StringField('Department')
    faculty = StringField('Faculty')
    interest = StringField('Interest')
>>>>>>> 91958e88cd2bfdb47bad79c49ad8fb3c0a9d9dae
