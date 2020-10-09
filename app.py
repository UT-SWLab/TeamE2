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

@app.route('/models_drivers')
def driver_model():
    with open('./data/drivers.json') as f:
        drivers = json.load(f)
    return render_template('drivers-model.html', drivers=drivers)

@app.route('/models_constructors')
def constructor_model():
    with open('./data/constructors.json') as f:
        constructors = json.load(f)
    return render_template('constructors-model.html', constructors=constructors)

@app.route('/models_circuits')
def circuit_model():
    with open('./data/circuits.json') as f:
        circuits = json.load(f)
    return render_template('circuits-model.html', circuits=circuits)

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
    return render_template('drivers-instance.html', name=name, code=data['code'],\
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
    return render_template('constructors-instance.html')


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
    return render_template('circuits-instance.html')


if __name__ == '__main__':
    app.run(debug=True)