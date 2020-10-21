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
            {'driverRef': driver['driverRef'], 'surname': driver['surname'], 'forename': driver['forename'], 'nationality': driver['nationality']})
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
            {'constructorRef': constructor['constructorRef'], 'name': constructor['name'], 'nationality': constructor['nationality']})
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
            {'circuitRef': circuit['circuitRef'], 'name': circuit['name'], 'location': circuit['location'], 'country': circuit['country']})
    per_page = 20
    pages = int(len(circuits)/per_page)
    circuits = circuits[page*per_page: page*per_page+per_page]
    return render_template('circuits-model.html', circuits=circuits, pages=pages, page=page)

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
    url = driver['url']
    img_path = f'images/{driver_id}.jpg'

    # Gathers the teams for the player
    teamIds = db.results.distinct('constructorId', {'driverId': driver_id})
    teams = []
    for team in teamIds:
        team = db.constructors.find_one({'constructorId': team})
        teams.append({'constructorId': team['constructorId'], 'name': team['name']})
    # print(teams)

    victories = []
    results = []
    all_results = list(db.results.find({'driverId': driver_id}))
    for result in all_results:
        results.append({'raceId': result['raceId'], 'constructorId': result['constructorId'],
                        'position': result['positionOrder'], 'points': result['points'],
                        'laps': result['laps'], 'time': result['time'],
                        'fastestLap': result['fastestLap'], 'rank': result['rank'],
                        'fastestLapTime': result['fastestLapTime'], 'date': "", 'race_name': "",
                        'constructor_name': ""})

    for result in results:
        race = db.races.find_one({'raceId': result['raceId']})
        constructor = db.constructors.find_one({"constructorId": result['constructorId']})
        result['date'] = race['date']
        result['race_name'] = str(race['year']) + " " + race['name']
        result['constructor_name'] = constructor['name']
        if result['position'] == 1:
            victories.append(result)

    victories = sorted(victories, key=lambda i: i['date'], reverse=True)
    latest = sorted(results, key=lambda i: i['date'], reverse=True)
    latest = latest[:5]
    # victories = list(db.results.find({"driverId": driver_id, "positionOrder": 1}))
    # for victory in victories:
    #     constructor = db.constructors.find_one({"constructorId": victory['constructorId']})
    #     victory['constructorId'] = constructor['name']
    #
    #     race = db.races.find_one({"raceId": victory['raceId']})
    #     victory['raceId'] = str(race['year']) + " " + race['name']

    return render_template('drivers-instance.html', name=name, code=code,
                           dob=dob, nation=nationality, number=number, teams=teams,
                           url=url, img_path=img_path, victories=victories, latest=latest)


@app.route('/constructors')
def constructor_instance():
    constructor_id = int(request.args['id'])

    constructor = db.constructors.find_one({'constructorId': constructor_id})
    name = constructor['name']
    nation = constructor['nationality']
    url = constructor['url']
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
        wonCircuits[raceInfo['circuitId']] = {'circuitId': raceInfo['circuitId'], 'circuitName': raceInfo['name']}
    wonCircuits = list(wonCircuits.values())
    return render_template('constructors-instance.html', name=name, nation=nation,
                           drivers=teamDrivers, wins=wonCircuits, img_path=img_path, url=url)


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

    races_list = db.races.find({'circuitId': int(circuit_id)})  # Get all races held at this circuit
    races = []
    for race in races_list:
        races.append({'raceId': race['raceId'], 'name': race['name'], 'year': race['year'], 'url': race['url'],
                      'date': race['date']})

    latest_race_name = ""
    results = None

    races = sorted(races, key=lambda i: i['date'], reverse=True)
    for race in races:
        results = db.results.find({'raceId': race['raceId']})  # Results of the latest race
        results = list(results)
        if len(results) != 0:  # Ergast returns races that are scheduled for the future as well, so we have to make sure
            # the latest race has actually happened
            latest_race_name = str(race['year']) + " " + race['name']
            break

    driver_result_data = []
    for result in results:
        driver_result_data.append(
            {'driverId': result['driverId'], 'driverName': '', 'position': result['positionOrder'],
             'points': result['points'], 'laps': result['laps'], 'time': result['time'],
             'constructorId': result['constructorId'], 'fastestLapTime': result['fastestLapTime'],
             'fastestLapSpeed': result['fastestLapSpeed'], 'fastestLap': result['fastestLap'],
             'rank': result['rank'], 'constructorName': ''})

    driver_result_data = sorted(driver_result_data, key=lambda i: i['position'])
    # Find the name of the drivers
    for driver_result in driver_result_data:
        driver = db.drivers.find_one({'driverId': driver_result['driverId']})  # Should come up with a faster way
        # to find a driver's name given their Id besides querying the db
        constructor = db.constructors.find_one({'constructorId': driver_result['constructorId']})  # Should come up
        # with a faster way to find a constructor's name given their ID besides querying the db
        driver_result['driverName'] = driver['forename'] + " " + driver['surname']
        driver_result['constructorName'] = constructor['name']

    return render_template('circuits-instance.html', name=name, lat=lat,
                           long=longitude, locality=location, country=country, url=url,
                           img_path=img_path, circuit_id=circuit_id, latest_results=driver_result_data,
                           latest_race_name=latest_race_name)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
