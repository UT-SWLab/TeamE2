import pymongo as pymongo

dbUsername = 'formulaOne'
dbPassword = '0WpPVH6LdcHiwdct'
CONNECTION_STRING = "mongodb+srv://" + dbUsername + ":" + dbPassword + "@formulaonedb.bue6f.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('FormulaOneDB')


def results():
    db_results = db.results.find()
    results = []

    for result in db_results:
        results.append({'_id': result['_id'], 'driverId': result['driverId'],
                        'constructorId': result['constructorId'], 'resultId': result['resultId'],
                        'raceId': result['raceId']})
    count = 0
    for result in results:
        try:
            count = count + 1
            if count == 500:
                print(result['resultId'])
                count = 0
            driver = db.drivers.find_one({'driverId': result['driverId']})
            constructor = db.constructors.find_one({'constructorId': result['constructorId']})
            race = db.races.find_one({'raceId': result['raceId']})
            circuit = db.circuits.find_one({'circuitId': race['circuitId']})
            circuitId = circuit['circuitId']
            circuitName = circuit['name']
            driverName = driver['forename'] + " " + driver['surname']
            constructorName = constructor['name']
            raceName = str(race['year']) + " " + race['name']
            raceDate = race['date']
            db.results.update_one({"_id": result["_id"]}, {"$set": {"driverName": driverName}})
            db.results.update_one({"_id": result["_id"]}, {"$set": {"constructorName": constructorName}})
            db.results.update_one({"_id": result["_id"]}, {"$set": {"raceName": raceName}})
            db.results.update_one({"_id": result["_id"]}, {"$set": {"raceDate": raceDate}})
            db.results.update_one({"_id": result["_id"]}, {"$set": {"circuitId": circuitId}})
            db.results.update_one({"_id": result["_id"]}, {"$set": {"circuitName": circuitName}})
        except:
            print("ERROR: " + str(result['resultId']))


def constructor_standings():
    db_standings = db.constructor_standings.find()
    standings = []

    for s in db_standings:
        standings.append({'_id': s['_id'], 'raceId': s['raceId'], 'constructorId': s['constructorId'], })

    count = 0
    for s in standings:
        try:
            count = count + 1
            if count == 500:
                count = 0
                print(count)
            constructor = db.constructors.find_one({'constructorId': s['constructorId']})
            race = db.races.find_one({'raceId': s['raceId']})
            circuit = db.circuits.find_one({'circuitId': race['circuitId']})

            constructorName = constructor['name']
            raceName = str(race['year']) + ' ' + race['name']
            raceDate = race['date']
            circuitName = circuit['name']
            circuitId = circuit['circuitId']

            db.constructor_standings.update_one({"_id": s["_id"]}, {"$set": {"constructorName": constructorName}})
            db.constructor_standings.update_one({"_id": s["_id"]}, {"$set": {"raceName": raceName}})
            db.constructor_standings.update_one({"_id": s["_id"]}, {"$set": {"raceDate": raceDate}})
            db.constructor_standings.update_one({"_id": s["_id"]}, {"$set": {"circuitName": circuitName}})
            db.constructor_standings.update_one({"_id": s["_id"]}, {"$set": {"circuitId": circuitId}})
        except:
            print("ERROR: " + str(s['_id']))


def best_driver():
    db_constructors = db.constructors.find()
    constructors = []

    for c in db_constructors:
        constructors.append({'_id': c['_id'], 'constructorId': c['constructorId'],
                             'constructorName': c['name']})
    for c in constructors:
        try:
            print(c['constructorName'])
            total_points = {}
            db_results = db.results.find({'constructorId': c['constructorId']})

            # Initialize points for each driver
            for result in db_results:
                driverId = result['driverId']
                total_points[str(driverId)] = 0

            # Add up all points for each driver
            db_results = db.results.find({'constructorId': c['constructorId']})
            for result in db_results:
                driverId = result['driverId']
                total_points[str(driverId)] = total_points[str(driverId)] + result['points']
            top_driver = max(total_points, key=total_points.get)  # driverId of top driver

            db_top_driver = db.drivers.find_one({'driverId': int(top_driver)})
            top_driver_name = db_top_driver['forename'] + " " + db_top_driver['surname']
            top_driver_points = total_points[top_driver]

            db.constructors.update_one({"constructorId": c['constructorId']},
                                       {"$set": {"topDriverId": int(top_driver)}})
            db.constructors.update_one({"constructorId": c['constructorId']},
                                       {"$set": {"topDriverName": top_driver_name}})
            db.constructors.update_one({"constructorId": c['constructorId']},
                                       {"$set": {"topDriverPoints": top_driver_points}})
            # print(c['constructorName'] + "'s top driver is " + top_driver_name + " with " + str(
            #     top_driver_points) + " points")
        except:
            print("ERROR with " + c['constructorName'])


def constructor_results():
    # query = {"position": {"$exists": False}}
    # db_results = list(db.constructor_results.find(query))
    db_results = db.constructor_results.find()
    results = []

    for s in db_results:
        results.append(
            {'_id': s['_id'], 'raceId': s['raceId'], 'constructorId': s['constructorId'], 'points': s['points']})

    count = 0
    for s in results:
        try:
            count = count + 1
            if count == 100:
                print(count)
                count = 0
            constructor = db.constructors.find_one({'constructorId': s['constructorId']})
            race = db.races.find_one({'raceId': s['raceId']})
            circuit = db.circuits.find_one({'circuitId': race['circuitId']})
            if db.constructor_standings.count_documents(
                    {'raceId': s['raceId'], 'constructorId': s['constructorId']}) != 0:

                standing = db.constructor_standings.find_one(
                    {'raceId': s['raceId'], 'constructorId': s['constructorId']})

                position = standing['position']
            else:
                position = '\\N'
            constructorName = constructor['name']
            raceName = str(race['year']) + ' ' + race['name']
            raceDate = race['date']
            circuitName = circuit['name']
            circuitId = circuit['circuitId']

            db.constructor_results.update_one({"_id": s["_id"]}, {"$set": {"constructorName": constructorName}})
            db.constructor_results.update_one({"_id": s["_id"]}, {"$set": {"raceName": raceName}})
            db.constructor_results.update_one({"_id": s["_id"]}, {"$set": {"raceDate": raceDate}})
            db.constructor_results.update_one({"_id": s["_id"]}, {"$set": {"position": position}})
            db.constructor_results.update_one({"_id": s["_id"]}, {"$set": {"circuitName": circuitName}})
            db.constructor_results.update_one({"_id": s["_id"]}, {"$set": {"circuitId": circuitId}})
        except:
            print("ERROR: " + str(s['_id']))



if __name__ == '__main__':
    results()
    constructor_standings()
    best_driver()
    constructor_results()
