# 1st party packages
import os
import unicodedata

# 3rd party packages
from flask_pymongo import pymongo


class Image_Handler(object):
    @staticmethod
    def build_image_path(objectRef, objectType):
        # Default file image
        NO_IMG = 'images/no_img.png'

        img_path = f'images/{objectType}/{objectRef}.png'
        if not os.path.exists(f'./static/{img_path}'):
            img_path = NO_IMG
        return img_path
        

class F1_Database(object):

    def __init__(self, username='formulaOne', password='0WpPVH6LdcHiwdct'):
        self.username = username
        self.password = password
        CONNECTION_STRING = f"mongodb+srv://{username}:{password}@formulaonedb.bue6f.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"
        client = pymongo.MongoClient(CONNECTION_STRING)
        self.db = client.get_database('FormulaOneDB')
    

    def get_driver(self, field , query):
        driver = self.db.drivers.find_one({field : query})
        return driver


    def get_regex_drivers(self, field, regex_query):
        drivers = self.db.drivers.find({field: {'$regex': f'.*{regex_query}.*?', '$options' : 'i'}})
        return list(drivers)


    def get_regex_circuits(self, field, regex_query):
        circuits = self.db.circuits.find({field: {'$regex': f'.*{regex_query}.*?', '$options' : 'i'}})
        return list(circuits)


    def get_all_drivers(self):
        drivers = self.db.drivers.find()
        return list(drivers)


    def get_all_circuits(self):
        circuits = self.db.circuits.find()
        return list(circuits)


    def get_all_constructors(self):
        constructors = self.db.constructors.find()
        return list(constructors)


    def get_constructor(self, field, query):
        constructor = self.db.constructors.find_one({field : query})
        return constructor


    def get_circuit(self, field, query):
        circuit = self.db.circuits.find_one({field: query})
        return circuit


    def get_drivers(self, field, query):
        driver_list = self.db.drivers.find({field : query})
        return list(driver_list)


    def get_races(self, field, query):
        races = self.db.races.find({field : query})
        races = list(races)
        return races


    def get_result(self, field, query):
        result_list = self.db.results.find({field : query})
        return list(result_list)


    def get_driver_standings_from_year(self, year):
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


    def get_constructor_standings_from_year(self, year):
        year = int(year)
        results = self.db.results.find({'year': year})
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
                image_path = Image_Handler.build_image_path(circuit_ref , 'circuits')
                tempDict = {'circuit_ref': circuit_ref, 'name': name, 'image_path': image_path, 'id': circuit['circuitId']}
                randomCircuits.append(tempDict)
        return randomCircuits


    def get_random_drivers(self):
        drivers = self.db.drivers.aggregate([{'$sample': {'size' : 10}}])
        popularDrivers = []
        for driver in drivers:
            driver_ref = driver['driverRef']
            name = driver['forename'] + "  " + driver['surname']
            image_path = Image_Handler.build_image_path(driver_ref , 'drivers')
            tempDict = {'driver_ref' : driver_ref, 'image_path' : image_path, 'name' : name, 'id': driver['driverId']}
            popularDrivers.append(tempDict)
        return popularDrivers


    def get_lap_times(self, field, query):
        results = self.get_result(field, query)
        lap_times = sorted(results, key=lambda i: (i['fastestLapTime']))
        return lap_times


    def get_circuit_latest_race(self, circuitId):
        races_list = self.db.races.find({'circuitId': int(circuitId)})  # Get all races held at this circuit
        races = list(races_list)
        latest_race_info = ""
        results = None

        races = sorted(races, key=lambda i: i['date'], reverse=True)
        for race in races:
            results = self.db.results.find({'raceId': race['raceId']})  # Results of the latest race
            results = list(results)
            if len(results) != 0:  # Ergast returns races that are scheduled for the future as well, so we have to make sure
                # the latest race has actually happened
                latest_race_info = {'year': race['year'], "name" : race['name'], 'raceId' : race['raceId']}
                break
        return latest_race_info


    def get_constructor_standings_from_position(self, position, constructorId):
        constructors  = self.db.constructor_standings.find({'constructorId' : constructorId, 'position' : position})
        return list(constructors)


    def get_constructor_results(self, field, query):
        races = self.db.constructor_results.find({field: query})
        return list(races)


    def get_drivers_from_month(self, month):
        regExDate = "....-" + month + "-.."
        drivers = self.db.drivers.find({"dob" : {'$regex' : regExDate}})
        drivers = list(drivers)
        finalDriverList = []
        for driver in drivers:
            driver_ref = driver['driverRef']
            name  = driver['forename'] + " " + driver['surname']
            image_path = Image_Handler.build_image_path(driver_ref, 'drivers')
            tempDict = {'driver_ref': driver_ref, 'image_path': image_path, 'name': name, 'id': driver['driverId']}
            finalDriverList.append(tempDict)
        return finalDriverList
    

class Search(object):
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
            driver_list = data.db.get_all_drivers()
            return driver_list
        if select == 'constructor':
            field = 'constructor.name'
            driver_list = data.db.get_regex_drivers(field,query)
        elif select == 'nationality':
            driver_list = data.db.get_regex_drivers(select,query)
        else:
            driver_list = driver_name_search(query)
        return driver_list

    def driver_name_search(self, query):
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
        driver_list = []
        if len(tokens) == 1:
            forname_list = data.db.get_regex_drivers('forename', query)
            surname_list = data.db.get_regex_drivers('surname' , query)
            for driver in surname_list:
                if driver not in forname_list:
                    forname_list.append(driver)
            driver_list = forname_list
        else:
            # Search first token in forenames, search other tokens in surnames
            forename_list = data.db.get_regex_drivers('forename', query)
            surname_list = []
            
            for i in range(1, len(tokens)):
                surname_list += data.db.get_regex_drivers('surname' , tokens[i])
            driver_list = forename_list + surname_list
        return driver_list

    def get_circuit_list(self, select, query):
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
            circuit_list = data.db.get_all_circuits()
            return circuit_list
        
        if select == 'name' or select == 'most_recent_race':
            circuit_list = data.db.get_regex_circuits(select, query)
        else:
            circuit_list = circuit_location_search(query)
        return circuit_list

    def circuit_location_search(self, query):
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
            location_list = data.db.get_circuit('location' , query)
            country_list = data.db.get_circuit('country' , query)

            for circuit in country_list:
                if circuit not in location_list:
                    location_list += circuit
            circuit_list = location_list
        else:
            location_list = list()
            country_list = list()
            for i in range(0, len(tokens)):
                location_list += data.db.get_regex_circuits('location' , tokens[i])
                country_list += data.db.get_regex_circuits('location' , tokens[i])
            for circuit in location_list:
                if circuit not in circuit_list:
                    circuit_list += circuit
            for circuit in country_list:
                if circuit not in country_list:
                    country_list += circuit
        return circuit_list

class Sort(object):
    def sort_models(self, models, sort, filtered):
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
                    return sorted(models, key=lambda x:(self.remove_accents(x['surname']),
                        self.remove_accents(x['forename'])))
                elif sort == 'reverse_alpha':
                    # reverse alphabetical sort
                    return sorted(models, key=lambda x:(self.remove_accents(x['surname']),
                        self.remove_accents(x['forename'])), reverse=True)
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
                    return sorted(models, key=lambda x: self.remove_accents(x['constructor']['name']))
                elif sort == 'reverse_alpha':
                    # reverse alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['constructor']['name']),
                        reverse=True)
        elif 'constructorId' in models[0]:
            if filtered == 'name' or filtered == '':
                if sort == 'alpha':
                    # alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['name']))
                elif sort == 'reverse_alpha':
                    # reverse alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['name']),
                        reverse=True)
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
                    return sorted(models, key=lambda x: self.remove_accents(x['topDriverName']))
                elif sort == 'reverse_alpha':   
                    # reverse alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['topDriverName']),
                        reverse=True)         
        elif 'circuitId' in models[0]:
            if filtered == 'name' or filtered == '':
                if sort == 'alpha':
                    # alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['name']))
                elif sort == 'reverse_alpha':
                    # reverse alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['name']),
                        reverse=True)
            elif filtered == 'location':
                if sort == 'alpha':
                    # alphabetical sort
                    return sorted(models, key=lambda x:(self.remove_accents(x['location']),
                        self.remove_accents(x['country'])))
                elif sort == 'reverse_alpha':
                    # reverse alphabetical sort
                    return sorted(models, key=lambda x:(self.remove_accents(x['location']), 
                        self.remove_accents(x['country'])), reverse=True)
            elif filtered == 'most_recent_race':
                if sort == 'alpha':
                    # alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['most_recent_race']))
                elif sort == 'reverse_alpha':
                    # reverse alphabetical sort
                    return sorted(models, key=lambda x: self.remove_accents(x['most_recent_race']),
                        reverse=True)

    def remove_accents(self, input_str):
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return u"".join([c for c in nfkd_form if not unicodedata.combining(c)])
    