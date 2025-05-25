	from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pets.db'
db = SQLAlchemy(app)

# Pet model
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    type = db.Column(db.String(50))
    age = db.Column(db.Integer)
    image_url = db.Column(db.String(200))

# Adoption request model
class AdoptionRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    pet_name = db.Column(db.String(100))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/pets')
def show_pets():
    pets = Pet.query.all()
    return render_template('pets.html', pets=pets)

@app.route('/adopt', methods=['GET', 'POST'])
def adopt():
    if request.method == 'POST':
        name = request.form['name']
        pet_name = request.form['pet_name']
        request_entry = AdoptionRequest(name=name, pet_name=pet_name)
        db.session.add(request_entry)
        db.session.commit()
        return redirect(url_for('thank_you'))
    return render_template('adopt.html')

@app.route('/thankyou')
def thank_you():
    return render_template('thankyou.html')

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        age = int(request.form['age'])
        image_url = request.form['image_url']
        new_pet = Pet(name=name, type=type_, age=age, image_url=image_url)
        db.session.add(new_pet)
        db.session.commit()
    pets = Pet.query.all()
    return render_template('admin.html', pets=pets)

@app.route('/delete_pet/<int:pet_id>')
def delete_pet(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    db.session.delete(pet)
    db.session.commit()
    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
