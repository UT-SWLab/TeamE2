
#!/usr/bin/env python3
"""
collect.py
"""

# First party packages
import argparse
import os
import sys

# Third party packages
import requests

API_DICT = {'ergast': 'http://ergast.com/api/f1'}
ERGAST = 'ergast'


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
    parser.add_argument('-c', '--constructor', dest='constructor', action='store_true', help='Request constructor data')
    parser.add_argument('-i', '--circuit', dest='circuit', action='store_true', help='Request circuit data')
    args = parser.parse_args()

    return args.api, args.driver, args.constructor, args.circuit


def main():
    # Make data directory if it does not exist
    data_path = os.path.dirname(os.path.abspath(__file__)) + '/data'
    os.makedirs(data_path, exist_ok=True)

    # Change working directory to data directory
    os.chdir(data_path)

    api, driver, constructor, circuit = get_inputs()
    collect(api, driver, constructor, circuit)
    
    return None


def collect(api, driver, constructor, circuit):
    if api not in API_DICT.keys():
        print('ERROR: Did not receive valid API to request from. Please select one of the API\'s below')
        for key in API_DICT.keys():
            print(key)
    
    if not (constructor or driver or circuit):
        print('ERROR: Did not receive request input. Please enter -d to request driver data,\
            -c to request constructor data, and -i to request circuit data')
        return None
    if api==ERGAST:
        collect_ergast(driver, constructor, circuit)
    return None


def collect_ergast(driver, constructor, circuit):
    if driver:
        collect_ergast_drivers()
    return None


def collect_ergast_drivers():
    # Collect drivers in the current year for now, will have to expand to 1950-2020 in the future
    endpoint = '/2020/drivers'
    url = API_DICT[ERGAST] + endpoint + '.json'
    response = requests.request('GET', url)
    print(response.json())
    return None


if __name__ == '__main__':
    main()