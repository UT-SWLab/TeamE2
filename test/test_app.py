import unittest
from flask import Flask, render_template, request
from flask_pymongo import pymongo
from app import search

class TestApp(unittest.TestCase):
    
    #I have only writtent test cases for the collections that we use in App.py
    @classmethod
    def setUpClass(cls):
        print('setupClass')

    def setUp(self):
        dbUsername = 'formulaOne'  
        dbPassword = '0WpPVH6LdcHiwdct'
        CONNECTION_STRING = "mongodb+srv://" + dbUsername + ":" + dbPassword + "@formulaonedb.bue6f.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"
        client = pymongo.MongoClient(CONNECTION_STRING)
        db = client.get_database('FormulaOneDB')
        self.db = db

    def test_createDriver(self):
        desiredDocumentCount = self.db.drivers.count_documents({'forename' : 'Samuel'})
        desiredDocumentCount+=1
        self.db.drivers.insert_one({'forename' : 'Samuel'})
        actualDocumentCount = self.db.drivers.count_documents({'forename' : 'Samuel'})
        self.assertEqual(desiredDocumentCount,actualDocumentCount)
    
    def test_readDriver(self):
        desiredCurrentTeam = "Mercedes"
        mercedesDrivers = self.db.drivers.find({'constructor.name' : 'Mercedes'})
        for drivers in mercedesDrivers:
            self.assertEqual(desiredCurrentTeam , drivers['constructor']['name'])
    
    def test_updateDriver(self):
        desiredDriver = {
            'forename' : 'Samuel',
            'surename' : 'Yeboah',
            'dob' : "1998-11-15",
            'nationality' : 'American',
            'url' : "na",
            'bio' : "na",
            'constructor' : "Mercedes",
            'all_constructors' : [],
        }

        self.db.drivers.insert_one(desiredDriver)

        self.db.drivers.update_one(
            {'forename' : desiredDriver['forename']}, 
            {'$set' : {'bio' : "The coolest man on the planet. He is the best driver in america."}})
        
        driver = self.db.drivers.find_one({'forename' : desiredDriver['forename']})
        desiredBio = "The coolest man on the planet. He is the best driver in america."
        self.assertEqual(desiredBio,driver['bio'])
        self.db.drivers.delete_many({'forename' : desiredDriver['forename']})
    
    def test_deleteDriver(self):
        desiredDriver = {
            'forename' : 'John',
            'surename' : 'Yeboah',
            'dob' : "1998-11-15",
            'nationality' : 'American',
            'url' : "na",
            'bio' : "na",
            'constructor' : "Mercedes",
            'all_constructors' : [],
        }

        self.db.drivers.insert_one(desiredDriver)

        desiredDriverCount = 0
        result = self.db.drivers.delete_many({'forename' : 'John'})
        driverCount = self.db.drivers.count_documents({'forename' : 'John'})
        self.assertEqual(desiredDriverCount , driverCount)
        self.db.drivers.delete_many({'forename' : desiredDriver['forename']})
    
    def test_createCircuit(self):
        desiredCircuit = {
            'name' : 'LSU Grand Prix',
            'location' : 'Louisiana'
        }

        self.db.circuits.insert_one(desiredCircuit)

        dbCircuit = self.db.circuits.find_one({'name' : 'LSU Grand Prix'})

        self.assertEqual(desiredCircuit['name'] ,  dbCircuit['name'])

        self.db.circuits.delete_many({'name' : 'LSU Grand Prix'})
    
    def test_retrieveMultipleCircuits(self):
        circuits = self.db.circuits.find({'country' : 'Austrlia'})
        desiredCountry = 'Australia'
        for circuit in circuits:
            self.assertEqual(desiredCountry , circuit['country'])

    def test_updatingCircuits(self):
        desiredCircuit = {
            'name' : 'Clemson Grand Prix',
            'location' : 'South Carolina'
        }

        self.db.circuits.insert_one(desiredCircuit)

        self.db.circuits.update_one({'name' : 'Clemson Grand Prix'} , {'$set' : {'bio' : 'New Bio has been created'}})

        actualBio = self.db.circuits.find_one({'name' : 'Clemson Grand Prix'})
        
        desiredBio = 'New Bio has been created'

        self.assertEqual(desiredBio , actualBio['bio'])

        self.db.circuits.delete_many({'name' : 'Clemson Grand Prix'})

    def test_deletingCircuits(self):
        desiredCircuit = {
            'name' : 'Aggie Grand Prix',
            'location' : 'College Station'
        }

        self.db.circuits.insert_one(desiredCircuit)

        desiredCircuitCount = 0

        self.db.circuits.delete_many({'name' : 'Aggie Grand Prix'})
        actualCircuitCount = self.db.circuits.count_documents({'name' : 'Aggie Grand Prix'})

        self.assertEqual(desiredCircuitCount , actualCircuitCount)
    
    def test_creatingConstructors(self):
        constructor = {
            'name' : 'Kevin''s Team',
            'topDriverName' : 'Sam'
        }

        self.db.constructors.insert_one(constructor)
        actualCircuit = self.db.constructors.find_one({'name' : 'Kevin''s Team'})

        self.assertEqual('Kevin''s Team' , actualCircuit['name'])

        self.db.constructors.delete_many({'name' : 'kevin''s Team'})
    
    def test_retrieveConstructors(self):
        desiredNationality = 'British'
        constructors = self.db.constructors.find({'nationality' : desiredNationality})
        for constructor in constructors:
            self.assertEqual(desiredNationality , constructor['nationality'])

    def test_updatingConstructors(self):
        constructor = {
            'name' : 'Edies Team',
            'topDriverName' : 'Sam',
            'bio' : ''
        }

        self.db.constructors.insert_one(constructor)

        desiredBio = "We have a new bio"
        result = self.db.constructors.update_one({'name' : 'Edies Team' } , {'$set' : {'bio' : desiredBio}})
        
        actualCircuit = self.db.constructors.find_one({'name' : 'Edies Team'})
        self.assertEqual(desiredBio , actualCircuit['bio'])

    def test_deletingConstructors(self):
        constructor = {
            'name' : 'A Team',
            'topDriverName' : 'Sam',
            'bio' : ''
        }


        desiredDocumentCount = self.db.constructors.count_documents({'name' : 'A Team'})
        self.db.constructors.insert_one(constructor)
        actualDocumentCount = self.db.constructors.count_documents({'name' : 'A Team'})
        self.assertEqual(1 , actualDocumentCount)
        self.db.constructors.delete_many({'name' : 'A Team'})
        actualDocumentCount = self.db.constructors.count_documents({'name' : 'A Team'})
        self.assertEqual(desiredDocumentCount, actualDocumentCount)

    def test_createResults(self):
        result = {
            'points' : 10,
            'rank' : "2",
            'driverName' : 'Samuel Yeboah',
            'constructorName' : 'A Team'
        }
        
        self.db.results.insert_one(result)
        
        actualResult = self.db.results.find_one({'driverName' : result['driverName']})
        desiredResultName = 'Samuel Yeboah'
        self.assertEqual(desiredResultName , actualResult['driverName'])
    
    def test_readResults(self):
        driverName = "Lewis Hamilton"

        drivers = self.db.results.find({'name' : driverName})
        for driver in drivers:
            self.assertEqual(driverName , driver['name'])
    
    def test_updateResults(self):
        result = {
            'points' : 10,
            'rank' : "2",
            'driverName' : 'John hopkins',
            'constructorName' : 'A Team'
        }
        
        self.db.results.insert_one(result)
        
        actualResult = self.db.results.find_one({'driverName' : result['driverName']})
        driverName = actualResult['driverName']

        desiredConstructor = "Carolina Panthers"
        results = self.db.results.update_one({'driverName' : driverName} , {'$set': {'constructorName' : desiredConstructor}})
        actualResult = self.db.results.find_one({'constructorName' : desiredConstructor})

        actualConstructorName = actualResult['constructorName']

        self.assertEqual(desiredConstructor , actualConstructorName)

        self.db.results.delete_many({'driverName' : result['driverName']})
        
    def test_deleteResults(self):
        self.db.results.delete_many({'driverName' : 'Samuel Yeboah'})

        desiredCount = 0
        actualCount = self.db.results.count_documents({ 'driverName' : 'Samuel Yeboah'})

        self.assertEqual(desiredCount , actualCount)

    def test_createConstructorStandings(self):
        desiredDocumentCount = self.db.constructors_standings.count_documents({'constructorName' : 'SamuelYeboah' })
        desiredDocumentCount+=1
        self.db.constructors_standings.insert_one({'constructorName' : 'SamuelYeboah'})
        actualCount = self.db.constructors_standings.count_documents({'constructorName' : 'SamuelYeboah'})
        self.assertEqual(desiredDocumentCount , actualCount)

    def test_readConstructorStandings(self):
        desiredConstructorName = "Ferrari"
        constructors = self.db.constructors_standings.find({'constructorName' : desiredConstructorName})
        for constructor in constructors:
            self.assertEqual(desiredConstructorName , constructor['constructorName'])

    def test_updateConstructorStandings(self):
        desiredRaceName = 'LSU Grand Prix'
        self.db.constructors_standings.insert_one({'constructorName' : 'Samuel Yeboah' , "raceName" : ""})
        standings = self.db.constructors_standings.find_one({'constructorName' : 'Samuel Yeboah'})
        self.db.constructors_standings.update_one({'constructorName' : 'Samuel Yeboah'} , {'$set' : {'raceName' : desiredRaceName}})
        standings = self.db.constructors_standings.find_one({'raceName' : desiredRaceName})
        self.assertEqual(desiredRaceName , standings['raceName'])
        
    def test_deleteConstructorStandings(self): 
        self.db.constructors_standings.delete_many({'constructorName' : "John Hopkins"})
        actualDocumentCount = self.db.constructors_standings.count_documents({'constructorName' : 'John Hopkins' })
        desiredDocumentCount = 0
        self.assertEqual(desiredDocumentCount , actualDocumentCount)


    def test_SpecificSearch(self):
        field = 'forename'
        collection = self.db.drivers
        query = 'Samuel'
        self.db.drivers.insert_one({'forename' : 'Samuel'})
        drivers = search(field , collection, query)
        for driver in drivers:
            self.assertEquals(driver['forename'] , query)
    
    def test_GeneralSearch(self):
        field = 'forename'
        collection =  self.db.drivers
        query = ''
        drivers = search(field, collection, query)
        drivers = list(drivers)
        desiredNumDrivers = collection.count_documents({})
        self.assertEquals(desiredNumDrivers,len(drivers))

    

       
    
        



        

    
    


if __name__ == '__main__':
    unittest.main()
