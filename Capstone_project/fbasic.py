import sqlite3

conn = sqlite3.connect('fstructureddata.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, population_count FROM demography ORDER BY id')
demographies = dict()
for demography_row in cur :
    demographies[demography_row[0]] = demography_row[1]
#print(demographies
cur.execute('SELECT id, city FROM location ORDER BY id')
locations = dict()
for location_row in cur :
    locations[location_row[0]] = location_row[1]

# cur.execute('SELECT id, guid,sender_id,subject_id,headers,body FROM Messages')
cur.execute('''
SELECT flight.id, passengers, seats, stops, distance, origin.city, destination.city, demography.date
FROM `flight`
INNER JOIN `location` as origin ON flight.location_id_orig=origin.id
INNER JOIN `location` as destination ON flight.location_id_dest=destination.id
INNER JOIN `demography` ON flight.demography_id=demography.id
ORDER BY demography.date''')
flights = dict()
for flight_row in cur :
    flights[flight_row[0]] = (flight_row[1],flight_row[2],flight_row[3],flight_row[4],flight_row[5],flight_row[6],flight_row[7])

# variables
passengerscount, emptyseatscount, dates, flightsfromloc, flightstoloc, origincounts, destinationcounts= dict(), dict(), list(), dict(), dict(), dict(), dict()
# flag values
total_seats_empty = 0
# Constants
DFORMAT = 6  #adjust to 4 for year only, and 6 for months

                                                              #flight id[0] is 1 next iteration 2, etc. Wheras flight id[1] is the tuple (0,0,1,156 etc.)
#loop through data and create analysis points                 #by specifying a second iteration variable we access the second value i.e. the tuple
for (flight_id, flight) in list(flights.items()):             #list snippit [(1, (0, 0, 1, 156, 1, 2, 1)), (2, (124, 124, 1, 858, 3, 4, 2))
    passengers, seats, stops, distance, origin_city, destination_city, date = flight[0], flight[1], flight[2], flight[3], flight[4], flight[5], flight[6]
    #histogram of passenger counts
    passengerscount[passengers] = passengerscount.get(passengers,0) + 1
    #histogram of empty seats and total number of empty seat
    emptyseats = seats - passengers
    empty_seats_key = (date, emptyseats)
    emptyseatscount[empty_seats_key] = emptyseatscount.get(empty_seats_key, 0) + 1
    total_seats_empty = total_seats_empty + emptyseats

    if date not in dates: dates.append(date[:DFORMAT]) #already sorted by how we extracted data from the database ORDER BY demography.date

    flightsfromloc[origin_city] = flightsfromloc.get(origin_city, 0) + 1
    flightstoloc[destination_city] = flightstoloc.get(destination_city, 0) + 1

    origin_key = (date, origin_city)
    origincounts[origin_key] = origincounts.get(origin_key,0) + 1

    destination_key = (date, destination_city)
    destinationcounts[destination_key] = destinationcounts.get(destination_key, 0) + 1

#find date range of dataset
date_range_max, date_range_min = max(dates), min(dates)
sdate_range_max, sdate_range_min = str(date_range_max), str(date_range_min)
#find average empty seats for dataset

if total_seats_empty > 1:
    avg_empty_seats = (total_seats_empty) / (max(flights.keys()))
else:
    avg_empty_seats = "None empty"

if DFORMAT == 6:
    print("Loaded flights=",len(flights),"locations=",len(locations),
    "demographies=",len(demographies),"average-empty-seats=",(round(avg_empty_seats,2)), "from dates:",
    (sdate_range_min[:4]+"-"+sdate_range_min[4:]),"->",(sdate_range_max[:4]+"-"+sdate_range_max[4:]))
else:
    print("Loaded flights=",len(flights),"locations=",len(locations),
    "demographies=",len(demographies),"average-empty-seats=",(round(avg_empty_seats,2)), "from dates:",
    (sdate_range_min+" -> "+sdate_range_max))


print('')
print('Top Fly to Locations')
x = sorted(flightstoloc.items(), key=lambda item: item[1], reverse=True)
for key, value in x:
    print(value,"flights to", key)

print('')
print('Top Fly From Locations')
x = sorted(flightsfromloc.items(), key=lambda item: item[1], reverse=True)
for key, value in x:
    print(value,"flights from", key)

cur.close()
