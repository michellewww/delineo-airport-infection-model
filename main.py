import gen_infection_model as gim
import config as cfg
import math
import numpy as np
import test_data as td

totalTimeStep = 519
# person - 440 people
# dict {facility id: list of tuples (enter time, leave time)}
# boolean masked
# boolean infected

# facilityInfectedTime = {
#     0: [(10, 30), (40, 60)],  # facility_id: Infected people enter at time 10 and leave at time 30, and enter at time 40 and leave at time 60
#     1: [(20, 50), (70, 90)]   # Infected people enter at time 20 and leave at time 50, and enter at time 70 and leave at time 90
# }

# peopleFacilityTime = {
#     1: {0: [(10, 20), (30, 40)]},  # Example person with their visited facilities and times
#     2: {1: [(20, 30), (40, 50)]}
# }


low_emit_rate = 3.563*10**3
high_emit_rate = 2.354*10**5

N0 = 900 # number of particles inhaled to get infected

def simulate(cur_time, total_virions_inhaled):
    for t in range(cur_time):
        time_facility_conc[t] = {}
        for f in range(19):
            time_facility_conc[t][f] = 0

    for t in range(cur_time):
        print("t: ", t)
        for f in range(19):
            f_conc = gim.facility_concentration(t, f, facilityInfectedTime, cfg.facilityInfo[f][7], low_emit_rate, high_emit_rate)
            time_facility_conc[t][f] = f_conc
            print(f"Facility {f} has a concentration of {f_conc} at time {t}")
            
    for person, visited_facilities in peopleFacilityTime.items():
        total_inhaled = 0
        for facility_id, visited_times in visited_facilities.items():
            for enter_time, leave_time in visited_times:
                for t in range(enter_time, leave_time + 1):  # Include the leave_time
                    f_conc = time_facility_conc[t][facility_id]
                    total_inhaled += fraction_inhaled * f_conc
        print(person)
        print(total_virions_inhaled)
        if person in total_virions_inhaled:
            total_inhaled += total_virions_inhaled[person]

        p_infected = 1 - math.exp(-total_inhaled/N0)
        people_infected_prob[person] = p_infected
        print(f"Person {person} has a {p_infected} chance of being infected")
        if p_infected > 0.7:
            peopleGettingInfected.append(person)
        
        
        

if __name__ == "__main__":
    facilityInfectedTime = td.facilityInfectedTime
    peopleFacilityTime = td.peopleFacilityTime
    fraction_inhaled = gim.fraction_inhaled()
    total_virions_inhaled = gim.short_distance_virions_inhaled()

    peopleGettingInfected = []
    people_infected_prob = {}
    # initialize facility concentration for each time {t: {facility: conc}}
    time_facility_conc = {}
    simulate(totalTimeStep, total_virions_inhaled)
    gim.short_distance_virions_inhaled()