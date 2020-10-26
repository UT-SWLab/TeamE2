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
            {'driverId': driver['driverId'], 'driverRef': driver['driverRef'], 'surname': driver['surname'],
             'forename': driver['forename'], 'constructor': driver['constructor']['name'],
             'nationality': driver['nationality']})
    per_page = 20
    pages = int(len(drivers) / per_page)
    drivers = drivers[page * per_page: page * per_page + per_page]
    return render_template('drivers-model.html', drivers=drivers, pages=pages, page=page)


@app.route('/models_constructors')
def constructor_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    constructor_list = db.constructors.find()
    constructors = []
    topDriver = "N/A"
    for constructor in constructor_list:
        if 'topDriverName' in constructor:
            topDriver = constructor['topDriverName']
        constructors.append(
            {'constructorId': constructor['constructorId'], 'constructorRef': constructor['constructorRef'],
             'name': constructor['name'], "topDriver": topDriver, "nationality": constructor['nationality']})
    print(len(constructors))
    per_page = 20
    pages = int(len(constructors) / per_page)
    constructors = constructors[page * per_page: page * per_page + per_page]
    print(constructors)
    return render_template('constructors-model.html', constructors=constructors, pages=pages, page=page)


@app.route('/models_circuits')
def circuit_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    circuit_list = db.circuits.find()
    circuits = []
    for circuit in circuit_list:
        print(circuit['location'])
        circuits.append(
            {'circuitId': circuit['circuitId'], 'circuitRef': circuit['circuitRef'], 'name': circuit['name'],
             'location': str(circuit['location']), 'country': circuit['country']})
    per_page = 20
    pages = int(len(circuits) / per_page)
    circuits = circuits[page * per_page: page * per_page + per_page]
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
    ref = driver['driverRef']
    img_path = f'images/drivers/{ref}.png'
    bio = driver['bio']
    teams = driver['all_constructors']
    cur_constructor = driver['constructor']

    victories = []
    results = []
    all_results = list(db.results.find({'driverId': driver_id}))
    for result in all_results:
        results.append({'raceId': result['raceId'], 'constructorId': result['constructorId'],
                        'position': result['positionOrder'], 'points': result['points'],
                        'laps': result['laps'], 'time': result['time'],
                        'fastestLap': result['fastestLap'], 'rank': result['rank'],
                        'fastestLapTime': result['fastestLapTime'], 'date': result['raceDate'],
                        'raceName': result['raceName'],
                        'constructorName': result['constructorName'], 'driverName': result['driverName']})

    for result in results:
        if result['position'] == 1:
            victories.append(result)

    victories = sorted(victories, key=lambda i: i['date'], reverse=True)
    latest = sorted(results, key=lambda i: i['date'], reverse=True)
    if len(latest) >= 5:
        latest = latest[:5]  # List the driver's 5 latest races

    return render_template('drivers-instance.html', name=name, code=code,
                           dob=dob, nation=nationality, number=number, teams=teams,
                           url=url, img_path=img_path, victories=victories, latest=latest, bio=bio,
                           constructor=cur_constructor)


@app.route('/constructors')
def constructor_instance():
    constructor_id = int(request.args['id'])

    constructor = db.constructors.find_one({'constructorId': constructor_id})
    name = constructor['name']
    nation = constructor['nationality']
    url = constructor['url']
    ref = constructor['constructorRef']
    img_path = f'images/constructors/{ref}.png'
    bio = constructor['bio']
    top_driver = {'id': constructor['topDriverId'], 'name': constructor['topDriverName'],
                  'points': constructor['topDriverPoints']}

    drivers = db.drivers.find({"constructor.id": constructor_id})
    team_drivers = []
    for driver in drivers:
        team_drivers.append({'driverId': driver['driverId'], 'name': driver['forename'] + " " + driver['surname']})

    wins = []
    db_victories = db.constructor_standings.find({'constructorId': constructor_id, 'position': 1})

    for v in db_victories:
        wins.append({'raceName': v['raceName'], 'date': v['raceDate'], 'circuitId': v['circuitId'],
                     'circuitName': v['circuitName'], 'points': v['points']})

    wins = sorted(wins, key=lambda i: i['date'], reverse=True)
    total_wins = len(wins)
    if len(wins) >= 5:
        wins = wins[:5]  # Take the 5 latest victories

    return render_template('constructors-instance.html', name=name, nation=nation,
                           drivers=team_drivers, wins=wins, img_path=img_path, url=url, bio=bio,
                           total_wins=total_wins, top_driver=top_driver)


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
    ref = circuit['circuitRef']
    bio = circuit['bio']
    img_path = f'images/circuits/{ref}.png'

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
            {'driverId': result['driverId'], 'driverName': result['driverName'], 'position': result['positionOrder'],
             'points': result['points'], 'laps': result['laps'], 'time': result['time'],
             'constructorId': result['constructorId'], 'fastestLapTime': result['fastestLapTime'],
             'fastestLapSpeed': result['fastestLapSpeed'], 'fastestLap': result['fastestLap'],
             'rank': result['rank'], 'constructorName': result['constructorName']})

    driver_result_data = sorted(driver_result_data, key=lambda i: i['position'])

    all_results = db.results.find({'circuitId': circuit_id})
    fastest_lap_times = []
    for result in all_results:
        fastest_lap_times.append({'fastestLapTime': result['fastestLapTime'], 'driverId': result['driverId'],
                                  'driverName': result['driverName'], 'raceName': result['raceName'],
                                  'speed': result['fastestLapSpeed'], 'constructorId': result['constructorId'],
                                  'constructorName': result['constructorName']})

    fastest_lap_times = sorted(fastest_lap_times, key=lambda i: (i['fastestLapTime']))
    if len(fastest_lap_times) >= 5:
        fastest_lap_times = fastest_lap_times[:5]

    return render_template('circuits-instance.html', name=name, lat=lat,
                           long=longitude, locality=location, country=country, url=url,
                           img_path=img_path, circuit_id=circuit_id, latest_results=driver_result_data,
                           latest_race_name=latest_race_name, bio=bio, lap_times=fastest_lap_times)


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
