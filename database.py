from flask_pymongo import pymongo

class FormulaOneDatabase(object):

    def __init__(self , username , password):
        self.username = username
        self.password = password
        self.CONNECTION_STRING = "mongodb+srv://" + username + ":" + password + "@formulaonedb.bue6f.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"
        client = pymongo.MongoClient(CONNECTION_STRING)
        self.db = client.get_database('FormulaOneDB')
    
    def get_driver(self, field , query):
        driver = self.db.drivers.find_one({field : query})
        return driver
    
    def get_constructor(self, field, query):
        constructor = self.db.constructors.find_one({field : query})
        return constructor

    def get_circuit(self, field , query):
        circuit = self.db.circuits.find_one({field: query})
        return circuit

    def get_drivers(self,field , query):
        driver_list = self.db.drivers.find({field : query})
        return list(driver_list)

    def get_races(self, field , query):
        races = self.db.races.find({field : query})
        races = list(races)
        return races

    def get_result(self ,field , query):
        result_list = self.db.results.find({field : query})
        return list(result_list)

    def get_driver_standings_from_year(self , year):
        results = self.db.results.find({'year' : int(year)})
        seasonDriverStandings = {}
        for result in results:
            driver = result['driverId']
            driverPoints = result['points']
            driverName = result['driverName']
            if driver in seasonDriverStandings:
                currentPoints = seasonDriverStandings[driver][1]
                seasonDriverStandings[driver][1] = currentPoints + driverPoints
            else:
                seasonDriverStandings[driver] = [driverName, driverPoints, driver]

        sortedDriverSeasonLeaders = []
        for key in sorted(seasonDriverStandings.keys(), key=lambda k: seasonDriverStandings[k][1], reverse=True):
            sortedDriverSeasonLeaders.append(seasonDriverStandings[key])
        return sortedDriverSeasonLeaders

    def get_constructor_standings_from_year(self,year):
        year = int(year)
        results = db.results.find({'year': year})
        seasonConstructorStandings = {}
        for result in results:
            constructor = result['constructorId']
            constructPoints = result['points']
            constructorName = result['constructorName']
            if constructor in seasonConstructorStandings:
                currentPoints = seasonConstructorStandings[constructor][1]
                seasonConstructorStandings[constructor][1] = currentPoints + constructPoints
            else:
                seasonConstructorStandings[constructor] = [constructorName, constructPoints, constructor]
        
        sortedConstructorSeasonLeaders = []
        for key in sorted(seasonConstructorStandings.keys(), key=lambda k: seasonConstructorStandings[k][1], reverse=True):
            sortedConstructorSeasonLeaders.append(seasonConstructorStandings[key])
        return sortedConstructorSeasonLeaders
    
    def get_random_circuits(self):
        circuits = self.db.circuits.aggregate([{'$sample' : {'size' : 10}}])
        randomCircuits = []
        for circuit in circuits:
            if 'circuitRef' in circuit.keys():
                circuit_ref = circuit['circuitRef']
                name = circuit['name']
                image_path = f'images/circuits/{circuit_ref}.png'
                if not os.path.exists(f'./static/{image_path}'):
                    image_path = NO_IMG
                tempDict = {'circuit_ref': circuit_ref, 'name': name, 'image_path': image_path, 'id': circuit['circuitId']}
                randomCircuits.append(tempDict)
        return randomCircuits
    
    def get_random_drivers(self):
        drivers = self.db.drivers.aggregate([{'$sample': {'size' : 10}}])
        popularDrivers = []
        for driver in drivers:
            driver_ref = driver['driverRef']
            name = driver['forename'] + "  " + driver['surname']
            image_path = f'images/drivers/{driver_ref}.png'
            if not os.path.exists(f'./static/{image_path}'):
                image_path = NO_IMG
            tempDict = {'driver_ref' : driver_ref, 'image_path' : image_path, 'name' : name, 'id': driver['driverId']}
            popularDrivers.append(tempDict)
        return popularDrivers
    
    def get_lap_times(self,field , query):
        results = get_result(field,query)
        lap_times = sorted(results, key=lambda i: (i['fastestLapTime']))
        return lap_times
    
    def get_circuit_latest_race(self, circuitId):
        races_list = db.races.find({'circuitId': int(circuitId)})  # Get all races held at this circuit
        races = list(races_list)
        latest_race_info = ""
        results = None

        races = sorted(races, key=lambda i: i['date'], reverse=True)
        for race in races:
            results = db.results.find({'raceId': race['raceId']})  # Results of the latest race
            results = list(results)
            if len(results) != 0:  # Ergast returns races that are scheduled for the future as well, so we have to make sure
                # the latest race has actually happened
                latest_race_info = {'year': race['year'], "name" : race['name'], 'raceId' : race['raceId']}
                break
        return latest_race_info
    
    def get_constructor_standings_from_position(self , position, constructorId):
        constructors  = self.db.constructor_standings.find({'constructorId' : constructorId, 'position' : position})
        return list(constructors)
    
    def get_constructor_results(self,field,query):
        races = db.constructor_results.find({field: query})
        return list(races)
    


        
    