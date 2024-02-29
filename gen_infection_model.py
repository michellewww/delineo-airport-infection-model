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

lifetime = 1.628 #hours
deg_rate = 1/(lifetime*60) # 1/min

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