from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import IntegerField, PasswordField, RadioField, \
    SelectField, StringField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, \
    Optional, URL, ValidationError


data_required = DataRequired()
optional = Optional()


def validate_title(form, field):
    if form.role.data == 'faculty' and field.data not in \
            ['Professor', 'Associate Professor', 'Assistant Professor', 'Lecturer']:
        raise ValidationError(
            'Title must be in [Professor, Associate Professor, Assistant Professor, Lecturer]')


def validate_opening(form, field):
    if form.role.data == 'faculty':
        data_required(form, field)
    else:
        optional(form, field)


def validate_status(form, field):
    if form.role.data == 'student' and field.data not in \
            ['Undergraduate', 'Master', 'PhD', 'Post-Doc']:
        raise ValidationError(
            'Status must be in [Undergraduate, Master, PhD, Post-Doc]')


def validate_start_year(form, field):
    if form.role.data == 'student':
        data_required(form, field)
        if field.data < 1838:
            raise ValidationError(
                'Start year cannot be earlier than 1838.')
    else:
        optional(form, field)


def validate_department2(form, field):
    if field.data == form.department1.data:
        raise ValidationError('Department1 and Department2 must be different.')


class SignupForm(FlaskForm):
    netid = StringField('NetID', [data_required])
    first_name = StringField('First Name', [data_required])
    last_name = StringField('Last Name', [data_required])
    email = StringField('Email', [data_required, Email()])
    password = PasswordField('Password', [data_required])
    confirm = PasswordField(
        'Confirm Password', [data_required,
                             EqualTo('password', message='Passwords must match')])
    department1 = StringField('Department 1', [data_required])
    department2 = StringField(
        'Department 2', [optional, validate_department2])
    website = StringField('Website', [optional, URL()])
    resume = FileField('Resume')
    role = RadioField(
        'Role', [data_required], choices=[('faculty', 'Faculty'), ('student', 'Student')])
    title = SelectField('Title', [validate_title],
                        choices=[('N/A', '--'),
                                 ('Professor', 'Professor'),
                                 ('Associate Professor', 'Associate Professor'),
                                 ('Assistant Professor', 'Assistant Professor'),
                                 ('Lecturer', 'Lecturer')])
    opening = IntegerField('Opening', [validate_opening])
    status = SelectField("Academic Status", [validate_status],
                         choices=[('N/A', '--'),
                                  ('Undergraduate', 'Undergraduate'),
                                  ('Master', 'Master'),
                                  ('PhD', 'PhD'),
                                  ('Post-Doc', 'Post-Doc')])
    start_year = IntegerField('Start Year', [validate_start_year])


class LoginForm(FlaskForm):
    netid = StringField('NetID', [data_required])
    password = PasswordField('Password', [data_required])


def ProfileForm(person, faculty=None, student=None):
    int_fields = [interest.field for interest in person.interests]
    if faculty:
        role_default = 'faculty'
    elif student:
        role_default = 'student'
    else:
        role_default = None

    class F(FlaskForm):
        netid = StringField('NetID', [data_required], default=person.netid)
        first_name = StringField(
            'First Name', [data_required], default=person.first_name)
        last_name = StringField(
            'Last Name', [data_required], default=person.last_name)
        email = StringField(
            'Email', [data_required, Email()], default=person.email)
        # interests = TextAreaField('Interests', default=', '.join(int_fields))
        interests = TextAreaField('Interests', default=', '.join(int_fields))
        department1 = StringField('Department 1', [data_required], default=person.departments[0].dept_id)
        department2 = StringField(
            'Department 2', [optional, validate_department2], default=person.departments[1].dept_id if len(person.departments)>1 else None)
        website = StringField(
            'Website', [optional, URL()], default=person.website)
        resume = FileField('Resume', default=person.resume)
        role = RadioField('Role', [data_required],
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


class SearchForm(FlaskForm):
    department = StringField('Department')
    faculty = StringField('Faculty')
    interest = StringField('Interest')
