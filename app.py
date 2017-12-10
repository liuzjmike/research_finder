from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy

import models
import forms
import itertools

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

            # TODO: Deal with existing user
            # if models.People.has_user(form.netid.data):
            #     return render_template('signup.html', form=form)
            # TODO: Add Member row

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
            return render_template('edit-profile.html', user=person, form=form)
    else:
        return render_template('edit-profile.html', user=person, form=form)


@app.route('/profile/<netid>', methods=['GET', 'POST'])
def profile(netid):
    user = db.session.query(models.People)\
        .filter(models.People.netid == netid).one()
    return render_template('profile.html', user=user)


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
            return render_template('searchpage.html')
    return render_template('searchpage.html')

@app.route('/search-prof/<term>', methods=['GET', 'POST'])
def search-prof():
    results = []
    prof_netid = set()
    search_term = request.args.get('term')

    results_prof = db.session.query(models.Faculty).all()
    for prof in results_prof:
        prof_netid.add(prof['netid'])

    results_temp = []
    results_prof = db.session.query(models.People).filter(People.last_name.like('%' + search_term + '%')).all()
    for prof in results_prof:
        if prof['netid'] in prof_netid:
            results_temp.append(prof['first_name'] + prof['last_name'])
            prof_netid.remove(prof['netid'])
    results_prof = db.session.query(models.People).filter(People.first_name.like('%' + search_term + '%')).all()
    for prof in results_prof:
        if prof['netid'] in prof_netid:
            results_temp.append(prof['first_name'] + prof['last_name'])
            prof_netid.remove(prof['netid'])

    for i in min(range(5), len(results_temp))
        results.append(results_temp[i])
    flattened = list(itertools.chain.from_iterable(result[0]))
    return flattened

@app.route('/search-dept/<term>', methods=['GET', 'POST'])
def search-dept():
    results = []
    dept_name = set()
    search_term = request.args.get('term')

    results_dept = db.session.query(models.Member).all()
    for dept in results_dept:
        dept_name.add(dept['name'])

    results_temp = []
    results_dept = db.session.query(models.Member).filter(Member.name.like('%' + search_term + '%')).all()
    for dept in results_dept:
        if dept['name'] in dept_name:
            results_temp.append(dept['name'])
            dept_name.remove(dept['name'])

    for i in min(range(5), len(results_temp))
        results.append(results_temp[i])
    flattened = list(itertools.chain.from_iterable(result[0]))
    return flattened

@app.route('/search-interests/<term>', methods=['GET', 'POST'])
def search-interests():
    results = []
    field = set()
    search_term = request.args.get('term')

    results_interest = db.session.query(models.Interest).all()
    for interest in results_interest:
        field.add(interest['field'])

    results_temp = []
    results_interest = db.session.query(models.Interest).filter(Interest.field.like('%' + search_term + '%')).all()
    for interest in results_interest:
        if interest['field'] in field:
            results_temp.append(interest['field'])
            field.remove(interest['field'])

    for i in min(range(5), len(results_temp))
        results.append(results_temp[i])
    flattened = list(itertools.chain.from_iterable(result[0]))
    return flattened

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)