from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import models
import forms

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
            return render_template('search.html')
    return render_template('search.html')


@app.route('/search')
def searchpage():
    return render_template('searchpage.html')


class SearchResult(object):
    def __init__(self, netid, first_name, last_name, dept, interests):
        self.netid = netid
        self.first_name = first_name
        self.last_name = last_name
        self.dept = dept
        self.interests = interests

    def get_netid(self):
        return self.netid

    def get_last_name(self):
        return self.last_name


@app.route('/search-results')
def search_results(dept, interests, professor):
    # netid_maps maps the netid to index in the list of search results
    netid_map = {}
    last_index = 0

    results = []

    # find all netid (of professors) with matching first name
    users = db.session.query(models.People)\
        .filter(models.People.first_name == professor).all()
    for user in users:
        if user['netid'] not in netid_map:
            netid_map['netid'] = last_index
            last_index = last_index + 1
            prof_department = db.session.query(models.Member)\
                .filter(models.Member.netid == user['netid']).one()
            results.append(SearchResult(
                user['netid'],
                user['first_name'],
                user['last_name'],
                prof_department,
                []))
    # find all netid (of professors) with matching last name
    users = db.session.query(models.People)\
        .filter(models.People.last_name == professor).all()
    for user in users:
        if user['netid'] not in netid_map:
            netid_map['netid'] = last_index
            last_index = last_index + 1
            prof_department = db.session.query(models.Member)\
                .filter(models.Member.netid == user['netid']).one()
            results.append(SearchResult(
                user['netid'],
                user['first_name'],
                user['last_name'],
                prof_department,
                []))
    # find all netid (of professors) with matching department
    users = db.session.query(models.People)\
        .filter(models.Member.name == dept).all()
    for user in users:
        if user['netid'] not in netid_map:
            netid_map['netid'] = last_index
            last_index = last_index + 1
            results.append(SearchResult(
                user['netid'],
                user['first_name'],
                user['last_name'],
                dept,
                []))
    # find all netid (of professors) with matching Interests
    for interest in interests
        users = db.session.query(models.Interest)\
            .filter(models.Interest.field == interest).all()
        for user in users:
            if user['netid'] in netid_map:
                index = user['netid']
                results[index].interests.append(interest)
            else:
                netid_map['netid'] = last_index
                last_index = last_index + 1
                prof = db.session.query(models.People)\
                    .filter(models.People.netid == user['netid']).all()
                prof_department = db.session.query(models.Member)\
                    .filter(models.Member.netid == user['netid']).one()
                results.append(SearchResult(
                    prof['netid'],
                    prof['first_name'],
                    prof['last_name'],
                    prof_department,
                    [interest]))

    # sort results by alphabetical order
    sorted_results = sorted(results, key=SearchResult.get_last_name)

    # TODO: redirect to search results page


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
