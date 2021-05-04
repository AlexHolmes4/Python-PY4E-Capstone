import sqlite3

conn = sqlite3.connect('fstructureddata.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, population_count FROM demography ORDER BY id')
demographies = dict()
for demography_row in cur :
    demographies[demography_row[0]] = demography_row[1]

cur.execute('SELECT id, city FROM location ORDER BY id')
locations = dict()
for location_row in cur :
    locations[location_row[0]] = location_row[1]

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

print("Loaded flights=",len(flights),"locations=",len(locations),"demographies=",len(demographies))

# o = origin d = destination

#histogram of origins and flights, and destinations and flights, and a list of dates
flights_o_locations = dict()
flights_d_locations = dict()
for (flight_id, flight) in list(flights.items()):
    origin = flight[4]
    destination = flight[5]
    flights_o_locations[origin] = flights_o_locations.get(origin, 0) + 1
    flights_d_locations[destination] = flights_d_locations.get(destination, 0) + 1

# pick the top 5 locations travlled from
olocations = sorted(flights_o_locations, key=flights_o_locations.get, reverse=True)
olocations = olocations[:5]
print("Top 5 Locations Travelled From")
print(olocations)

# pick the top 5 locations travelled to
dlocations = sorted(flights_d_locations, key=flights_d_locations.get, reverse=True)
dlocations = dlocations[:5]
print("Top 5 Locations Travelled To")
print(dlocations)


ocounts = dict()
dcounts = dict()
dates = list()
DFORMAT = 4  #adjust to 4 for year only, and 6 for months
for (flight_id, flight) in list(flights.items()):
    origin = flight[4]
    destination = flight[5]
    date = flight[6]
    date = date[:DFORMAT]
    if date not in dates: dates.append(date) #already sorted by how we extracted data from the database ORDER BY demography.date
    okey = (date, origin)
    dkey = (date, destination)
    ocounts[okey] = ocounts.get(okey, 0) + 1
    dcounts[dkey] = dcounts.get(dkey, 0) + 1

#write to JS file for origin locations
foriginhand = open('foriginline.js','w')
foriginhand.write("foriginline = [ ['Month'")
for olocation in olocations:
    foriginhand.write(",'"+olocation+"'")
foriginhand.write("]")

for date in dates:
    foriginhand.write(",\n['"+date+"'")
    for olocation in olocations:
        key = (date, olocation)
        val = ocounts.get(key,0)
        foriginhand.write(","+str(val))
    foriginhand.write("]");

foriginhand.write("\n];\n")
foriginhand.close()

#write to JS file for destination locations
fdestinationhand = open('fdestinationline.js', 'w')
fdestinationhand.write("fdestinationline = [ ['Month'")
for dlocation in dlocations:
    fdestinationhand.write(",'"+dlocation+"'")
fdestinationhand.write("]")

for date in dates:
    fdestinationhand.write(",\n['"+date+"'")
    for dlocation in dlocations:
        key = (date, dlocation)
        val = dcounts.get(key, 0)
        fdestinationhand.write(","+str(val))
    fdestinationhand.write("]");

fdestinationhand.write("\n];\n")
fdestinationhand.close()

print("Output written to foriginline.js, and fdestinationline.js")
print("Open foriginline.htm to visualize the origin location data")
print("Open fdestinationline.htm to visualize the destination location data")
