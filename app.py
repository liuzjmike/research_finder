import errno
import os

from flask import (Flask, redirect, render_template, send_from_directory,
                   url_for)
from flask_sqlalchemy import SQLAlchemy

import forms
import models

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})
try:
    os.makedirs(os.path.join(
        app.root_path, app.config['RESUME_FOLDER']))
except OSError as e:
    if e.errno != errno.EEXIST:
        raise


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignupForm()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            if models.People.contains(form.netid.data):
                form.netid.errors.append("User already exists.")
                return render_template('signup.html', form=form)
            if form.resume.data:
                resume_name = '%s.pdf' % form.netid.data
                form.resume.data.save(os.path.join(
                    app.root_path, app.config['RESUME_FOLDER'], resume_name))
            else:
                resume_name = None
            models.People.insert(
                form.netid.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.website.data,
                resume_name,
                form.password.data)
            models.Member.insert(
                form.netid.data,
                form.department1.data
            )
            if form.department2.data:
                models.Member.insert(
                    form.netid.data,
                    form.department2.data
                )
            interests = []
            for interest in form.interests.data.split(','):
                interest = interest.strip()
                if interest:
                    interests.append(interest)
            if interests:
                models.Interest.insert(
                    form.netid.data,
                    interests)

            if form.role.data == 'student':
                models.Student.insert(
                    form.netid.data,
                    form.status.data,
                    form.start_year.data)
            else:
                models.Faculty.insert(
                    form.netid.data,
                    form.title.data,
                    form.opening.data)
            return redirect(url_for('profile', netid=form.netid.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('signup.html', form=form)
    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        form.errors.pop('database', None)
        if not models.People.authenticate(form.netid.data, form.password.data):
            form.password.errors.append("Invalid NetID or password.")
            return render_template('login.html', form=form)
        return redirect(url_for('profile', netid=form.netid.data))
    else:
        return render_template('login.html', form=form)


@app.route('/profile/<netid>')
def profile(netid):
    if netid == -1:
        return redirect(url_for('login'))
    user = db.session.query(models.People) \
        .filter(models.People.netid == netid).one()
    return render_template('profile.html', user=user,
                           faculty=models.Faculty.get(netid),
                           student=models.Student.get(netid))


@app.route('/resume/<netid>')
def resume(netid):
    print(type(models.People.get(netid).resume))
    return send_from_directory(os.path.join(
        app.root_path, app.config['RESUME_FOLDER']), models.People.get(netid).resume)


@app.route('/edit-profile/<netid>', methods=['GET', 'POST'])
def edit_profile(netid):
    person = db.session.query(models.People)\
        .filter(models.People.netid == netid).one()
    student = models.Student.get(netid)
    if student:
        faculty = None
    else:
        faculty = models.Faculty.get(netid)
    form = forms.ProfileForm(person, faculty, student)

    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            if form.resume.data:
                resume_name = '%s.pdf' % netid
                form.resume.data.save(os.path.join(
                    app.root_path, app.config['RESUME_FOLDER'], resume_name))
            else:
                resume_name = person.resume
            models.People.edit(
                netid,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.website.data,
                resume_name,
                person.password
            )
            models.Member.query.filter_by(netid=netid).delete()
            models.Member.insert(
                netid,
                form.department1.data
            )
            if form.department2.data:
                models.Member.insert(
                    netid,
                    form.department2.data
                )
            interests = []
            for interest in form.interests.data.split(','):
                interest = interest.strip()
                if interest:
                    interests.append(interest)
            models.Interest.edit(
                netid,
                interests)

            if student:
                models.Student.edit(
                    netid,
                    form.status.data,
                    form.start_year.data
                )
            elif faculty:
                models.Faculty.edit(
                    netid,
                    form.title.data,
                    form.opening.data
                )
            return redirect(url_for('profile', netid=netid))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-profile.html', user=person, form=form)
    else:
        return render_template('edit-profile.html', user=person, form=form)


@app.route('/search', methods=['GET', 'POST'])
def search():
    form = forms.SearchForm()
    if form.validate_on_submit():
        try:
            query = db.session.query(models.People).join(models.Faculty)
            if form.name.data:
                q_str = '%' + form.name.data + '%'
                query = query.filter(db.or_(models.People.first_name.ilike(q_str),
                                            models.People.last_name.ilike(q_str)))
            if form.dept.data:
                query = query.join(models.People.departments).filter(
                    models.Member.dept_id == form.dept.data)
            if form.interest.data:
                query = query.join(models.People.interests).filter(
                    models.Interest.field == form.interest.data)
            query = query.order_by(models.People.last_name)
            return render_template(
                'results.html',
                matches=query.all())
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('search.html', form=form)
    else:
        return render_template('search.html', form=form)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
