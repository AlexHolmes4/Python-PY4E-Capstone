import sqlite3

conn = sqlite3.connect('fstructureddata.sqlite')
cur = conn.cursor()

# connection to raw data database established for data extraction
conn_raw = sqlite3.connect('file:rawfdata.sqlite?mode=ro', uri=True)
cur_raw = conn_raw.cursor()

# The flight data model program will start a fresh each time.
#cur.execute('''DROP TABLE IF EXISTS location ''')
#cur.execute('''DROP TABLE IF EXISTS demography ''')
#cur.execute('''DROP TABLE IF EXISTS flight ''')

cur.execute('''CREATE TABLE IF NOT EXISTS location
        (id INTEGER PRIMARY KEY UNIQUE, airport_name TEXT UNIQUE,
         city TEXT UNIQUE)''')
cur.execute('''CREATE TABLE IF NOT EXISTS demography
        (id INTEGER PRIMARY KEY UNIQUE, population_count INTEGER,
        date TEXT, location_id INTEGER)''')
cur.execute('''CREATE TABLE IF NOT EXISTS flight
        (id INTEGER PRIMARY KEY UNIQUE, passengers INTEGER, seats INTEGER,
        stops INTEGER, distance INTEGER, location_id_orig INTEGER,
        location_id_dest INTEGER, demography_id INTEGER)''')

#find last modelled row
resume_count = None
cur.execute('SELECT max(id) FROM flight')
try:
    row = cur.fetchone()
    if row is None:
        resume_count = 0
    else:
        resume_count = row[0]
        print("Rows modelled previously:",resume_count,"\nProgram will resume where it left off.\n")
except:
    resume_count = 0

if resume_count is None: resume_count = 0

#loop through the file rows
many = 0
insert_count = 0
while True:
    resume_count = resume_count + 1
    conn.commit()
    #if iterations specified by user are completed, prompt input
    if ( many < 1 ) :
        sval = input('Number of database rows to model:')
        if ( len(sval) < 1 ) : break
        try:
            many = int(sval)
        except:
            print("enter a number")
            continue

    # fetch row of raw flight data
    cur_raw.execute('''SELECT origin, destination, origin_city, destination_city, passengers, seats, stops, distance, fly_date,
    origin_population, destination_population FROM flights_raw WHERE id = ?''', (resume_count, ))
    try:
        row = cur_raw.fetchone()
    except KeyboardInterrupt:
        print('')
        print("Program interrupted by user...")
        cur.close()
    except:
        print("Modelling complete.")
        cur.close()
        break
    if row is None:
        print("Modelling complete.")
        cur.close()
        break
#                print("raw data retrieved for cleaning and modelling:\n",row,'\n')

    # location table
    # insert origin to location table
    cur.execute('''INSERT OR IGNORE INTO location (airport_name, city)
        SELECT * FROM (SELECT ?, ?) AS `values`
        WHERE NOT EXISTS (SELECT ?, ? FROM location WHERE airport_name=? AND city=?)
        LIMIT 1''', (row[0], row[2], row[0], row[2], row[0], row[2]))
    conn.commit()

    # retrieve the id for the origin location
    cur.execute('SELECT id FROM location WHERE airport_name = ?', (row[0], ))
    try: origin_id = cur.fetchone()[0]
    except: pass #that location not yet inserted, next line will add dest city to ref table - locations

    # insert destination to location table
    cur.execute('''INSERT OR IGNORE INTO location (airport_name, city)
        SELECT * FROM (SELECT ?, ?) AS `values`
        WHERE NOT EXISTS (SELECT ?, ? FROM location WHERE airport_name=? AND city=?)
        LIMIT 1''', (row[1], row[3], row[1], row[3], row[1], row[3]))
    conn.commit()
    # retrieve the id for the destination location
    cur.execute('SELECT id FROM location WHERE airport_name = ?', (row[1], ))
    destination_id = cur.fetchone()[0]

    # demography table
    #insert origin to demography table
    cur.execute('''INSERT INTO demography (population_count, date,
    location_id) VALUES (?, ?, ?)''', (row[9], row[8], origin_id))
    conn.commit()
    #insert destination to demography table
    cur.execute('''INSERT INTO demography (population_count, date,
    location_id) VALUES (?, ?, ?)''', (row[10], row[8], destination_id))
    conn.commit()

    #retrieve the id for the demography insert
    #only 1 id for the the two (origin, destination) inserts needed as shared date
    cur.execute('SELECT id FROM demography WHERE id = ?', (resume_count*2, ))
    demography_id = cur.fetchone()[0]

    # flight Table
    cur.execute('''INSERT INTO flight (passengers, seats, stops, distance,
    location_id_orig, location_id_dest, demography_id)
    VALUES (?, ?, ?, ?, ?, ?, ?)''', (row[4],row[5],row[6],row[7], origin_id,
    destination_id, demography_id))
    conn.commit()

    many = many - 1

    #print("id's retrieved:\n","origin_id:",origin_id, " destination_id:",destination_id, " demography_id:",demography_id)
    insert_count = insert_count + 1
    if insert_count % 20 == 0: print("20 more rows inserted")
    if insert_count % 100 == 0: print("100 more rows inserted")
    if insert_count % 1000 == 0: print("1000 more rows inserted")

if insert_count == 0:
    print(insert_count, "rows modelled. No more rows left to model")
else:
    print(insert_count, "rows modelled.")

cur.close()
cur_raw.close()
