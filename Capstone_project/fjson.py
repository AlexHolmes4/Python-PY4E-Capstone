import sqlite3

conn = sqlite3.connect('fstructureddata.sqlite')
cur = conn.cursor()

print("Creating JSON output on flights.js...")

cur.execute('''SELECT MAX(population_count) AS Populations, location.city
FROM demography
JOIN location ON demography.location_id = location.id
GROUP BY location_id ORDER BY Populations Desc''')
#Populations  City
#5154164	Seattle, WA
#284093	Eugene, OR
#147300	Medford, OR
#122049	Manhattan, KS
#86219	Ames, IA
#76034	Bend, OR
populations = dict()
for demography_row in cur :
    populations[demography_row[1]] = (demography_row[0])

cur.execute('''SELECT COUNT(location.city) AS Travelled, location.city as City, location.id
FROM location
JOIN flight ON location.id  = flight.location_id_dest OR  location.id = flight.location_id_orig
GROUP BY location.id ORDER BY Travelled DESC, City''')
#Travelled   City
#9	Bend, OR
#5	Medford, OR
#3	Eugene, OR
#1	Ames, IA
#1	Manhattan, KS
#1	Seattle, WA

fhand = open('flights.js', 'w')
nodes = list()

#line thickness
maxtravelrank = None
mintravelrank = None
for row in cur:
    nodes.append(row)
    travel = row[0]
    if maxtravelrank is None or maxtravelrank < travel: maxtravelrank = travel
    if mintravelrank is None or mintravelrank > travel: mintravelrank = travel

if maxtravelrank == mintravelrank or maxtravelrank is None or mintravelrank is None:
    print("Error - please review data, run fgather and fmodel for more data.")
    quit()

fhand.write('flightsJson = {"nodes":[\n')
count = 0
map = dict()
ranks = dict()
for row in nodes :
    if count > 0 : fhand.write(',\n')
    # print row
    rank = row[0]
    rank = 19 * ( (rank - mintravelrank) / (maxtravelrank - mintravelrank) )
    fhand.write('{'+'"weight":'+str(populations[row[1]])+',"rank":'+str(rank)+',')
    fhand.write(' "id":'+str(row[2])+', "city":"'+row[1]+'"}')
    map[row[2]] = count
    ranks[row[2]] = rank
    count = count + 1

fhand.write('],\n')


cur.execute('''SELECT DISTINCT location_id_dest, location_id_orig FROM flight''')
fhand.write('"links":[\n')

count = 0
for row in cur :
    if row[0] not in map or row[1] not in map : continue
    if count > 0 : fhand.write(',\n')
    rank = ranks[row[0]]
    srank = 19 * ( (rank - mintravelrank) / (maxtravelrank - mintravelrank) )
    fhand.write('{"source":'+str(map[row[0]])+',"target":'+str(map[row[1]])+',"value":3}')
    count = count + 1
fhand.write(']};')
fhand.close()
cur.close()

print("Open force.html in a browser to view the visualization")
