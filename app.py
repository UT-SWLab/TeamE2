# 1st party packages
import json
import os
from collections import defaultdict

# 3rd party packages
from flask import Flask, render_template, request
from flask_pymongo import pymongo

app = Flask(__name__)
dbUsername = 'formulaOne'
dbPassword = '0WpPVH6LdcHiwdct'
CONNECTION_STRING = "mongodb+srv://" + dbUsername + ":" + dbPassword + "@formulaonedb.bue6f.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('FormulaOneDB')

@app.route('/dbTest')
def test():
    db.db.collection.insert_one({"name": "John"})
    return "Connected to the data base!"


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/models_drivers')
def driver_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    driver_list = db.drivers.find()
    drivers = []
    for driver in driver_list:
        drivers.append(
            {'driverId': driver['driverRef'], 'surname': driver['surname'], 'forename': driver['forename']})
    per_page = 20
    pages = int(len(drivers)/per_page)
    drivers = drivers[page*per_page: page*per_page+per_page]
    return render_template('drivers-model.html', drivers=drivers, pages=pages, page=page)


@app.route('/models_constructors')
def constructor_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    constructor_list = db.constructors.find()
    constructors = []
    for constructor in constructor_list:
        constructors.append(
            {'constructorId': constructor['constructorRef'], 'name': constructor['name']})
    print(len(constructors))
    per_page = 20
    pages = int(len(constructors)/per_page)
    constructors = constructors[page*per_page: page*per_page+per_page]
    print(constructors)
    return render_template('constructors-model.html', constructors=constructors, pages=pages, page=page)


@app.route('/models_circuits')
def circuit_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    circuit_list = db.circuits.find()
    circuits = []
    for circuit in circuit_list:
        circuits.append(
            {'circuitId': circuit['circuitRef'], 'name': circuit['name']})
    per_page = 20
    pages = int(len(circuits)/per_page)
    circuits = circuits[page*per_page: page*per_page+per_page]
    return render_template('circuits-model.html', circuits=circuits, pages=pages, page=page)


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
