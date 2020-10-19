
#!/usr/bin/env python3
"""
collect.py
"""

# First party packages
import argparse
from datetime import datetime as dt
import json
import os
import sys

# Third party packages
import requests
from ratelimit import limits, sleep_and_retry


def get_inputs():
    """
    Purpose:
        Gets inputs for collect.py
    Args:
        None
    Returns:
    """
    # NOTE -e will add on ages starting from last age in `-a` list
    parser = argparse.ArgumentParser(description='Request information from an F1 API')
    parser.add_argument('-a', '--api', dest='api', required=True, help='API to request from')
    parser.add_argument('-d', '--driver', dest='driver', action='store_true', help='Request driver data')
    parser.add_argument('-t', '--team', dest='team', action='store_true', help='Request team data')
    parser.add_argument('-c', '--circuit', dest='circuit', action='store_true', help='Request circuit data')
    parser.add_argument('-r', '--result', dest='result', action='store_true', help='Request result data')
    args = parser.parse_args()

    return args.api, args.driver, args.team, args.circuit, args.result


def main():
    # Make data directory if it does not exist
    data_path = os.path.dirname(os.path.abspath(__file__)) + '/data'
    os.makedirs(data_path, exist_ok=True)

    # Change working directory to data directory
    os.chdir(data_path)

    api, driver, team, circuit, result = get_inputs()
    collect(api, driver, team, circuit, result)
    
    return None

API_DICT = {'ergast': 'http://ergast.com/api/f1'}
ERGAST = 'ergast'

def collect(api, driver, team, circuit, result):
    if api not in API_DICT.keys():
        print('ERROR: Did not receive valid API to request from. Please select one of the API\'s below')
        for key in API_DICT.keys():
            print(key)
    
    if not (team or driver or circuit or result):
        print('ERROR: Did not receive request input. Please enter -d to request driver data,\
            -c to request team data, and -i to request circuit data')
        return None
    if api==ERGAST:
        collect_ergast(driver, team, circuit, result)
    return None


DRIVERS = 'drivers'
TEAMS = 'constructors'
CIRCUITS = 'circuits'
RESULTS = 'results'

def collect_ergast(driver, team, circuit, result):
    if driver:
        get_ergast_data(DRIVERS)
    elif team:
        get_ergast_data(TEAMS)
    elif circuit:
        get_ergast_data(CIRCUITS)
    elif result:
        get_ergast_data(RESULTS)

    return None


JSON = '.json'

def get_ergast_data(request_type):
    year_str = str(dt.now())
    end_year = int(year_str[:year_str.index('-')]) + 1
    years = range(1950, end_year)
    years_dict = {}
    for year in years:
        # Collect drivers in the current year for now, will have to expand to 1950-2020 in the future
        url = f'{API_DICT[ERGAST]}/{year}/{request_type}{JSON}'
        response = call_api(url)
    
        if request_type == DRIVERS:
            table_id = 'DriverTable'
            data_id = 'Drivers'
        elif request_type == TEAMS:
            table_id = 'ConstructorTable'
            data_id = 'Constructors'
        elif request_type == CIRCUITS:
            table_id = 'CircuitTable'
            data_id = 'Circuits'
        elif request_type == RESULTS:
            table_id = 'RaceTable'
            data_id = 'Races'
        data = response.json()['MRData'][table_id][data_id]
        years_dict[year] = data

    with open(f'{request_type}.json', 'w') as outfile:
        json.dump(years_dict, outfile)
    return None


FIFTEEN_MINUTES = 900

@sleep_and_retry
@limits(calls=15, period=FIFTEEN_MINUTES)
def call_api(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception('API response: {}'.format(response.status_code))
    return response


if __name__ == '__main__':
    main()