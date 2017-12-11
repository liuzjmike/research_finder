import itertools
import json

from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

import forms
import models

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app, session_options={'autocommit': False})


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

            models.People.insert(
                form.netid.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.website.data,
                form.resume.data,
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


@app.route('/edit-person/<netid>', methods=['GET', 'POST'])
def edit_person(netid):
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
            models.People.edit(
                netid,
                form.first_name.data,
                form.last_name.data,
                form.email.data,
                form.website.data,
                form.resume.data,
                person.password
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


@app.route('/profile/<netid>', methods=['GET', 'POST'])
def profile(netid):
    if netid==-1:
        return redirect(url_for('login')) 
    user = db.session.query(models.People)\
        .filter(models.People.netid == netid).one()
    return render_template('profile.html', user=user)


@app.route('/search-prof/<term>', methods=['GET', 'POST'])
def search_prof():
    results = []
    prof_netid = set()
    search_term = request.args.get('term')

    results_prof = db.session.query(models.Faculty).all()
    for prof in results_prof:
        prof_netid.add(prof['netid'])

    results_temp = []
    results_prof = db.session.query(models.People).filter(
        models.People.last_name.like(search_term + '%')).all()
    for prof in results_prof:
        if prof['netid'] in prof_netid:
            results_temp.append(prof['first_name'] + prof['last_name'])
            prof_netid.remove(prof['netid'])
    results_prof = db.session.query(models.People).filter(
        models.People.first_name.like(search_term + '%')).all()
    for prof in results_prof:
        if prof['netid'] in prof_netid:
            results_temp.append(prof['first_name'] + prof['last_name'])
            prof_netid.remove(prof['netid'])

    for i in range(min(5, len(results_temp))):
        results.append(results_temp[i])
    flattened = list(itertools.chain.from_iterable(results[0]))
    return flattened


@app.route('/search-dept/<term>', methods=['GET', 'POST'])
def search_dept():
    results = []
    dept_name = set()
    search_term = request.args.get('term')

    results_dept = db.session.query(models.Member).all()
    for dept in results_dept:
        dept_name.add(dept['name'])

    results_temp = []
    results_dept = db.session.query(models.Member).filter(
        models.Member.name.like(search_term + '%')).all()
    for dept in results_dept:
        if dept['name'] in dept_name:
            results_temp.append(dept['name'])
            dept_name.remove(dept['name'])

    for i in range(min(5, len(results_temp))):
        results.append(results_temp[i])
    flattened = list(itertools.chain.from_iterable(results[0]))
    return flattened


@app.route('/search-interests/<term>', methods=['GET', 'POST'])
def search_interests():
    results = []
    field = set()
    search_term = request.args.get('term')

    results_interest = db.session.query(models.Interest).all()
    for interest in results_interest:
        field.add(interest['field'])

    results_temp = []
    results_interest = db.session.query(models.Interest).filter(
        models.Interest.field.like(search_term + '%')).all()
    for interest in results_interest:
        if interest['field'] in field:
            results_temp.append(interest['field'])
            field.remove(interest['field'])

    for i in range(min(5, len(results_temp))):
        results.append(results_temp[i])
    flattened = list(itertools.chain.from_iterable(results[0]))
    return flattened


@app.route('/search')
def search():
    form = forms.SearchForm()
    if form.validate_on_submit():
        try:
            matches = []
            name = form.name.data
            dept = form.dept.data
            interests = form.interests.data

            netid_set = set()
            profs = db.session.query(models.Faculty).all()
            for prof in profs:
                netid_set.add(prof['netid'])

            # search by prof
            profs = set()
            users = db.session.query(models.People).filter(
                models.People.last_name == name).all()
            for user in users:
                profs.add(user['netid'])
            users = db.session.query(models.People).filter(
                models.People.first_name == name).all()
            for user in users:
                profs.add(user['netid'])
            for prof in profs:
                if prof in netid_set:
                    matches.append(db.session.query(models.People).filter(models.People.netid == prof).one())
                    netid_set.remove(prof)

            # search by dept
            users_in_dept = db.session.query(models.Member).filter(models.Member.name == dept).all()
            valid_profs = set()
            for user in users_in_dept:
                if user['netid'] in netid_set:
                    valid_profs.add(user['netid'])
            for prof_netid in valid_profs:
                user = db.session.query(models.People).filter(models.People.netid == prof_netid).one()
                matches.append(user)
                netid_set.remove(prof_netid)

            # search by interests
            users_in_interests = db.session.query(models.Interest).filter(models.Interest.field == interests).all()
            valid_profs = set()
            for user in users_in_dept:
                if user['netid'] in netid_set:
                    valid_profs.add(user['netid'])
            for prof_netid in valid_profs:
                user = db.session.query(models.People).filter(models.People.netid == prof_netid).one()
                matches.append(user)
                netid_set.remove(prof_netid)

            # sort the matches
            sorted_results = sorted(matches, key = matches.last_name)
            return render_template('search_results.html', matches=sorted_results)
        except BaseException as e:
            form1.errors['database'] = str(e)
            return render_template('searchpage.html')
    else:
        return render_template('searchpage.html', form=form)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
