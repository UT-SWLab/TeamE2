# 1st party packages
import json

# 3rd party packages
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/models_drivers')
def driver_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    with open('./data/drivers.json') as f:
        per_page = 8
        drivers = json.load(f)
        pages = int(len(drivers)/per_page)
        drivers = drivers[page*per_page : page*per_page+per_page]
    return render_template('drivers-model.html', drivers=drivers, pages=pages, page=page)

@app.route('/models_constructors')
def constructor_model():
    with open('./data/constructors.json') as f:
        constructors = json.load(f)
    return render_template('constructors-model.html', constructors=constructors)
@app.route('/models_circuits')
def circuit_model():
    with open('./data/circuits.json') as f:
        circuits = json.load(f)
    return render_template('circuits-model.html', circuits=circuits)

@app.route('/drivers')
def driver_instance():
    driver_id = request.args['id']

    # we need to change this to request from firebase db in the future
    with open('data/drivers.json') as json_file:
        drivers = json.load(json_file)
        for driver in drivers:
            if driver['driverId'] == driver_id:
                data = driver
                break
    name = data['givenName'] + ' ' + data['familyName']
    img_path = f'images/{driver_id}.jpg'
    return render_template('drivers-instance.html', name=name, code=data['code'],\
        dob=data['dateOfBirth'], nation=data['nationality'], img_path=img_path)


@app.route('/constructors')
def constructor_instance():
    constructor_id = request.args['id']

    # we need to change this to request from firebase db in the future
    with open('data/constructors.json') as json_file:
        constructors = json.load(json_file)
        for constructor in constructors:
            if constructor['constructorId'] == constructor_id:
                data = constructor
                break
    name = data['name']
    nation = data['nationality']
    img_path = f'images/{constructor_id}.jpg'
    return render_template('constructors-instance.html', name=name, nation=nation,\
        img_path=img_path)


@app.route('/circuits')
def circuit_instance():
    circuit_id = request.args['id']

    # we need to change this to request from firebase db in the future
    with open('data/circuits.json') as json_file:
        circuits = json.load(json_file)
        for circuit in circuits:
            if circuit['circuitId'] == circuit_id:
                data = circuit
                break
    name = data['circuitName']
    location = data['Location']
    lat = location['lat']
    long = location['long']
    locality = location['locality']
    country = location['country']

    img_path = f'images/{circuit_id}.jpg'
    return render_template('circuits-instance.html', name=name, lat=lat,\
        long=long, locality=locality, country=country, img_path=img_path)


@app.route('/')
def home():
    return render_template('home.html')    


if __name__ == '__main__':
    app.run(debug=True)
