import mysql.connector
import os
from simple_term_menu import TerminalMenu
from tabulate import tabulate

def create_connection():
    """
    This creates a connection to the MySQL localhost with f1 database
    
    Args:
        None
    
    Returns:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
    
    """
    conn = mysql.connector.connect(
        user = 'root',
        password = 'root',
        host = 'localhost',
        database = 'f1'
    )
    return conn

def all_country_circuits(conn, country):
    """
    This lists all the circuits in a user input country.
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        string: Country name
        
    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("""
                    select circuitID, name, location
                    from circuits
                    where country = %s;
                   """, [country])
    res = cursor.fetchall()
    if len(res) > 0:
        print(tabulate(res, headers=['circuitID', 'name', 'location'], tablefmt='psql'))
    else:
        print("No results found :(")
    cursor.close()

def driver_teams(conn, driverID):
    """
    driverID, forename, surname, constructorName and race_count
 	of all teams the driver with driverID has raced with.
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        int: driverID
        
    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("""
                   select d.driverID, d.forename as first_name, d.surname as last_name, c.name as team_name, count(*) as race_count
                    from drivers d
                    join results r on d.driverID = r.driverID
                    join constructors c on r.constructorID = c.constructorID
                    where d.driverID = %s
                    group by c.constructorID
                    order by c.name ASC;
                   """, [driverID])
    res = cursor.fetchall()
    if len(res) > 0:
        print(tabulate(res, headers=['driverID', 'first_name', 'last_name', 'team_name', 'race_count'], tablefmt='psql'))
    else:
        print("No such driver found :(")
    cursor.close()

def team_most_wins(conn):
    """
    Returns the team with the most number of wins. Columns
    returned are teamID, teamName and win_count
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        int: driverID
        
    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("""
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
                   """)
    res = cursor.fetchall()
    if len(res) > 0:
        print(tabulate(res, headers=['teamID', 'team_name', 'win_count'], tablefmt='psql'))
    else:
        print("No teams found :(")
    cursor.close()
    
def sum_pit_stops(conn, year):
    """
    Selects all drivers that raced in the 2012 season and sums up
    their total pit stops durations for that season and groups the
    result by driverID and orders by total duration in ascending order.
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        int: year of the season we are interested in
        
    Returns:
        None
    """
    cursor = conn.cursor()
    cursor.execute("""
                    SELECT d.driverID as driver_ID, d.forename as first_name, d.surname as last_name, sum(ps.duration) as total_pit_stops_time
                    FROM drivers d
                    JOIN pitStops ps ON ps.driverID = d.driverID
                    WHERE ps.raceID in (
                        SELECT raceID
                        FROM races
                        WHERE year = %s
                    )
                    GROUP BY d.driverID
                    ORDER BY total_pit_stops_time ASC;
                   """, [year])
    res = cursor.fetchall()
    if len(res) > 0:
        print(tabulate(res, headers=['driverID', 'first_name', 'last_name', 'total_pit_stops_time'], tablefmt='psql'))
    else:
        print("No records found :(")
    cursor.close()

def insert_result(conn, data):
    """
    Inserts a row of result into the results table
    for raceID and for driverID
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        [int, int, int, int, int, string, int]: listed data in the order (driverID, raceID, constructorID, points, position, fastestLapTime, statusID)
        
    Returns:
        None
    """
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO results (driverID, raceID, constructorID, points, position, fastestLapTime, statusID) VALUES (%s, %s, %s, %s, %s, %s, %s);', data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
    cursor.close()

def delete_result(conn, data):
    """
    Deletes the result for raceID and driverID
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        [int, int]: lsited data in the order (raceID, driverID)
        
    Returns:
        None
    """
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM results WHERE raceID = %s AND driverID = %s;', data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
    cursor.close()
       
def update_constructorID(conn, data):
    """
    Update constructorID of a constructor to another
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        [int, int]: lsited data in the order (new constructorID, old constructorID)
        
    Returns:
        None
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        UPDATE constructors
                        SET constructorID = %s
                        WHERE constructorID = %s;""", data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
    cursor.close()

def delete_driver(conn, data):
    """
    Delete a driver from the database using driverID
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        int: driverID to be deleted
        
    Returns:
        None
    """
    cursor = conn.cursor()
    try:
        cursor.execute("""
                        DELETE FROM drivers
                        WHERE driverID = %s;""", data)
        conn.commit()
    except mysql.connector.Error as err:
        print(err)
        print("Error Code:", err.errno)
        print("SQLSTATE", err.sqlstate)
        print("Message", err.msg)
    cursor.close()

def menu(conn):
    """
    Sets up a dynamic menu to choose queries from using simple_term_menu
    
    Args:
        PooledMySQLConnection|MySQLConnectionAbstract: MySQL connection with the localhost and f1 database
        
    Returns:
        None
    """
    # Type out the menu forever so user can choose the next option
    while True:
        options = ["[1] Get all circuits located in specific country", "[2] List all teams a driver has raced with", "[3] List the team with the most wins",
                "[4] List all the drivers with sum of their pit stop times for a particular season", "[5] Insert a row into the results table", "[6] Delete a row from the results table",
                "[7] Update constructorID for a team", "[8] Delete a driver with a driverID", "[9] Exit this CLI"]
        terminal_menu = TerminalMenu(options, title="F1-Database", shortcut_key_highlight_style=("fg_purple",))
        menu_entry_index = terminal_menu.show()
        choice = menu_entry_index + 1
        match choice:
            case 1:
                country = input("What country's circuits would you like to list? => ")
                all_country_circuits(conn, country)
            case 2:
                driverID = input("What is the ID of the driver? => ")
                driver_teams(conn, driverID)
            case 3:
                team_most_wins(conn)
            case 4:
                year = input("What year (season) do you wish to look up? => ")
                sum_pit_stops(conn, year)
            case 5:
                print("Input the following information about the result record:")
                driverID = int(input("driverID => "))
                raceID = int(input("raceID => "))
                constructorID = int(input("constructorID/teamID => "))
                points = int(input("points => "))
                position = int(input("position => "))
                fastestLapTime = input("fastest lap time => ")
                status = int(input("status => "))
                data = [driverID, raceID, constructorID, points, position, fastestLapTime, status]
                insert_result(conn, data)
            case 6:
                print("Input the following information to delete a record from results:")
                raceID = int(input("raceID => "))
                driverID = int(input("driverID => "))
                data = [raceID, driverID]
                delete_result(conn, data)
            case 7:
                print("Input the following information to update constructorID:")
                newID = int(input("new constructorID => "))
                oldID = int(input("old constructorID => "))
                data = [newID, oldID]
                update_constructorID(conn, data)
            case 8:
                print("Input the following information:")
                driverID = int(input("driverID => "))
                delete_driver(conn, [driverID])
            case 9:
                return
            case default:
                print("Invalid choice :(")
                continue
        
        another_query_options = ["[1] Yes", "[0] No"]
        another_query_trm = TerminalMenu(another_query_options, shortcut_key_highlight_style=("fg_purple",), title="Would you like to make another query?")
        another_query_index = another_query_trm.show()
        if another_query_index == 0:
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            return

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    conn = create_connection()
    if conn is None:
        exit()
    menu(conn)
    conn.close()
    
if __name__ == '__main__':
    main()