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

@app.route('/signup')
def signup():
    form = forms.SignUpFormFactory.signup()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)

            existing_user = models.People.doesUserExist(form.netid.data)
            if not existing_user:
                return render_template('signup.html', form=form)

            models.People.insert(
                form.netid.data,
                form.first_name.data,
                form.last_name.data,
                form.email.data)
            # check if student or professor and store in the appropriate table

            if form.member.data == 'student':
                # TODO: figure out how to add resume
                models.Student.insert(
                    form.netid.data,
                    form.status.data,
                    form.start_year.data)
            else:
                models.Faculty.insert(
                    form.netid.data,
                    form.title.data,
                    form.opening.data,
                    form.personal_web.data)

            # insert interests
            interests = [x.strip() for x in (form.interests.data).split(',')]
            models.Interest.insert(form.netid.data, interests)

            # TODO: redirect to profile page (not finished)
            return redirect(url_for('profile', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('signup', form=form)
    else:
        return render_template('signup', form=form)

@app.route('/login')
def login():
    form = forms.SignUpFormFactory.login()
    if form.validate_on_submit():
        try:
            form.errors.pop('database', None)

            existing_user = models.People.validateUser(form.netid.data, form.password.data)
            if not existing_user:
                return render_template('login.html', form=form)

            # TODO: redirect to profile page (not finished)
            return redirect(url_for('drinker', name=form.name.data))
        except BaseException as e:
            form.errors['database'] = str(e)
            return render_template('login', form=form)
    else:
        return render_template('login', form=form)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/profile/<netid>')
def profile(netid):
    person_data = db.session.query(models.People)\
        .filter(models.People.netid == netid).one()
    return render_template('drinker.html', drinker=drinker)


# @app.route('/drinker/<name>')
# def drinker(name):
#     drinker = db.session.query(models.Drinker)\
#         .filter(models.Drinker.name == name).one()
#     return render_template('drinker.html', drinker=drinker)

# @app.route('/edit-drinker/<name>', methods=['GET', 'POST'])
# def edit_drinker(name):
#     drinker = db.session.query(models.Drinker)\
#         .filter(models.Drinker.name == name).one()
#     beers = db.session.query(models.Beer).all()
#     bars = db.session.query(models.Bar).all()
#     form = forms.DrinkerEditFormFactory.form(drinker, beers, bars)
#     if form.validate_on_submit():
#         try:
#             form.errors.pop('database', None)
#             models.Drinker.edit(name, form.name.data, form.address.data,
#                                 form.get_beers_liked(), form.get_bars_frequented())
#             return redirect(url_for('drinker', name=form.name.data))
#         except BaseException as e:
#             form.errors['database'] = str(e)
#             return render_template('edit-drinker.html', drinker=drinker, form=form)
#     else:
#         return render_template('edit-drinker.html', drinker=drinker, form=form)

# @app.template_filter('pluralize')
# def pluralize(number, singular='', plural='s'):
#     return singular if number in (0, 1) else plural

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
