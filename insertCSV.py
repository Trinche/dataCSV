import csv
from flask import Flask, render_template, flash, request
from werkzeug.datastructures import MultiDict

from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'


class ReusableForm(Form):
    name = StringField('Name:', validators=[validators.required()])
    surname = StringField('surname:', validators=[validators.required()])
    job = StringField('job:', validators=[validators.required()])
    company = StringField('company:', validators=[validators.required()])
    city = StringField('city:', validators=[validators.required()])
    country = StringField('country:', validators=[validators.required()])

    def reset(self):
        blankData = MultiDict([('csrf', self.reset_csrf())])
        self.process(blankData)


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    print form.errors
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        job = request.form['job']
        company = request.form['company']
        city = request.form['city']
        country = request.form['country']
        fieldnames = ['name', 'surname', 'job', 'company', 'city', 'country']

        if form.validate():
            with open('nameList.csv', 'a') as inFIle:
                flash('Thanks for registration ' + name)
                writer = csv.DictWriter(inFIle, fieldnames=fieldnames)
                writer.writerow({'name': name, 'surname': surname, 'job': job, 'company': company, 'city': city,
                                 'country': country})
        else:
            flash('Error: All the form fields are required. ')

    return render_template('form.html', form=form)


if __name__ == "__main__":
    app.run()

