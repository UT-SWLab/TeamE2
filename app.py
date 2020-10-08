# 1st party packages
import json

# 3rd party packages
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/drivers')
def drivers():
    driver_id = request.args['id']

    # we need to change this to request from firebase db in the future
    with open('data/drivers.json') as json_file:
        drivers = json.load(json_file)
        for driver in drivers:
            if driver['driverId'] == driver_id:
                data = driver
                break
    print(data)
    name = data['givenName'] + ' ' + data['familyName']
    img_path = f'images/{driver_id}.jpg'
    return render_template('drivers.html', name=name, code=data['code'],\
        dob=data['dateOfBirth'], nation=data['nationality'], img_path=img_path)


@app.route('/constructors')
def constructors():
    constructor_id = request.args['id']

    # we need to change this to request from firebase db in the future
    with open('data/constructors.json') as json_file:
        constructors = json.load(json_file)
        for constructor in constructors:
            if constructor['constructorId'] == constructor_id:
                data = constructor
                break
    print(data)
    return render_template('constructors.html')


@app.route('/circuits')
def circuits():
    circuit_id = request.args['id']

    # we need to change this to request from firebase db in the future
    with open('data/drivers.json') as json_file:
        circuits = json.load(json_file)
        for circuit in circuits:
            if circuit['circuitId'] == circuit_id:
                data = circuit
                break
    print(data)
    return render_template('circuits.html')


if __name__ == '__main__':
    app.run(debug=True)