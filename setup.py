import mysql.connector
import pandas as pd
import numpy as np
import sqlalchemy

conn = mysql.connector.connect(
    user = 'root',
    password = 'root',
    host = 'localhost',
    database = 'f1'
)

print("Connection established:", conn)

cur = conn.cursor()

createCircuits = """
    CREATE TABLE IF NOT EXISTS circuits (
    circuitID INT PRIMARY KEY NOT NULL,
    name VARCHAR(60) NOT NULL,
    location VARCHAR(30),
    country VARCHAR(20),
    lat DECIMAL(10, 6),
    lng DECIMAL(10, 6)
    );"""

createRaces = """
    CREATE TABLE IF NOT EXISTS races (
    raceID INT PRIMARY KEY NOT NULL,
    circuitID INT,
    name VARCHAR(60) NOT NULL,
    year INT NOT NULL,
    date DATE,
    time TIME,
    round INT,
    FOREIGN KEY (circuitID) REFERENCES circuits(circuitID)
    );"""

createConstructor = """
    CREATE TABLE IF NOT EXISTS constructors (
    constructorID INT PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    nationality VARCHAR(20) NOT NULL
    );"""

createDrivers = """
    CREATE TABLE IF NOT EXISTS drivers (
    driverID INT PRIMARY KEY,
    forename VARCHAR(25),
    surname VARCHAR(30),
    number INT NOT NULL,
    code CHAR(3),
    nationality VARCHAR(20) NOT NULL,
    dob DATE
    );"""

createStatus = """
    CREATE TABLE IF NOT EXISTS status (
    statusID INT PRIMARY KEY,
    description VARCHAR(20) NOT NULL
    );"""

createResults = """
    CREATE TABLE IF NOT EXISTS results (
    resultID INT PRIMARY KEY,
    driverID INT,
    raceID INT,
    constructorID INT,
    points INT,
    position INT,
    fastestLapTime TIME,
    statusID INT,
    FOREIGN KEY (driverID) REFERENCES drivers(driverID),
    FOREIGN KEY (raceID) REFERENCES races(raceID),
    FOREIGN KEY (statusID) REFERENCES status(statusID)
    );"""

createDriverStandings = """
    CREATE TABLE IF NOT EXISTS driverStandings (
    driverID INT,
    raceID INT,
    wins INT,
    points INT,
    position INT,
    PRIMARY KEY (driverID, raceID),
    FOREIGN KEY (driverID) REFERENCES drivers(driverID),
    FOREIGN KEY (raceID) REFERENCES races(raceID)
    );"""

createLapTimes = """
    CREATE TABLE IF NOT EXISTS lapTimes (
    driverID INT,
    raceID INT,
    lap INT,
    position INT,
    time TIME,
    PRIMARY KEY (driverID, raceID, lap),
    FOREIGN KEY (driverID) REFERENCES drivers(driverID),
    FOREIGN KEY (raceID) REFERENCES races(raceID)
    );"""

createPitStops = """
    CREATE TABLE IF NOT EXISTS pitStops (
    driverID INT,
    raceID INT,
    stop INT,
    lap INT,
    time TIME,
    duration TIME(3),
    PRIMARY KEY (driverID, raceID, stop),
    FOREIGN KEY (driverID) REFERENCES drivers(driverID),
    FOREIGN KEY (raceID) REFERENCES races(raceID)
    );"""

createConstStand = """
    CREATE TABLE IF NOT EXISTS constructorStandings (
    raceID INT,
    constructorID INT,
    wins INT,
    points INT,
    position INT,
    PRIMARY KEY (raceID, constructorID),
    FOREIGN KEY (raceID) REFERENCES races(raceID),
    FOREIGN KEY (constructorID) REFERENCES constructors(constructorID)
    );"""

cur.execute(createCircuits)
cur.execute(createRaces)
cur.execute(createConstructor)
cur.execute(createDrivers)
cur.execute(createStatus)
cur.execute(createResults)
cur.execute(createDriverStandings)
cur.execute(createLapTimes)
cur.execute(createPitStops)
cur.execute(createConstStand)

# Making DataFrames for all tables to import data from csv files :)

circuits = pd.read_csv("data/circuits.csv")
circuits.drop(['circuitRef', 'alt', 'url'], axis = 1, inplace=True)

races = pd.read_csv("data/races.csv")
races.drop(['url','fp1_date','fp1_time','fp2_date','fp2_time','fp3_date','fp3_time','quali_date','quali_time','sprint_date','sprint_time'], axis=1, inplace=True)
races['time'].replace('\\N', '', inplace=True)

constructors = pd.read_csv("data/constructors.csv")
constructors.drop(['constructorRef', 'url'], axis=1, inplace=True)

drivers = pd.read_csv("data/drivers.csv")
drivers['number'].replace('\\N', 0, inplace=True)
drivers['code'].replace('\\N', 'XYZ', inplace=True)
drivers.drop(['driverRef', 'url'], axis=1, inplace=True)

status = pd.read_csv("data/status.csv")

results = pd.read_csv("data/results.csv")
results = results[['resultId', 'driverId', 'raceId', 'constructorId', 'points', 'position', 'fastestLapTime', 'statusId']]
results['position'].replace('\\N', 0, inplace=True)
results['fastestLapTime'].replace('\\N', '', inplace=True)

driver_standings = pd.read_csv("data/driver_standings.csv")
driver_standings.drop(['driverStandingsId', 'positionText'], axis=1, inplace=True)

lapTimes = pd.read_csv("data/lap_times.csv")
lapTimes.drop(['milliseconds'], axis=1, inplace=True)

pitStops = pd.read_csv("data/pit_stops.csv")
pitStops.drop('milliseconds', axis=1, inplace=True)
print(pitStops)

constStands = pd.read_csv("data/constructor_standings.csv")
constStands.drop(['constructorStandingsId', 'positionText'], axis=1, inplace=True)

# -x-x-x-x-x-x-x-x-x-x-x-x-x
# Inserting data into each table one by one

insertCircuits = """INSERT INTO circuits(circuitID, name, location, country, lat, lng) VALUES(%s, %s, %s, %s, %s, %s)"""

for row in circuits.values.tolist():
    cur.execute(insertCircuits, tuple(row))

insertRaces = """INSERT INTO races(raceID,year,round,circuitID,name,date,time) VALUES(%s, %s, %s, %s, %s, %s, %s)"""

for row in races.values.tolist():
    cur.execute(insertRaces, tuple(row))

insertConstructors = """INSERT INTO constructors(constructorID, name, nationality) VALUES(%s, %s, %s)"""
for row in constructors.values.tolist():
    cur.execute(insertConstructors, tuple(row))

insertDrivers = """INSERT INTO drivers(driverID, number, code, forename, surname, dob, nationality) VALUES(%s, %s, %s, %s, %s, %s, %s)"""
for row in drivers.values.tolist():
    print(row)
    cur.execute(insertDrivers, tuple(row))

insertStatus = """INSERT INTO status(statusID, description) VALUES(%s, %s)"""
for row in status.values.tolist():
    cur.execute(insertStatus, tuple(row))

insertResults = """INSERT INTO results(resultID, driverID, raceID, constructorID, points, position, fastestLapTime, statusID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
for row in results.values.tolist():
    cur.execute(insertResults, tuple(row))
    
insertDriverStand = """INSERT INTO driverStandings(raceID, driverID, points, position, wins) VALUES(%s, %s, %s, %s, %s)"""
for row in driver_standings.values.tolist():
    cur.execute(insertDriverStand, tuple(row))
    
insertLapTimes = """INSERT INTO lapTimes(raceID, driverID, lap, position, time) VALUES(%s, %s, %s, %s, %s)"""
for row in lapTimes.values.tolist():
    cur.execute(insertLapTimes, tuple(row))

insertPitStops = """INSERT INTO pitStops(raceID, driverID, stop, lap, time, duration) VALUES(%s, %s, %s, %s, %s, %s)"""
for row in pitStops.values.tolist():
    cur.execute(insertPitStops, tuple(row))
    
insertConstStands = """INSERT INTO constructorStandings(raceID, constructorID, points, position, wins) VALUES(%s, %s, %s, %s, %s)"""
for row in constStands.values.tolist():
    cur.execute(insertConstStands, tuple(row))

conn.commit()
cur.execute("SELECT * FROM constructorStandings;")
print(cur.fetchall())
conn.close()