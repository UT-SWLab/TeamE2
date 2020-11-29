# 1st party packages
import json
from collections import defaultdict
from datetime import date
import unicodedata

# 3rd party packages
from flask import Flask, render_template, request
from flask_pymongo import pymongo

# Self Written Modules
from database import FormulaOneDatabase
from image_handler import ImageHandler

app = Flask(__name__)
dbUsername = 'formulaOne'
dbPassword = '0WpPVH6LdcHiwdct'
db =  FormulaOneDatabase(dbUsername , dbPassword)
image_handler = ImageHandler()

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/models_drivers')
def driver_model():
    # get drivers from search, filtering, and sorting
    query = request.args.get('search', '', type=str).rstrip()
    filtered = request.args.get('filtered', '', type=str)
    driver_list = get_driver_list(filtered, query)
    sort = request.args.get('sort', '', type=str)
    driver_list = sort_models(driver_list, sort, filtered)

    page = request.args.get('page', 1, type=int)
    page = page - 1
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
                all_constructors.reverse()  # newest to oldest
                # print(all_constructors)
                db.drivers.update_one({'_id': driver['_id']}, {'$set': {'constructor': all_constructors[0]}})
                db.drivers.update_one({'_id': driver['_id']}, {'$set': {'all_constructors': all_constructors}})
            else:
                # TODO: Consider adding logging, print statements clutter up the terminal
                # print('found constructor for driver: ' + str(driver['driverId']))
                drivers[-1].update({'constructor': driver['constructor']})
            drivers[-1].update({'link': 'drivers?id=' + str(driver['driverId'])})

            # Get image
            driver_ref = driver['driverRef']
            img_path = image_handler.build_image_path(driver_ref , 'drivers')
            drivers[-1].update({'imgpath': img_path})

    per_page = 18
    pages = int(len(drivers) / per_page)
    drivers = drivers[page * per_page: page * per_page + per_page]
    return render_template('drivers-model.html', drivers=drivers, pages=pages, page=page, query=query, filtered=filtered, sort=sort)

#facade to build a page
@app.route('/models_constructors')
def constructor_model():
    # get constructors from search, filtering, and sorting
    query = request.args.get('search', '', type=str).rstrip()
    filtered = request.args.get('filtered', '', type=str)
    sort = request.args.get('sort', '', type=str)
    constructor_list = search(filtered, db.constructors, query)
    constructor_list = sort_models(constructor_list, sort, filtered)

    page = request.args.get('page', 1, type=int)
    page = page - 1
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
            constructors[-1].update({'link': 'constructors?id=' + str(constructor['constructorId'])})

            # Get image
            constructor_ref = constructor['constructorRef']
            img_path = image_handler.build_image_path(constructor_ref , 'constructors')
            constructors[-1].update({'imgpath': img_path})
    per_page = 18
    pages = int(len(constructors) / per_page)
    constructors = constructors[page * per_page: page * per_page + per_page]
    return render_template('constructors-model.html', constructors=constructors, pages=pages,
        page=page, query=query, filtered=filtered, sort=sort)

#Facade to build a page
@app.route('/models_circuits')
def circuit_model():
    # get circuits from search, filtering, and sorting
    query = request.args.get('search', '', type=str).rstrip()
    filtered = request.args.get('filtered', '', type=str)
    sort = request.args.get('sort', '', type=str)
    circuit_list = get_circuit_list(filtered, query)
    print(len(circuit_list))
    circuit_list = sort_models(circuit_list, sort, filtered)
    print(len(circuit_list))

    page = request.args.get('page', 1, type=int)
    page = page - 1
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
                    db.circuits.update_one({'_id': circuit['_id']},
                                           {'$set': {'most_recent_race': mrr['name'] + ' ' + mrr['date']}})
                else:
                    db.circuits.update_one({'_id': circuit['_id']}, {'$set': {'most_recent_race': 'N/A'}})
            else:
                # print('found most recent race for circuit: ' + str(circuit['circuitId']))
                circuits[-1].update({'most_recent_race': circuit['most_recent_race']})
            circuits[-1].update({'link': 'circuits?id=' + str(circuit['circuitId'])})

            # Get image
            circuit_ref = circuit['circuitRef']
            img_path = image_handler.build_image_path(circuit_ref , 'circuits')
            circuits[-1].update({'imgpath': img_path})
    per_page = 16
    pages = int(len(circuits) / per_page)
    circuits = circuits[page * per_page: page * per_page + per_page]
    return render_template('circuits-model.html', circuits=circuits, pages=pages, page=page,
        query=query, filtered=filtered, sort=sort)

@app.route('/drivers')
def driver_instance():
    driver_id = int(request.args['id'])
    driver = db.get_driver('driverId' , driver_id)
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
    results = db.get_result('driverId' , driver_id)
    for result in results:
        if result['position'] == 1:
            victories.append(result)

    victories = sorted(victories, key=lambda i: i['date'], reverse=True)
    latest = sorted(results, key=lambda i: i['date'], reverse=True)
    if len(latest) >= 5:
        latest = latest[:5]  # List the driver's 5 latest races

    # Get image
    driver_ref = driver['driverRef']
    img_path = image_handler.build_image_path(driver_ref , 'drivers')
    return render_template('drivers-instance.html', name=name, code=code,
                           dob=dob, nation=nationality, number=number, teams=teams,
                           url=url, img_path=img_path, victories=victories, latest=latest, bio=bio,
                           constructor=cur_constructor)

@app.route('/constructors')
def constructor_instance():
    constructor_id = int(request.args['id'])
    constructor = db.get_constructor('constructorId', constructor_id)
    name = constructor['name']
    nation = constructor['nationality']
    url = constructor['url']
    bio = constructor['bio']
    top_driver = {'id': constructor['topDriverId'], 'name': constructor['topDriverName'],
                  'points': constructor['topDriverPoints']}
    team_drivers = db.get_drivers('constructor.id' , constructor_id)

    wins = db.get_constructor_standings_from_position(1,constructor_id)
    wins = sorted(wins, key=lambda i: i['date'], reverse=True)
    total_wins = len(wins)
    if total_wins >= 5:
        wins = wins[:5]  # Take the 5 latest victories

    latest_races = db.get_constructor_results('constructorId' , constructor_id)
    latest_races = sorted(latest_races, key=lambda i: i['date'], reverse=True)
    if len(latest_races) >= 5:
        latest_races = latest_races[:5]

    # Get image
    constructor_ref = constructor['constructorRef']
    img_path = image_handler.build_image_path(constructor_ref , 'constructors')

    return render_template('constructors-instance.html', name=name, nation=nation,
                           drivers=team_drivers, wins=wins, img_path=img_path, url=url, bio=bio,
                           total_wins=total_wins, top_driver=top_driver, latest_races=latest_races)

@app.route('/circuits')
def circuit_instance():
    circuit_id = request.args['id']
    circuit = db.get_circuit('circuitId' ,circuit_id)
    name = circuit['name']
    location = circuit['location']
    lat = circuit['lat']
    longitude = circuit['lng']
    country = circuit['country']
    circuit_id = circuit['circuitId']
    url = circuit['url']
    bio = circuit['bio']

    latest_race = db.get_circuit_latest_race(circuit_id)
    latest_race_name = latest_race['name']
    latest_race_id = latest_race['raceId']
    latest_race_results = db.get_result('raceId' , latest_race_id)
    latest_race_results = sorted(latest_race_results, key=lambda i: i['position'])

    fastest_lap_times = db.get_lap_times('circuitId' , circuit_id)
    if len(fastest_lap_times) >= 5:
        fastest_lap_times = fastest_lap_times[:5]

    # Get image
    circuit_ref = circuit['circuitRef']
    img_path = image_handler.build_image_path(circuit_ref , 'circuits')

    return render_template('circuits-instance.html', name=name, lat=lat,
                           long=longitude, locality=location, country=country, url=url,
                           img_path=img_path, circuit_id=circuit_id, latest_results=latest_race_results,
                           latest_race_name=latest_race_name, bio=bio, lap_times=fastest_lap_times)
@app.route('/')
def home():
    today = date.today()
    currentMonth = str(today).split("-")[1]
    currentMonthName = today.strftime('%B')
    currentDay = str(today).split("-")[2]
    currentYear = str(today).split("-")[0]

    recentRaces = db.get_races('year',int(currentYear))
    currentMonthDrivers = db.get_drivers_from_month(currentMonth)
    popularDrivers = db.get_random_drivers()
    popularCircuits = db.get_random_circuits()
    sortedConstructorSeasonLeaders = db.get_constructor_standings_from_year(currentYear)
    sortedDriverSeasonLeaders = db.get_driver_standings_from_year(currentYear)

    recentRaces = recentRaces[:5]
    sortedConstructorSeasonLeaders = sortedConstructorSeasonLeaders[:5]
    sortedDriverSeasonLeaders = sortedDriverSeasonLeaders[:5]

    return render_template('home.html', recentRaces=recentRaces, monthDrivers=currentMonthDrivers,
                           driverSeasonStandings=sortedDriverSeasonLeaders,
                           constructorSeasonStandings=sortedConstructorSeasonLeaders,
                           year=currentYear, monthName=currentMonthName, popularCircuits=popularCircuits,
                           popularDrivers=popularDrivers)

def get_driver_list(select, query):
    """
    Purpose:
        Seach drivers using various selectors
    
    Args:
        select: {str}   selector type
        query:  {str}   data to be searched for in the collection

    Returns:
        {list} List of search results
    """
    driver_list = list()
    if query == '':
        driver_list = list(db.drivers.find()) 
        return driver_list
    if select == 'constructor':
        field = 'constructor.name'
        driver_list = list(db.drivers.find({field: {'$regex': f'.*{query}.*?', '$options': 'i'}}))
    elif select == 'nationality':
        driver_list = list(db.drivers.find({select: {'$regex': f'.*{query}.*?', '$options': 'i'}}))
    else:
        driver_list = driver_name_search(query)
    return driver_list

def driver_name_search(query):
    """
    Purpose:
        Seach driver names with a query
    
    Args:
        query: {str} data to be sarched for in the collection

    Returns:
        {list} List of search results
    """
    # Search token in forenames and surnames
    tokens = query.split()
    if len(tokens) == 1:
        driver_list = list(search('forename', db.drivers, query))
        surname_list = search('surname', db.drivers, query)

        for driver in surname_list:
            if driver not in driver_list:
                driver_list.append(driver)
    else:
        # Search first token in forenames, search other tokens in surnames
        driver_list = list(db.drivers.find({'forename': {'$regex': f'{tokens[0]}?', '$options': 'i'}}))
        surname_cursors = []

        for i in range(1, len(tokens)):
            surname_cursors.append(db.drivers.find({'surname': {'$regex': f'{tokens[i]}?', '$options': 'i'}}))
        for cursor in surname_cursors:
            for driver in cursor:
                if driver not in driver_list:
                    driver_list.append(driver)
    return driver_list

def get_circuit_list(select, query):
    """
    Purpose:
        Seach circuits using various selectors
    
    Args:
        select: {str}   selector type
        query:  {str}   data to be searched for in the collection

    Returns:
        {list} List of search results
    """
    circuit_list = list()
    if query == '':
        circuit_list = list(db.circuits.find())
        return circuit_list
    
    if select == 'name' or select == 'most_recent_race':
        circuit_list = list(db.circuits.find({select: {'$regex': f'.*{query}.*?', '$options': 'i'}}))
    else:
        circuit_list = circuit_location_search(query)
    return circuit_list

def circuit_location_search(query):
    """
    Purpose:
        Seach circuit locations with a query
    
    Args:
        query: {str} data to be sarched for in the collection

    Returns:
        {list} List of search results
    """
    # Search token in forenames and surnames
    tokens = query.split()
    circuit_list = list()
    if len(tokens) == 1:
        location_list = list(search('location', db.circuits, query))
        country_list = search('country', db.circuits, query)

        for circuit in country_list:
            if circuit not in location_list:
                location_list.append(circuit)
        circuit_list = location_list
    else:
        location_cursors = list()
        country_cursors = list()
        for i in range(0, len(tokens)):
            location_cursors.append(db.circuits.find({'location': {'$regex': f'{tokens[i]}?', '$options': 'i'}}))
            country_cursors.append(db.circuits.find({'location': {'$regex': f'{tokens[i]}?', '$options': 'i'}}))

        for cursor in location_cursors:
            for circuit in cursor:
                if circuit not in circuit_list:
                    circuit_list.append(circuit)
        for cursor in country_cursors:
            for circuit in cursor:
                if circuit not in circuit_list:
                    circuit_list.append(circuit)
    return circuit_list

def search(field, collection, query):
    """
    Purpose:
        Search desired field with a query
    
    Args:
        field:      {str}        field to search through   
        collection: {collection} target PyMongo database collection
        query:      {str}        data to be sarched for in the collection

    Returns:
        {list} List of search results
    """
    if query == '':
        return list(collection.find())
    else:
        return list(collection.find({field: {'$regex': f'.*{query}.*?', '$options': 'i'}}))

def sort_models(models, sort, filtered):
    if sort == '' or sort == 'relevance':
        # sort by relevance
        return models
    elif len(models) == 0:
        # return if no results
        return models
    elif 'driverId' in models[0]:
        if filtered == 'name' or filtered == '':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x:(remove_accents(x['forename']), remove_accents(x['forename'])))
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x:(remove_accents(x['forename']), remove_accents(x['forename'])), reverse=True)
        elif filtered == 'nationality':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x: x['nationality'])
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x: x['nationality'], reverse=True)
        elif filtered == 'constructor':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['constructor']['name']))
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['constructor']['name']), reverse=True)
    elif 'constructorId' in models[0]:
        if filtered == 'name' or filtered == '':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['name']))
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['name']), reverse=True)
        elif filtered == 'nationality':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x: x['nationality'])
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x: x['nationality'], reverse=True)
        elif filtered == 'topDriverName':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['topDriverName']))
            elif sort == 'reverse_alpha':   
                # reverse alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['topDriverName']), reverse=True)         
    elif 'circuitId' in models[0]:
        if filtered == 'name' or filtered == '':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['name']))
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['name']), reverse=True)
        elif filtered == 'location':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x:(remove_accents(x['location']), remove_accents(x['country'])))
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x:(remove_accents(x['location']), remove_accents(x['country'])), reverse=True)
        elif filtered == 'most_recent_race':
            if sort == 'alpha':
                # alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['most_recent_race']))
            elif sort == 'reverse_alpha':
                # reverse alphabetical sort
                return sorted(models, key=lambda x: remove_accents(x['most_recent_race']), reverse=True)

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])

if __name__ == '__main__':
    app.run(debug=True)