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
	
### Grade
I expect to receive a 100, as I have more than 650k rows over 10 tables that relate in some way (Schema Level 2). I have written 8 queries covering all the requirements in Queries Level 2, and I have made a dynamic CLI front-end using Python with at least two functions of the “read-only” queries and two functions of the “modification” queries that accept user input() to change parameters of the SQL queries dynamically (Python Level 1).

### Challenges I faced:

I faced the following challenges:

 1. Setting up the database was difficult as there were a lot more columns than I wanted to use, so I had to clean up the data before I could add it locally.
 2. There were a lot of null values, which I had to change before I could set up the database.
 3. I wanted to make a dynamic front end, so I had to spend some time finding a library which can help me exactly with how I pictured the front-end to look like.
 4. Because the front end is dynamic, I had to spend more time to make it functional, yet be pretty and easy to look at and use.

### Usage Preview:
https://github.com/user-attachments/assets/7eca4fb3-135c-42e6-8879-94a5b7691091
