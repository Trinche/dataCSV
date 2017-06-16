import csv, os.path
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
        mylist = [name, surname, job, company, city, country]
        mydict = {'name': name, 'surname': surname, 'job': job, 'company': company, 'city': city, 'country': country}
        fieldnames = ['name', 'surname', 'job', 'company', 'city', 'country']
        file_exists = os.path.isfile('nameList.csv')

        with open('nameList.csv', 'a') as inFIle:
            writer = csv.DictWriter(inFIle, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow(mydict)
    return render_template('form.html', form=form)


@app.route("/search", methods=['GET', 'POST'])
def search():
    form = ReusableForm(request.form)

    if request.method == 'POST':
        searched = request.form['searched']

        with open('datasetBigDive.csv', 'r') as inFIle:
            reader = csv.reader(inFIle)
            campo = []

            for row in reader:
                print row
                for value in row:
                    if value == searched:
                        campo.append(row)

        if campo == []:
            return "Sorry value doesn't exist"
        else:
            return render_template('search.html', campo=campo, form=form)

    return render_template('search.html', form=form)


@app.route("<rowid>/edit", methods=['GET', 'POST'])
def edit(rowid):
    index = search(rowid)
    form = ReusableForm(request.form)
    bottle_list = []

    # Read all data from the csv file.
    with open('datasetBigDive.csv', 'rb') as b:
        bottles = csv.reader(b)
        bottle_list.extend(bottles)

    # data to override in the format {line_num_to_override:data_to_write}.
    line_to_override = {1: ['e', 'c', 'd']}

    # Write data to the csv file and replace the lines in the line_to_override dict.
    with open('a.csv', 'wb') as b:
        writer = csv.writer(b)
        for line, row in enumerate(bottle_list):
            data = line_to_override.get(line, row)
            writer.writerow(data)

    return render_template('overwrite.html', form=form)


@app.route('/blog/<blogid>/update', methods=['GET', 'POST'])
def update(blogid):
    index = search_blog(blogid)

    if request.method == 'POST':
        if not request.form['text'] or not request.form['title']:
            flash('Please, all fields are required', 'warning')
            return redirect('/blog/{}/update'.format(blogid))
        blogs[index]['title'] = request.form['title']
        blogs[index]['text'] = request.form['text']
        flash('Good job man!', 'success')
        return redirect('/blog/{}'.format(blogid))
    return render_template('create.html', mode='update', blog=blogs[index])

if __name__ == "__main__":
    app.run()

