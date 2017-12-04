from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import models
import forms

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})


@app.route('/')
def all_drinkers():
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = forms.SignupForm()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)

            # TODO: Deal with existing user
            # if models.People.has_user(form.netid.data):
            #     return render_template('signup.html', form=form)

            models.People.insert(
                form.netid.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.website.data,
                form.resume.data,
                form.password)

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
    form = forms.SignupForm()
    if form.validate_on_submit():
        form.errors.pop('database', None)
        if not models.People.authenticate(form.netid.data, form.password.data):
            # TODO: add error
            return render_template('login.html', form=form)
        return redirect(url_for('profile', netid=form.netid.data))
    else:
        return render_template('login.html', form=form)


@app.route('/edit-person/<netid>', methods=['GET', 'POST'])
def edit_person(netid):
    person = db.session.query(models.People)\
        .filter(models.People.netid == netid).one()
    student = models.Student.get(netid)
    if student:
        faculty = None
    else:
        faculty = models.Faculty.get(netid)
    form = forms.ProfileForm(person, student, faculty)

    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.People.edit(
                netid,
                form.netid.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.website.data,
                form.resume.data,
                form.password.data
            )

            # TODO: Update interests
            # models.Interest.edit(
            #     netid,
            #     form.get_interests()
            # )

            if student:
                models.Student.edit(
                    netid,
                    form.status,
                    form.start_year
                )
            elif faculty:
                models.Faculty.edit(
                    netid,
                    form.title,
                    form.opening
                )
            return redirect(url_for('profile', netid=netid))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('edit-profile.html', netid=netid, form=form)
    else:
        return render_template('edit-profile.html', netid=netid, form=form)


@app.route('/search')
def search():
    form = forms.SearchForm()
    if form.validate_on_submit():
        try:
            return redirect(url_for('search-results',
                                    dept=form.department_name.data,
                                    interests=form.interests.data,
                                    professor=form.professor_name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('search.html')
    return render_template('search.html')


@app.route('/search-results')
def search_results(dept, interests, professor):
    pass


@app.route('/profile/<netid>', methods=['GET', 'POST'])
def profile(netid):
    user = db.session.query(models.People)\
        .filter(models.People.netid == netid).one()
    return render_template('profile.html', user=user)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
