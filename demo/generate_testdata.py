import random
# 30 people
# 19 facilities
# time: 0 to 60

# Generate facilityInfectedTime
facilityInfectedTime = {}
for facility_id in range(19):
    infected_times = []
    for _ in range(random.randint(1, 5)):  # Random number of infected periods per facility
        enter_time = random.randint(0, 40)
        leave_time = enter_time + random.randint(10, 20)
        infected_times.append((enter_time, leave_time))
    facilityInfectedTime[facility_id] = infected_times

# Generate peopleFacilityTime
peopleFacilityTime = {}
for person_id in range(1, 31):  # 30 people
    peopleFacilityTime[person_id] = {}
    for _ in range(random.randint(1, 3)):  # Random number of visited facilities per person
        facility_id = random.randint(0, 18)
        visited_times = []
        for _ in range(random.randint(1, 3)):  # Random number of visits per facility
            enter_time = random.randint(0, 40)
            leave_time = enter_time + random.randint(5, 20)
            visited_times.append((enter_time, leave_time))
        peopleFacilityTime[person_id][facility_id] = visited_times

# Write data to file
with open("test_data.py", "w") as f:
    f.write("facilityInfectedTime = {\n")
    for facility_id, infected_times in facilityInfectedTime.items():
        f.write(f"    {facility_id}: {infected_times},\n")
    f.write("}\n\n")

    f.write("peopleFacilityTime = {\n")
    for person_id, visited_facilities in peopleFacilityTime.items():
        f.write(f"    {person_id}: {visited_facilities},\n")
    f.write("}\n")
