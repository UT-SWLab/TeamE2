# 1st party packages
import json
import os
from collections import defaultdict
from datetime import datetime

# 3rd party packages
from flask import Flask, render_template, request
from flask_pymongo import pymongo

app = Flask(__name__)
dbUsername = 'formulaOne'
dbPassword = '0WpPVH6LdcHiwdct'
CONNECTION_STRING = "mongodb+srv://" + dbUsername + ":" + dbPassword + "@formulaonedb.bue6f.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('FormulaOneDB')

# Default filelr image
NO_IMG = 'images/no_img.png'


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
        if 'driverId' in driver.keys():      
            drivers.append(
                {'driverId': driver['driverId'], 'driverRef': driver['driverRef'], 
                'surname': driver['surname'], 'forename': driver['forename'], 'nationality': driver['nationality']})
            if 'constructor' not in driver:
                con = list(db.results.find({'driverId': driver['driverId']}))
                all_constructors = []
                for c in con:
                    constructorId = c['constructorId']
                    constructorName = db.constructors.find_one({'constructorId': c['constructorId']})['name']
                    constructor = {'id': constructorId, 'name': constructorName}
                    if constructor not in all_constructors:
                        all_constructors.append(constructor)
                all_constructors.reverse() #newest to oldest
                # print(all_constructors)
                db.drivers.update_one({'_id': driver['_id']}, {'$set': {'constructor': all_constructors[0]}})
                db.drivers.update_one({'_id': driver['_id']}, {'$set': {'all_constructors': all_constructors}})
            else:
                # TODO: Consider adding logging, print statements clutter up the terminal
                # print('found constructor for driver: ' + str(driver['driverId']))
                drivers[-1].update({'constructor': driver['constructor']})
            drivers[-1].update({'link': 'drivers?id='+str(driver['driverId'])})

            # Get image
            driver_ref = driver['driverRef']
            img_path = f'images/drivers/{driver_ref}.png'
            print(img_path)
            print(os.getcwd())
            if not os.path.exists(f'./static/{img_path}'):
                img_path = NO_IMG
            drivers[-1].update({'imgpath': img_path})

    per_page = 20
    pages = int(len(drivers) / per_page)
    drivers = drivers[page * per_page: page * per_page + per_page]
    return render_template('drivers-model.html', drivers=drivers, pages=pages, page=page)


@app.route('/driver-search')
def driver_search():
    """
    Populate driver search result page
    """
    query = request.args['search'] 
    print('user entered query:')
    print(query)


@app.route('/models_constructors')
def constructor_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    constructor_list = db.constructors.find()
    constructors = []
    topDriver = "N/A"
    for constructor in constructor_list:
        if 'constructorId' in constructor.keys():
            constructors.append(
                {'constructorId': constructor['constructorId'], 'constructorRef': constructor['constructorRef'], 
                'name': constructor['name'], 'nationality': constructor['nationality']}) 
            if 'topDriverName' in constructor.keys():
                constructors[-1].update({'top_driver': constructor['topDriverName']})
            else:
                constructors[-1].update({'top_driver': 'N/A'})
            constructors[-1].update({'link': 'constructors?id='+str(constructor['constructorId'])})

            # Get image
            constructor_ref = constructor['constructorRef']
            img_path = f'images/constructors/{constructor_ref}.png'
            if not os.path.exists(f'./static/{img_path}'):
                img_path = NO_IMG
            constructors[-1].update({'imgpath': img_path})
    per_page = 20
    pages = int(len(constructors)/per_page)
    constructors = constructors[page*per_page: page*per_page+per_page]
    return render_template('constructors-model.html', constructors=constructors, pages=pages, page=page)


@app.route('/constructor-search')
def constructor_search():
    """
    Populate constructor search result page
    """
    query = request.args['search'] 
    print('user entered query:')
    print(query)


@app.route('/models_circuits')
def circuit_model():
    page = request.args.get('page', 1, type=int)
    page = page - 1
    circuit_list = db.circuits.find()
    circuits = []
    for circuit in circuit_list:
        if 'circuitId' in circuit.keys():
            circuits.append(
                {'circuitId': circuit['circuitId'], 'circuitRef': circuit['circuitRef'], 
                'name': circuit['name'], 'location': circuit['location'], 'country': circuit['country']})
            if 'most_recent_race' not in circuit.keys():
                mrr = db.races.find({'circuitId': circuit['circuitId']}).sort([('date', -1)])
                mrr = list(mrr)
                if len(mrr) > 0:
                    mrr = mrr[0]
                    print(mrr['name'] + ' ' + mrr['date'])
                    db.circuits.update_one({'_id': circuit['_id']}, {'$set': {'most_recent_race': mrr['name'] + ' ' + mrr['date']}})
                else:
                    db.circuits.update_one({'_id': circuit['_id']}, {'$set': {'most_recent_race': 'N/A'}})
            else:
                print('found most recent race for circuit: ' + str(circuit['circuitId']))
                circuits[-1].update({'most_recent_race': circuit['most_recent_race']})
            circuits[-1].update({'link': 'circuits?id='+str(circuit['circuitId'])})

            # Get image
            circuit_ref = circuit['circuitRef']
            img_path = f'images/circuits/{circuit_ref}.png'
            if not os.path.exists(f'./static/{img_path}'):
                img_path = NO_IMG
            circuits[-1].update({'imgpath': img_path})
    per_page = 20
    pages = int(len(circuits) / per_page)
    circuits = circuits[page * per_page: page * per_page + per_page]
    return render_template('circuits-model.html', circuits=circuits, pages=pages, page=page)


@app.route('/circuit-search')
def circuit_search():
    """
    Populate circuit search result page
    """
    query = request.args['search'] 
    print('user entered query:')
    print(query)


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
                        'fastestLap': result['fastestLap'], 'fastestLapTime': result['fastestLapTime'],
                        'date': result['raceDate'], 'raceName': result['raceName'],
                        'constructorName': result['constructorName'], 'driverName': result['driverName'],
                        'circuitId': result['circuitId'], 'circuitName': result['circuitName']
                        })

    for result in results:
        if result['position'] == 1:
            victories.append(result)

    victories = sorted(victories, key=lambda i: i['date'], reverse=True)
    latest = sorted(results, key=lambda i: i['date'], reverse=True)
    if len(latest) >= 5:
        latest = latest[:5]  # List the driver's 5 latest races

    # Get image
    driver_ref = driver['driverRef']
    img_path = f'images/drivers/{driver_ref}.png'
    if not os.path.exists(f'./static/{img_path}'):
        img_path = NO_IMG

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

    # Get image
    constructor_ref = constructor['constructorRef']
    img_path = f'images/constructors/{constructor_ref}.png'
    if not os.path.exists(f'./static/{img_path}'):
        img_path = NO_IMG

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
    bio = circuit['bio']

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

    # Get image
    circuit_ref = circuit['circuitRef']
    img_path = f'images/circuits/{circuit_ref}.png'
    if not os.path.exists(f'./static/{img_path}'):
        img_path = NO_IMG

    return render_template('circuits-instance.html', name=name, lat=lat,
                           long=longitude, locality=location, country=country, url=url,
                           img_path=img_path, circuit_id=circuit_id, latest_results=driver_result_data,
                           latest_race_name=latest_race_name, bio=bio, lap_times=fastest_lap_times)


@app.route('/')
def home():
    recentRaces = db.races.find({'year' : 2020}).limit(5)
    recentRaces = list(recentRaces)
    print(recentRaces)
    todaysDate = datetime.now()
    todayMonth = datetime.month
    todaysDay = datetime.day
    date = "...-"+str(todayMonth) + "-"+str(todaysDay)
    todaysDrivers = db.drivers.find({'dob' : {'$regex' : date}}).limit(20)
    for driver in todaysDrivers:
        print()
        print(driver)
    return render_template('home.html' , recentRaces = recentRaces , todayDrivers = todaysDrivers)


if __name__ == '__main__':
    app.run(debug=True)
