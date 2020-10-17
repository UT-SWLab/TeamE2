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
    # driverId, last name first name, picture
    driver_list = db.drivers.find()
    drivers = []
    for driver in driver_list:
        drivers.append(
            {'driverId': str(driver['driverId']), 'surname': driver['surname'], 'forename': driver['forename']})
    return render_template('drivers-model.html', drivers=drivers)


@app.route('/drivers')
def driver_instance():
    driver_id = int(request.args['id'])
    driver = db.drivers.find_one({"driverId": driver_id})

    # Gathers relevant information from database
    name = driver['forename'] + ' ' + driver['surname']
    dob = driver['dob']
    code = driver['code']
    nationality = driver['nationality']
    number = driver['number']
    img_path = f'images/{driver_id}.jpg'

    # Gathers the teams for the player
    teamIds = db.results.distinct('constructorId', {'driverId': driver_id})
    teams = []
    for team in teamIds:
        team = db.constructors.find_one({'constructorId': team})
        teams.append({'constructorId': team['constructorId'], 'name': team['name']})
    print(teams)

    victoryIds = db.results.find({"driverId": driver_id, "positionOrder": 1})
    for victory in victoryIds:
        # raceId => races collection.circuitId =>  circuits collection
        print(victory)

    return render_template('drivers-instance.html', name=name, code=code,
                           dob=dob, nation=nationality, number=number, teams=teams, img_path=img_path)


@app.route('/models_constructors')
def constructor_model():
    constructor_list = db.constructors.find()
    constructors = []
    for constructor in constructor_list:
        constructors.append({'constructorId': str(constructor['constructorId']), 'name': constructor['name'],
                             'nationality': constructor['nationality']})

    return render_template('constructors-model.html', constructors=constructors)


@app.route('/constructors')
def constructor_instance():
    constructor_id = int(request.args['id'])

    constructor = db.constructors.find_one({'constructorId': constructor_id})
    name = constructor['name']
    nation = constructor['nationality']
    img_path = f'images/{constructor_id}.jpg'

    driverIds = db.results.distinct('driverId', {'constructorId': constructor_id})
    teamDrivers = []
    for driver in driverIds:
        driver = db.drivers.find_one({'driverId': driver})
        teamDrivers.append({'driverId': driver['driverId'], 'name': driver['forename'] + " " + driver['surname']})

    victoryRaces = db.results.find({'constructorId': constructor_id, 'positionOrder': 1})
    wonCircuits = defaultdict(list)
    for victoryRace in victoryRaces:
        raceInfo = db.races.find_one({'raceId': victoryRace['raceId']})
        wonCircuits[raceInfo['circuitId']] = {'circuitId': raceInfo['circuitId'], 'ciruitName': raceInfo['name']}
    wonCircuits = list(wonCircuits.values())
    return render_template('constructors-instance.html', name=name, nation=nation,
                           drivers=teamDrivers, wins=wonCircuits, img_path=img_path)


@app.route('/models_circuits')
def circuit_model():
    circuit_list = db.circuits.find()
    circuits = []
    for circuit in circuit_list:
        print(circuit)
        circuits.append({'circuitId': str(circuit['circuitId']), 'circuitName': circuit['name']})

    return render_template('circuits-model.html', circuits=circuits)


# Add circuitID to results.csv to make it easier to find race participants and constructor winenrs
@app.route('/circuits')
def circuit_instance():
    circuit_id = request.args['id']
    circuit = db.circuits.find_one({'circuitId': int(circuit_id)})

    name = circuit['name']
    location = circuit['location']
    lat = circuit['lat']
    longitude = circuit['lng']
    country = circuit['country']
    circuit_id = circuit['circuitId']
    url = circuit['url']
    img_path = f'images/{circuit_id}.jpg'

    races_list = db.races.find()
    races = []
    # Get every race that happens in that circuit
    # for race in races_list:
    #     if race['circuitId'] == circuit_id:     # Only want the races that took place in that circuit
    #         races.append({'raceId': str(race['raceId']), 'name': race['name'],
    #                       'year': race['year'], 'url': race['url']})

    # Get only race name since it repeats a lot anyway
    for race in races_list:
        if race['circuitId'] == circuit_id:  # Only want the races that took place in that circuit
            races.append(race['name'])
    races = list(dict.fromkeys(races))  # Remove repeat race names (e.g. 2009 Spanish Grand
    # Prix, 2010 Spanish Grand Prix, etc

    return render_template('circuits-instance.html', name=name, lat=lat,
                           long=longitude, locality=location, country=country, url=url,
                           img_path=img_path, circuit_id=circuit_id, race_list=races)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
