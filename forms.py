from flask_wtf import FlaskForm
from wtforms import FileField, IntegerField, PasswordField, RadioField, StringField
from wtforms.validators import DataRequired, Email, EqualTo, \
    Optional, StopValidation, TextAreaField, URL, ValidationError


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
    title = StringField('Title')
    opening = IntegerField('Opening')
    status = StringField('Status')
    start_year = IntegerField('Start Year')

    def validate_title(form, field):  # pylint: disable=E0213
        if form.role.data == 'faculty' and field.data not in \
                ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer']:
            raise ValidationError(
                'Title must be in [Professor, Associate Professor, Assistant Professor, Lecturer]')

    def validate_opening(form, field):  # pylint: disable=E0213
        if form.role.data == 'faculty':
            DataRequired()(form, field)

    def validate_status(form, field):  # pylint: disable=E0213
        if form.role.data == 'student' and field.data not in \
                ['Undergraduate', 'Master', 'PhD', 'Post-Doc']:
            raise ValidationError(
                'Title must be in [Undergraduate, Master, PhD, Post-Doc]')

    def validate_year(form, field):  # pylint: disable=E0213
        if form.role.data == 'student':
            if not field.data:
                raise StopValidation('Required Field.')
            if field.data < 1838:
                raise ValidationError(
                    'Start year cannot be earlier than 1838.')


class LoginForm(FlaskForm):
    netid = StringField('NetID', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


def ProfileForm(person, faculty=None, student=None):
    int_fields = [interest.field for interest in person.interests]

    class F(FlaskForm):
        netid = StringField('NetID', [DataRequired()], default=person.netid)
        first_name = StringField(
            'First Name', [DataRequired()], default=person.first_name)
        last_name = StringField(
            'Last Name', [DataRequired()], default=person.last_name)
        email = StringField(
            'Email', [DataRequired(), Email()], default=person.email)
        interests = TextAreaField('Interests', default=', '.join(int_fields))
        department1 = StringField('Department 1', [DataRequired()])
        department2 = StringField('Department 2')
        website = StringField(
            'Website', [Optional(), URL()], default=person.website)
        resume = FileField('Resume', default=person.resume)

    if faculty:
        setattr(F, 'title', StringField('Title', default=faculty.title))
        setattr(F, 'opening', IntegerField('Opening', default=faculty.opening))
    if student:
        setattr(F, 'status', StringField('Status', default=student.status))
        setattr(F, 'start_year', IntegerField(
            'Start Year', default=student.start_year))
    return F()


class SearchForm(FlaskForm):
    department = StringField('Department')
    faculty = StringField('Faculty')
    interest = StringField('Interest')
