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


@app.route("/", methods=['GET', 'POST'])
def hello():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        job = request.form['job']
        company = request.form['company']
        city = request.form['city']
        country = request.form['country']
        fieldnames = ['name', 'surname', 'job', 'company', 'city', 'country']
        mydict = {'name': name, 'surname': surname, 'job': job, 'company': company, 'city':city, 'country':country}

        with open('nameList.csv', 'a') as inFIle:
            writer = csv.writer(inFIle)
            for key, value in mydict.items():
                writer.writerow([key, value])
            #writer.writerow({'name': name, 'surname': surname, 'job': job, 'company': company, 'city': city,
            #                 'country': country})

    return render_template('form.html', form=form)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = ReusableForm(request.form)
    var = ""

    if request.method == 'POST':
        searched = request.form['searched']

        with open('datasetBigDive.csv', 'r') as inFIle:
            reader = csv.reader(inFIle)
            campo = []

            for row in reader:
                for value in row:
                    if value == searched:
                        campo.append(row)
                        var = str(campo)

        if campo == []:
            return "Sorry value doesn't exist"
        else:
            return var

    return render_template('search.html', form=form)


if __name__ == "__main__":
    app.run()

