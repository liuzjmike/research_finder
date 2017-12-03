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
    form = forms.SignUpFormFactory.signup()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            if models.People.has_user(form.netid.data):
                return render_template('signup.html', form=form)

            models.People.insert(
                form.netid.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.password)
            # TODO: check if student or professor and store in the appropriate table

            if form.member.data == 'student':
                # TODO: figure out how to add resume
                models.Student.insert(
                    form.netid.data,
                    form.status.data,
                    form.start_year.data,
                    form.resume.data)
            else:
                models.Faculty.insert(
                    form.netid.data,
                    form.title.data,
                    form.opening.data,
                    form.website.data)

            # TODO: redirect to profile page
            return redirect(url_for('profile.html', netid=form.netid.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('signup.html', form=form)
    else:
        return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.SignUpFormFactory.login()
    if form.validate_on_submit():
        form.errors.pop('database', None)
        if not models.People.authenticate(form.netid.data, form.password.data):
            # TODO: add error
            return render_template('login.html', form=form)

        # TODO: redirect to profile page
        return redirect(url_for('profile.html', netid=form.netid.data))
    else:
        return render_template('login.html', form=form)

@app.route('/edit-person/<netid>', methods=['GET', 'POST'])
def edit_person(netid):
    isStudent = models.Student.has_user(netid)
    form = forms.ProfileEdit.form(netid)

    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)
            models.People.edit(
                netid,
                form.netid.data,
                form.first_name.data,
                form.last_name.data,
                form.password.data,
                form.email.data
            )
            models.Interest.edit(
                netid,
                form.get_interests()
            )

            if isStudent:
                models.Student.edit(
                    netid,
                    form.status,
                    form.start_year
                )
            else:
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
    return render_template('search.html')

@app.route('/profile/<netid>' , methods=['GET', 'POST'])
def profile(netid):
    user = db.session.query(models.People)\
        .filter(models.People.netid == netid).one()
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
