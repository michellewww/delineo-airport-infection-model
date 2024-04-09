# person 
# dict {facility id: list of tuples (enter time, leave time)}
# boolean masked
# boolean infected

# infected_people_info = {
#     'facility_A': [(10, 30), (40, 60)],  # Infected people enter at time 10 and leave at time 30, and enter at time 40 and leave at time 60
#     'facility_B': [(20, 50), (70, 90)]   # Infected people enter at time 20 and leave at time 50, and enter at time 70 and leave at time 90
# }


# facility
# virus concentration

import config as cfg
import pandas as pd
import numpy as np
import math
import os
import json
import re
from scipy.interpolate import interp1d

lifetime = 1.628 #hours
deg_rate = 1/(lifetime*60) # 1/min
distance_to_virions = {
    0.25: 96.57,
    0.5: 68.37,
    0.75: 32.68,
    1: 20.53,
    1.25: 16.47,
    1.5: 13.39,
    1.75: 11.18,
    2: 10.82,
}
folder_path = 'UERealTimeMovementData'
infected_people = [0, 1, 11, 22, 33, 55]
distances = list(distance_to_virions.keys())
virions = list(distance_to_virions.values())
interp_func = interp1d(distances, virions, kind='linear', fill_value="extrapolate")

def calculate_distance(x1, y1, z1, x2, y2, z2):
    if z1 <= 200 and z2 <= 200:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 1000
    elif z1 > 200 and z2 > 200:
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 1000
    else:
        return math.inf

def short_distance_virions_inhaled():
    total_virions_inhaled = {}

    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith('.json'):
            with open(os.path.join(folder_path, filename), 'r') as file:
                data = json.load(file)
                passengers = data['Passenger']
                # delete first {} in passengers
                passengers.pop(0)

                # Create a map of positions for quick access
                positions = {int(re.search(r'\d+', p['ID']).group()): (p['X'], p['Y'], p['Z']) for p in passengers}

                # Calculate virions inhaled for each non-infected person
                for passenger_id, pos in positions.items():
                    if passenger_id not in infected_people:
                        total_virions = 0
                        
                        # Calculate distance from each infected person and sum virions inhaled
                        for infected_id in infected_people:
                            if infected_id in positions:
                                infected_pos = positions[infected_id]
                                distance = calculate_distance(*pos, *infected_pos)
                                virions_inhaled = interp_func(min(distance, max(distances)))/60  # Use interpolated value
                                total_virions += virions_inhaled
                        
                        # Update total virions inhaled for the passenger
                        if passenger_id in total_virions_inhaled:
                            total_virions_inhaled[passenger_id] += total_virions
                        else:
                            total_virions_inhaled[passenger_id] = total_virions

    print(total_virions_inhaled)
    # for passenger_id, virions in total_virions_inhaled.items():
    #     print(f"{passenger_id}: {virions} virions inhaled")
    return total_virions_inhaled


def filt_removal(vol, filt_rate):
    # vol: volume of facility (m^3)
    # filt_rate: rate (vol/time) at which air goes through filter
    # Returns: rate of particle removal (1/time)
    return filt_rate / vol

def facility_concentration(t, facility_id, facilityInfectedTime, vol, low_emit_rate, high_emit_rate, k_deg=deg_rate, filt_rate=0, mask_eff=0):
    # t: time elapsed (minutes)
    # infected_info: list of tuples (emit_rate, enter_time, leave_time) where emit_rate is emission rate (particles/time),
    #              enter_time is the time when the person enters the facility (minutes), and
    #              leave_time is the time when the person leaves the facility (minutes)
    # k_deg: rate of particle degradation (1/time) - average lifetime is 1/k_deg
    # vol: facility volume
    # filt_eff: fraction of particles removed by filter (from 0 to 1; 1 if all particles that cycle through filter are removed)
    # filt_rate: rate (vol/time) at which air goes through filter
    # mask_eff: fraction of particles removed by mask on emitter (from 0 to 1; 1 if all particles stopped by mask)
    # Returns: particles/vol in facility
    total_conc = 0
    k_remove = k_deg + filt_removal(vol, filt_rate)
    # print(f'k_remove: {k_remove}')

    mean_emit_rate = (low_emit_rate + high_emit_rate) / 2
    std_dev = (high_emit_rate - low_emit_rate) / 6

    emit_rate = np.random.normal(mean_emit_rate, std_dev)
    emit_rate  = max(min(emit_rate, high_emit_rate), low_emit_rate)
    
    if facility_id in facilityInfectedTime:
        for enter_time, leave_time in facilityInfectedTime[facility_id]:
            emit_rate = (1 - mask_eff) * emit_rate
            if t >= enter_time and t <= leave_time:
                emit_time = min(t, leave_time) - min(t, enter_time) # time the person is in the facility
                # print(f't: {t}, enter_time: {enter_time}, leave_time: {leave_time}')
                # print(f'emit_time: {emit_time}')
                if k_remove > 0:
                    conc_nom = (1 - np.exp(-k_remove * emit_time)) * emit_rate
                    conc_denom = vol * k_remove
                    conc = conc_nom / conc_denom
                    
                    # if conc_nom < 0:
                    #     #send error message
                    #     print("i")
                    #     print(f'error: conc_nom is negative')
                    #     print(f'nom: {(1 - np.exp(-k_remove * emit_time)) * emit_rate}')
                    #     print(f'one: {1 - np.exp(-k_remove * emit_time)}')
                    #     print(f'emit_rate: {emit_rate}')
                else:
                    conc = emit_rate * emit_time / vol

                total_conc += conc
                # print(f'inner f {facility_id} has a concentration of {conc} at time {t}')
            
    return total_conc




def fraction_inhaled():
    size_df = pd.read_csv("./droplet_sizes.csv")[["expelled_size", "inhaled_size", "transmission_prob", "percent_expelled"]]
    size_df["deposition_prob"] = size_df["transmission_prob"]

    size_df["expelled_pdf"] = size_df["percent_expelled"]/100

    # steady-state fraction of virions in each droplet size class
    size_df["expelled_vol"] = np.power(size_df["expelled_size"]/2, 3) * (4/3)
    size_df["frac_viruses"] = size_df["expelled_pdf"] * size_df["expelled_vol"]
    # renormalized to account for larger particles not included in original pdf
    size_df["frac_viruses"] = np.sum(size_df["expelled_pdf"])*size_df["frac_viruses"]/np.sum(size_df["frac_viruses"])
    size_df["frac_viruses"] = size_df["frac_viruses"]/np.sum(size_df["frac_viruses"])

    # to marginalize out droplet size: probability that a virus in each droplet size class
    # will be inhaled multiplied by probability that virus is in that droplet size class
    size_df["trans_dist"] = size_df["frac_viruses"] * size_df["deposition_prob"]/100
    frac_vir_trans = np.sum(size_df["trans_dist"])

    return frac_vir_trans