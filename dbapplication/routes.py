from flask import render_template, request

from models import Person

def register_routes(app, db):

    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'GET':
            people = Person.query.all()
            return render_template('index.html', people=people)
        elif request.method == 'POST':
            name = request.form.get('name')
            age = int(request.form.get('age'))
            job = request.form.get('job')

            person = Person(name=name, age=age, job=job)

            db.session.add(person)
            db.session.commit()

            people = Person.query.all()
            return render_template('index.html', people=people)

    @app.route('/delete/<person_id>', methods=['DELETE'])
    def delete(person_id):
        Person.query.filter(Person.person_id == person_id).delete()

        db.session.commit()
        people = Person.query.all()
        return render_template('index.html', people=people)


    @app.route('/details/<person_id>')
    def details(person_id):
        person = Person.query.filter(Person.person_id == person_id).first()
        return render_template('details.html', person=person)