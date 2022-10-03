from glob import glob
import json
import math
from flask import Flask,request

cap_for_buildings = 0.3
cap_for_others = 0.9 - cap_for_buildings
fleetValue = 0
allowanceResources = {'Metal': 0, 'Crystal': 0, 'Deuterium': 0}
allowanceShips = {'Metal': 0, 'Crystal': 0, 'Deuterium': 0}

port = 5000
app = Flask(__name__)

def countDeuteriumHardCap():
    global fleetValue
    return fleetValue * 0.03

def getAllowanceWithNoShipyard(availableResources):
    global allowanceResources
    global allowanceShips
    
    allowanceResources['Metal'] = math.ceil(availableResources['Metal'])
    allowanceResources['Crystal'] = math.ceil(availableResources['Crystal'])
    allowanceResources['Deuterium'] = math.ceil(availableResources['Deuterium'])
    allowanceShips = {'Metal': 0, 'Crystal': 0, 'Deuterium': 0}

def getDefaultAllowance(resources):
    global allowanceResources
    
    allowanceResources['Metal'] = math.ceil(resources['Metal'] * cap_for_buildings)
    allowanceResources['Crystal'] = math.ceil(resources['Crystal'] * cap_for_buildings)
    allowanceResources['Deuterium'] = math.ceil(resources['Deuterium'] * cap_for_buildings)

def getDefaultShipAllowance(resources):
    global allowanceShips
    
    allowanceShips['Metal'] = math.ceil(resources['Metal'] * cap_for_others)
    allowanceShips['Crystal'] = math.ceil(resources['Crystal'] * cap_for_others)
    allowanceShips['Deuterium'] = math.ceil(resources['Deuterium'] * cap_for_others - countDeuteriumHardCap())

@app.route('/get_allowances', methods=['GET'])
def getAllowances():
    global fleetValue
    global allowanceResources
    global allowanceShips

    request_data = request.get_json()

    resources = request_data['resources']
    facilities = request_data['facilities']
    fleetValue = request_data['fleetValue']

    getDefaultShipAllowance(resources)

    if(facilities['Shipyard'] < 2):
        getAllowanceWithNoShipyard(resources)
    else:
        getDefaultAllowance(resources)

    allowanceResourcesWithHeader =  {'allowanceResources': allowanceResources}
    allowanceShipsWithHeaders =  {'allowanceShips': allowanceShips}

    returnAllowances = {**allowanceResourcesWithHeader, **allowanceShipsWithHeaders}
    print(returnAllowances)
    return returnAllowances

@app.route('/ready', methods=['GET'])
def getReadiness():
    return "{Status: OK}"
    
app.run(host='0.0.0.0', port=port)