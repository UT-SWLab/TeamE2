# Import packages
from urllib.request import urlopen

import pymongo as pymongo
from bs4 import BeautifulSoup
import re


dbUsername = 'formulaOne'
dbPassword = '0WpPVH6LdcHiwdct'
CONNECTION_STRING = "mongodb+srv://" + dbUsername + ":" + dbPassword + "@formulaonedb.bue6f.gcp.mongodb.net/<dbname>?retryWrites=true&w=majority"

client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('FormulaOneDB')


def init_drivers():
    driver_list = db.drivers.find()
    drivers = []
    final_text = "No bio"
    for driver in driver_list:
        drivers.append(
            {'_id': driver['_id'], 'url': driver['url']})
        db.drivers.update_one({"_id": driver["_id"]}, {"$set": {"bio": final_text}})


def driver_bios():
    driver_list = db.drivers.find()
    drivers = []
    for driver in driver_list:
        drivers.append(
            {'_id': driver['_id'], 'url': driver['url'], 'driverId': driver['driverId'], 'bio': driver['bio']})
    for driver in drivers:
        print(driver['driverId'])
        if driver['bio'] != "No bio":
            continue
        try:
            # Specify url of the web page
            source = urlopen(driver['url']).read()
            # Make a soup
            soup = BeautifulSoup(source, 'lxml')
            # Extract the plain text content from paragraphs
            paragraphs = soup.findAll('p')
            final_text = "No bio"
            for paragraph in paragraphs:
                text = paragraph.text
                if text.count('.') >= 3:
                    final_text = text
                    break
            if final_text == "No bio":  # No 3 sentence paragraphs, take whatever we can get
                for paragraph in paragraphs:
                    text = paragraph.text
                    if text.count('.') >= 1:
                        final_text = text
                        break
            final_text = re.sub(r'\[.*?]+', '', final_text)
            # text = text.replace('\n', '')
            # print(final_text)
            db.drivers.update_one({"_id": driver["_id"]}, {"$set": {"bio": final_text}})
        except:
            print(driver)


def init_constructors():
    constructor_list = db.constructors.find()
    constructors = []
    final_text = "No bio"
    for constructor in constructor_list:
        constructors.append(
            {'_id': constructor['_id'], 'url': constructor['url']})
        db.constructors.update_one({"_id": constructor["_id"]}, {"$set": {"bio": final_text}})


def constructor_bios():
    constructor_list = db.constructors.find()
    constructors = []
    for c in constructor_list:
        constructors.append(
            {'_id': c['_id'], 'url': c['url'], 'constructorId': c['constructorId'], 'bio': c['bio']})
    for c in constructors:
        print(c['constructorId'])
        if c['bio'] != "No bio":
            first_word = c['bio'].split()[0]
            if first_word == "Coordinates:":
                pass
            else:
                continue
        try:
            # Specify url of the web page
            source = urlopen(c['url']).read()
            # Make a soup
            soup = BeautifulSoup(source, 'lxml')
            # Extract the plain text content from paragraphs
            paragraphs = soup.findAll('p')
            final_text = "No bio"
            for paragraph in paragraphs:
                text = paragraph.text
                if text.count('.') >= 3:
                    first_word = text.split()[0]
                    if first_word == "Coordinates:":
                        continue
                    final_text = text
                    break
            if final_text == "No bio":  # No 3 sentence paragraphs, take whatever we can get
                for paragraph in paragraphs:
                    text = paragraph.text
                    if text.count('.') >= 1:
                        first_word = text.split()[0]
                        if first_word == "Coordinates:":
                            continue
                        final_text = text
                        break
            final_text = re.sub(r'\[.*?]+', '', final_text)
            # text = text.replace('\n', '')
            # print(final_text)
            db.constructors.update_one({"_id": c["_id"]}, {"$set": {"bio": final_text}})
        except:
            print(c)


def init_circuits():
    circuits_list = db.circuits.find()
    circuits = []
    final_text = "No bio"
    for circuit in circuits_list:
        circuits.append(
            {'_id': circuit['_id'], 'url': circuit['url']})
        db.circuits.update_one({"_id": circuit["_id"]}, {"$set": {"bio": final_text}})


def circuit_bios():
    circuit_list = db.circuits.find()
    circuits = []
    for c in circuit_list:
        circuits.append(
            {'_id': c['_id'], 'url': c['url'], 'circuitId': c['circuitId'], 'bio': c['bio']})
    for c in circuits:
        print(c['circuitId'])
        if c['bio'] != "No bio":
            first_word = c['bio'].split()[0]
            if first_word == "Coordinates:":
                pass
            else:
                continue
        try:
            # Specify url of the web page
            source = urlopen(c['url']).read()
            # Make a soup
            soup = BeautifulSoup(source, 'lxml')
            # Extract the plain text content from paragraphs
            paragraphs = soup.findAll('p')
            final_text = "No bio"
            for paragraph in paragraphs:
                text = paragraph.text
                if text.count('.') >= 3:
                    first_word = text.split()[0]
                    if first_word == "Coordinates:":
                        continue
                    final_text = text
                    break
            if final_text == "No bio":  # No 3 sentence paragraphs, take whatever we can get
                for paragraph in paragraphs:
                    text = paragraph.text
                    if text.count('.') >= 1:
                        first_word = text.split()[0]
                        if first_word == "Coordinates:":
                            continue
                        final_text = text
                        break
            final_text = re.sub(r'\[.*?]+', '', final_text)
            # text = text.replace('\n', '')
            # print(final_text)
            db.circuits.update_one({"_id": c["_id"]}, {"$set": {"bio": final_text}})
        except:
            print(c)


if __name__ == '__main__':
    init_drivers()
    driver_bios()
    init_constructors()
    constructor_bios()
    init_circuits()
    circuit_bios()
