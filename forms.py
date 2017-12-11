from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (IntegerField, PasswordField, RadioField, SelectField,
                     StringField, TextAreaField)
from wtforms.validators import (URL, DataRequired, Email, EqualTo, Optional,
                                ValidationError)

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
    interests = TextAreaField('Interests')
    website = StringField('Website', [optional, URL()])
    resume = FileField('Resume', [FileAllowed(['pdf'])])
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
    departments = sorted([dept.dept_id for dept in person.departments])
    int_fields = sorted([interest.field for interest in person.interests])
    if faculty:
        role_default = 'faculty'
    elif student:
        role_default = 'student'
    else:
        role_default = None

    class F(FlaskForm):
        first_name = StringField(
            'First Name', [data_required], default=person.first_name)
        last_name = StringField(
            'Last Name', [data_required], default=person.last_name)
        password = PasswordField('Password', [data_required])
        confirm = PasswordField(
        'Confirm Password', [data_required,
                             EqualTo('password', message='Passwords must match')])
        email = StringField(
            'Email', [data_required, Email()], default=person.email)
        interests = TextAreaField('Interests', default=', '.join(int_fields))
        department1 = StringField('Department 1',
                                  [data_required],
                                  default=departments[0] if person.departments else None)
        department2 = StringField(
            'Department 2', [optional, validate_department2],
            default=departments[1] if len(departments) > 1 else None)
        interests = TextAreaField('Interests', default=', '.join(int_fields))
        website = StringField(
            'Website', [optional, URL()], default=person.website)
        resume = FileField('Resume', [FileAllowed(['pdf'])])
        role = RadioField('Role', [data_required],
                          choices=[('faculty', 'Faculty'),
                                   ('student', 'Student')],
                          default=role_default)
        title = SelectField('Title', [validate_title],
                            choices=[('N/A', '--'),
                                     ('Professor', 'Professor'),
                                     ('Associate Professor',
                                      'Associate Professor'),
                                     ('Assistant Professor',
                                      'Assistant Professor'),
                                     ('Lecturer', 'Lecturer')],
                            default=faculty.title if faculty else None)
        opening = IntegerField('Opening', [validate_opening],
                               default=faculty.opening if faculty else None)
        status = SelectField("Academic Status", [validate_status],
                             choices=[('N/A', '--'),
                                      ('Undergraduate', 'Undergraduate'),
                                      ('Master', 'Master'),
                                      ('PhD', 'PhD'),
                                      ('Post-Doc', 'Post-Doc')],
                             default=student.status if student else None)
        start_year = IntegerField('Start Year', [validate_start_year],
                                  default=student.start_year if student else None)
    return F()


class SearchForm(FlaskForm):
    dept = StringField('Department')
    name = StringField('Professor Name')
    interest = StringField('Interests')
