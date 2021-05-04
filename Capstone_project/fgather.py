import sqlite3
import csv

# connect to DB
conn = sqlite3.connect('rawfdata.sqlite')
cur = conn.cursor()

# set up DB if first time
cur.execute('''CREATE TABLE IF NOT EXISTS flights_raw
    (id INTEGER PRIMARY KEY UNIQUE, origin TEXT, destination TEXT,
    origin_city TEXT, destination_city TEXT, passengers INTEGER, seats INTEGER,
    stops INTEGER, distance INTEGER, fly_date TEXT, origin_population INTEGER,
    destination_population INTEGER )''')

# open the file for read
file_handle = open("flight_edges.tsv", newline="")
file_content  = csv.reader(file_handle, delimiter="\t")

# find last row inserted (if there is one)
start = None
cur.execute('SELECT max(id) FROM flights_raw' )
try:
    row = cur.fetchone()
    if row is None :
        start = 0
    else:
        start = row[0]
        print("Rows inserted previously:",start,"\nProgram will resume where it left off.\n")
except:
    start = 0

if start is None : start = 0

many = 0
resume_count = 0  #used to find a point to resume inserting
insert_count = 0 #counts rows inserted

#loop through the file rows
for row in file_content:
    #if iterations specified by user are completed, prompt input
    if ( many < 1 ) :
        sval = input('Number of flight data rows to import:')
        if ( len(sval) < 1 ) : break
        try:
            many = int(sval)
        except:
            print("enter a number")
            continue

    stripped_row = list()
    for item in row:
        item = item.strip()
        stripped_row.append(item)
    row = stripped_row
#    print("Retrieved data :",row)

    #check to start inserting rows
    count = 0
    if resume_count == start: #number of rows matches max ID
        start = start + 1
        insert_count = insert_count + 1
        many = many - 1
        try:
            cur.execute('''INSERT OR IGNORE INTO flights_raw (id, origin, destination, origin_city,
            destination_city, passengers, seats, stops, distance, fly_date,
            origin_population, destination_population)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (start, row[0], row[1], row[2],
            row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
            conn.commit()
        except KeyboardInterrupt:
            print('')
            print('Program interrupted by user...')
            break
        if insert_count % 10 == 0:
            print("inserted 10 rows")
    resume_count = resume_count + 1 #counts number of rows looped through

if insert_count == 0:
    print(insert_count, "rows inserted. No more rows left to insert")
else:
    print(insert_count,"rows inserted.")

conn.commit()
cur.close()
