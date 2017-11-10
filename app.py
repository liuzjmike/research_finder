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
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/search')
def search():
    return render_template('search.html')

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
