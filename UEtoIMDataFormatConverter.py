import json
import os
import re
import random

class Person:
    def __init__(self, id, enteredTime):
        self.id = id
        self.enteredTime = enteredTime
        self.movementTrack = []
        probability = random.random()
        if probability <= 0.005:
            self.infected = 1
        else:
            self.infected = 0

def get_json_file_names(directory):
    return sorted([f for f in os.listdir(directory) if f.endswith('.json')], key=lambda x: int(x.split('.')[0]))

def parse_json_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file {file_name}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error with file {file_name}: {e}")
        return None

def extractID(id_string):
    match = re.search(r'\d+$', id_string)
    return int(match.group())

def getFacility(X, Y, Z):
    for facility in facility_info["floor_1"]:
        if Z <= 200 and facility["minX"] <= X <= facility["maxX"] and facility["minY"] <= Y <= facility["maxY"]:
            return facility["ID"]
    for facility in facility_info["floor_2"]:
        if Z > 200 and facility["minX"] <= X <= facility["maxX"] and facility["minY"] <= Y <= facility["maxY"]:
            return facility["ID"]
    return -1



facility_info = parse_json_file('UEAirportFacilityList.json')
json_files = get_json_file_names('UERealtimeMovementData')

peopleList = {}

# iterate through every timestep
# for file_index in range(len(json_files)):
for file_index in range(600):
    current_data = parse_json_file(os.path.join('UERealtimeMovementData', json_files[file_index]))

    # interate through every passenger
    for passenger in current_data["Passenger"]:
        if passenger != {}:
            id = extractID(passenger["ID"])
            # create new person if just enter the system
            if id not in peopleList:
                peopleList[id] = Person(id, file_index)
            # append current location
            peopleList[id].movementTrack.append(getFacility(passenger['X'], passenger['Y'], passenger['Z']))
 


facilityInfectedTime = {}
peopleFacilityTime = {}


for id, person in peopleList.items():
    # not infected
    if person.infected == 0:
        peopleFacilityTime.setdefault(person.id, {})

        currentFacility = None
        enterTime = None
        for i, facility_id in enumerate(person.movementTrack):
            if facility_id == -1:
                if currentFacility is not None:
                    peopleFacilityTime[person.id].setdefault(currentFacility, []).append(
                        (enterTime, i + person.enteredTime))
                    currentFacility = None
            else:
                if currentFacility is None:
                    currentFacility = facility_id
                    enterTime = i + person.enteredTime
        if currentFacility is not None:
            peopleFacilityTime[person.id].setdefault(currentFacility, []).append(
                (enterTime, len(person.movementTrack) + person.enteredTime))
    
    else:
        currentFacility = None
        enterTime = None
        for i, facility_id in enumerate(person.movementTrack):
            if facility_id == -1:
                if currentFacility is not None:
                    facilityInfectedTime.setdefault(currentFacility, []).append((enterTime, i + person.enteredTime))
                    currentFacility = None
            else:
                if currentFacility is None:
                    currentFacility = facility_id
                    enterTime = i + person.enteredTime
        if currentFacility is not None:
            facilityInfectedTime.setdefault(currentFacility, []).append(
                (enterTime, len(person.movementTrack) + person.enteredTime))

infectedPeopleList = []
for id, person in peopleList.items():
    if person.infected:
        infectedPeopleList.append(id)


with open("UEtoIM_formatted_data1.py", "w") as f:
    f.write(f"infectedPeopleList = {infectedPeopleList}\n\n")

    f.write("facilityInfectedTime = {\n")
    for facility_id, infected_times in facilityInfectedTime.items():
        f.write(f"    {facility_id}: {infected_times},\n")
    f.write("}\n\n")

    f.write("peopleFacilityTime = {\n")
    for person_id, visited_facilities in peopleFacilityTime.items():
        f.write(f"    {person_id}: {visited_facilities},\n")
    f.write("}\n")