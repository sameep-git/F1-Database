# F1-Database

### Description:
This is a MySQL implementation of a [F1 database on Kaggle ](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) which supports the following tables with the listed columns:

 - circuits - circuitID, name, location, country, lat, lng
 - constructors - constructorID, name, nationality
 - constructorStandings - raceID, constructorID, wins, points, position
 - drivers - driverID, forename, surname, number, code, nationality, dob
 - driverStandings - driverID, raceID, wins, points, position
 - lapTimes - driverID, raceID, lap, position, time
 - pitStops - driverID, raceID, stop, lap, time, duration
 - races - raceID, circuitID, name, year, date, time, round
 - results - resultID, driverID, raceID, constructorID, points, position, fastestLapTime, statusID
 - status - statusID, description

The data is a collection of information of F1 races from 1950 onwards. It includes all the present and past circuits, teams (constructors), drivers and even includes lap times, pit stops and results of drivers in different races!

### How to setup/run:

 1. Create a Python virtual environment.
 2. Install all the requirements by:
	  `pip3 install -r requirements.txt`
 3. Set up the database in MySQL by:
	 `python3 setup.py`
 4. Run the CLI app by:
	 `python3 front_end.py`
	