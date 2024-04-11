# pygame visualization
backgroundColor = (230, 230, 230)
textColor = (0, 0, 0)
textSize = 25
personRadius = 5
facilityBoxSize = 38


# departure
rate_self_checked = 0.1
check_time = 2 # min
security_time = 4 # min
maxBefore = 200 # if the plane departures at t, earliest person will come to airport at t-200
minBefore = 100 # if the plane departures at t, latest person will come to airport at t-100
boardingTime = 30 # min before departure time
boardingDecisionTime = 40


# arrival
num_people_off_plane = 15  # per min


# flight info
# flightId : [Arrival("A"), Gate, Time, numPassenger, ExitId, connectedInfo(connectedFlightId: numConnected)]
# flightId : Departure("D"), Gate, Time, total number of passengers, number of passengers not from connects]
flightInfo = {
    1: ["A", 0, 0, 150, 12, {3: 50}],
    2: ["A", 1, 30, 200, 12, {3: 10}],
    3: ["D", 1, 230, 150, 90]
}

# airport map info
mapWidth = 600
mapLength = 800
# id: [name, type, X, Y, maxOccupancy, medium, variance, volume]
# facilityInfo = {
#     0:  ['gate1',          'Gate',      30,  350, 500,   60,  16, 200000],
#     1:  ['gate2',          'Gate',      280, 550, 500,   60,  16, 200000],
#     2:  ['restroom1',      'Restroom',  130, 350, 20,    3,  1, 30000],
#     3:  ['restaurant1',    'Food',      280, 350, 50,    15, 4, 60000],
#     4:  ['store1',         'Shopping',  380, 350, 10,    3,  1, 50000],
#     5:  ['restaurant2',    'Food',      450, 350, 20,    10, 4, 60000],
#     6:  ['restroom2',      'Restroom',  550, 350, 10,    2,  1, 30000],
#     7:  ['restroom3',      'Restroom',  280, 480, 15,    2,  1, 30000],
#     8:  ['store2',         'Shopping',  380, 220, 15,    5,  1, 50000],
#     9:  ['restaurant3',    'Food',      450, 280, 40,    10, 4, 60000],
#     10: ['baggage claim1', 'BC',        670, 290, 300,   20, 4, 300000],
#     11: ['baggage claim2', 'BC',        670, 390, 300,   19, 4, 300000],
#     12: ['exit',           'Exit',      750, 350, 10000, 0,  0, 500000],
#     13: ['counter1',       'Counter',   190, 50,  None,   None,  None, 10000],
#     14: ['counter2',       'Counter',   270, 50,  None,   None,  None, 10000],
#     15: ['counter3',       'Counter',   350, 50,  None,   None,  None, 10000],
#     16: ['security1',      'Security',  190, 150, None,   None,  None, 10000],
#     17: ['security2',      'Security',  270, 150, None,   None,  None, 10000],
#     18: ['security3',      'Security',  350, 150, None,   None,  None, 10000]
# }
facilityInfo = {
  0: ["checkin_counter", "type_placeholder", -10.1, -27.07, "maxOccupancy_placeholder","medium", "variance", 10000],
  1: ["egg_shell_cafe", "type_placeholder", 44.145, -19.47, "maxOccupancy_placeholder", "medium", "variance", 5000],
  2: ["security", "type_placeholder", 21.745, -34.22, "maxOccupancy_placeholder", "medium", "variance", 10000],
  3: ["restroom1", "type_placeholder", 22.59, -44.17, "maxOccupancy_placeholder", "medium", "variance", 3000],
  4: ["gate_1", "type_placeholder", 6.195, -58.42, "maxOccupancy_placeholder", "medium", "variance", 200000],
  5: ["gate_2", "type_placeholder", 29.59, -59.62, "maxOccupancy_placeholder", "medium", "variance", 200000],
  6: ["book_store", "type_placeholder", -7.9, -56.37, "maxOccupancy_placeholder", "medium", "variance", 5000],
  7: ["cafe_under_stair", "type_placeholder", -4.5511, -45.12, "maxOccupancy_placeholder", "medium", "variance", 5000],
  8: ["restroom2", "type_placeholder", 22.34, -44.27, "maxOccupancy_placeholder", "medium", "variance", 10000],
  9: ["gate_3", "type_placeholder", -33.55, -61.52, "maxOccupancy_placeholder", "medium", "variance", 200000],
  10: ["gate_4", "type_placeholder", -3.055, -59.77, "maxOccupancy_placeholder", "medium", "variance", 200000],
  11: ["gate_5", "type_placeholder", 30.34, -60.57, "maxOccupancy_placeholder", "medium", "variance", 200000],
  12: ["cafe", "type_placeholder", -37.95, -48.42, "maxOccupancy_placeholder", "medium", "variance", 5000]
}




# weight of different factors when calculating the next facility
weight_1 = 0.1 # distance between current and next facility
weight_2 = 0.7 # distance between next facility and destination
weight_3 = 0.1 # facility type
weight_4 = 0.1 # occupancy of current and next facility


# person speed
minWalkingSpeed = 30
maxWalkingSpeed = 40



