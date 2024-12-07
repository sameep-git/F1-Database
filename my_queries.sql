/*
 *	Returns: circuitID, name, location of all the circuits that are located in USA
 *	Does it work: Yes
 *	Sample screenshot: https://ibb.co/1bSYrpQ
 */
select circuitID, name, location
from circuits
where country="USA";

/*
 *	Returns: driverID, forename, surname, constructorName and race_count
 *			 of all the teams Fernando Alonso (driverID = 4) has raced with.
 *	Does it work: Yes
 *	Sample screenshot: https://ibb.co/7kT2C1L
 */
select d.driverID, d.forename as first_name, d.surname as last_name, c.name as team_name, count(*) as race_count
from drivers d
join results r on d.driverID = r.driverID
join constructors c on r.constructorID = c.constructorID
where d.driverID = 4
group by c.constructorID
order by c.name ASC;

/*
 *	Returns: Returns the team with the most number of wins. Columns
			 returned are teamID, teamName and win_count
 *	Does it work: Yes
 *	Sample screenshot: https://ibb.co/tDdN4sj
 */
SELECT c.constructorID as team_ID, c.name as team_name, COUNT(*) AS win_count
FROM results r
JOIN constructors c on c.constructorID = r.constructorID
WHERE position = 1
GROUP BY c.constructorID
HAVING COUNT(*) = (
    SELECT MAX(win_count)
    FROM (
        SELECT COUNT(*) AS win_count
        FROM results
        WHERE position = 1
        GROUP BY constructorID
    ) AS sub
);

/*
 *	Returns: Selects all drivers that raced in the 2012 season and sums up
			 their total pit stops durations for that season and groups the
			 result by driverID and orders by total duration in ascending order.
 *	Does it work: Yes
 *	Sample screenshot: https://ibb.co/9cHbnzk
 */
SELECT d.driverID as driver_ID, d.forename as first_name, d.surname as last_name, sum(ps.duration) as total_pit_stops_time
FROM drivers d
JOIN pitStops ps ON ps.driverID = d.driverID
WHERE ps.raceID in (
	SELECT raceID
    FROM races
    WHERE year = 2012
)
GROUP BY d.driverID
ORDER BY total_pit_stops_time ASC;

/* Level 2 queries */
/*
 *	Returns: Inserts a row of result into the results table
			 for Las Vegas Grand Prix (1142) for driver Lewis Hamilton (1)
 *	Does it work: Yes
 *	Sample screenshot: https://ibb.co/kKG9KyV
 */
INSERT INTO results (driverID, raceID, constructorID, points, position, fastestLapTime, statusID)
VALUES (1, 1142, 131, 25, 1, '01:35:01', 1);

/*
 *	Returns: Deletes the result for Las Vegas Grand Prix (1142) for driver Lewis Hamilton (1)
 *	Does it work: Yes
 *	Sample screenshot: https://ibb.co/c18dMX5
 */
 
-- DELETE FROM results
-- WHERE raceID = 1142 AND driverID = 1;

/*
 *	Returns: Update constructors where constructorID = 10
			 to 384. Constructor is "Force India"
 *	Does it work: Yes
 *	Sample screenshot: https://ibb.co/RjNz7mx
 */
UPDATE constructors
SET constructorID = 384
WHERE constructorID = 10;

/*
 *	Returns: We try to delete driver with driverID = 39,
			 which is "Narain Karthikeyan" but as we have set
			 ON DELETE to RESTRICT, we cannot delete the record
             and driverStandings still has all of the records
             with driverID = 39.
 *	Does it work: No
 *	Sample screenshot: https://ibb.co/RH3tD03
 */
DELETE FROM drivers
WHERE driverID = 39;