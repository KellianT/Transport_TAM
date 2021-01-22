import sqlite3
import argparse
import sys
import urllib.request
from time import *
import logging


logging.basicConfig(
    filename='tam.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s - %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',)


logging.info('Demarrage du programe')


def clear_rows(cursor):
    """ This function does : Delete lines in table 'infoarret' for refresh the
    the line in the column before update.

    cursor : Cursor is the bridge that connects Python and SQlite databases
    and works under SQLite3 built-in package and It will be use to execute SQL
    commands. It acts like a position indicator and will be mostly use to
    retrieve data.

    """
    cursor.execute("""DELETE FROM infoarret""")
    logging.info('clear_rows: Efface les lignes dans la table')


def insert_csv_row(csv_row, cursor):

    """ This function insert values in table 'infoarret'

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    csv_row : retrieve the lines on the csv file.

    """
    cursor.execute("""INSERT INTO infoarret VALUES (?,?,?,?,?,?,?,?,?,?,?) """,
                   csv_row.strip().split(";"))


def load_csv(path, cursor):
    """ This function load and read the csv file, and insert row in db file.

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    path : Source of the csv file.

    """
    with open(path, "r") as f:
        # ignore the header
        f.readline()
        line = f.readline()
        # loop over the lines in the file
        while line:
            insert_csv_row(line, cursor)
            line = f.readline()
    logging.info('load_csv: Charge la base de données')


def remove_table(cursor):
    """This function remove table 'infoarret' if exist,
    for remove before update

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    """
    cursor.execute("""DROP TABLE IF EXISTS infoarret""")
    logging.info('remove_table: la table est supprime')


def create_schema(cursor):
    """ This function create table 'infoarret' if not exist

    this table contains 11 columns and determinate the type.

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    """
    cursor.execute("""CREATE TABLE IF NOT EXISTS "infoarret" (
    "course"	INTEGER,
    "stop_code"	TEXT,
    "stop_id"	INTEGER,
    "stop_name"	TEXT,
    "route_short_name"	TEXT,
    "trip_headsign"	TEXT,
    "direction_id"	INTEGER,
    "is_theorical" INTEGER,
    "departure_time"	TEXT,
    "delay_sec"	INTEGER,
    "dest_arr_code"	INTEGER
    );""")
    logging.info('create_schema: on cree les colonnes de la base')


def temps_arrive(horaire):
    """This function return time (sec) to time (min,sec)"""
    logging.info("temps_arrive: Conversion du temps d'attente")
    return strftime('%M min %S sec', gmtime(horaire))


def time_tram(database, cursor):  # argument 'time' tram
    """ This function configure the argument 'time'

    this function request
    the database for recuperate the line in the column
    (stop_name , trip_headsign and route_short_name) and return the request

    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    database : Search in the SQlite database

  """
    cursor.execute("""
    SELECT * FROM infoarret
    WHERE stop_name = ? AND trip_headsign = ? AND route_short_name = ?
    """, (args.station, args.destination, args.ligne))
    for row in cursor:
        if args.fichier:
            time_passage = str(f'Prochain passage de la ligne {row[4]} passant à {row[3]} vers {row[5]} départ dans : {temps_arrive(row[9])}\n')
            with open("passage.txt", "a", encoding='utf8') as f:
                f.writelines(time_passage)
        else:
            print(f'Prochain passage de la ligne {row[4]} passant à {row[3]} vers {row[5]} départ dans : {temps_arrive(row[9])}')
    logging.info("time_tram: Affichage de la demande de l'utilisateur(argument time) ")


def next_tram(database, cursor):  # argument 'next' tram
    """The function configure the argument 'next'

    this function request the
    database for recuperate line in the column stop_name,delay_sec and
    route_short_name.
    Then it returns the next passes in min,sec, the line and the direction.
    cursor : It acts like a position indicator and will be mostly use to
    retrieve data.

    database : Search in the SQlite database.


    """
    cursor.execute("""
    SELECT * FROM infoarret
    WHERE stop_name = ?
    """, (args.station, ))
    for row in cursor:
        if args.fichier:
            passage = str(f'Ligne {row[4]} vers {row [5]} départ dans : {temps_arrive(row[9])}\n')
            with open("passage.txt", "a", encoding='utf8') as f:
                f.writelines(str(passage))
        else:
            print(f'Ligne {row[4]} vers {row [5]} départ dans : {temps_arrive(row[9])}')
    logging.info("next_tram: Affichage de la demande de l'utilisateur(argument next) ")


def update_db():
    """This function, retrieve the csv from url and download this csv file

    """
    csv_url = 'https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv'
    urllib.request.urlretrieve(csv_url, 'tam.csv')
    logging.info('update_db: Mise a jour de la base de données')


parser = argparse.ArgumentParser("Script to interact with data from TAM API")
parser.add_argument("-l", "--ligne", type=str, help="entre ligne de tram")
parser.add_argument("-d", "--destination", type=str, help="entre destination")
parser.add_argument("-s", "--station", type=str, help="entre une station")
parser.add_argument("-c", "--currentdb", type=str, help="Use existing db")
parser.add_argument("action", nargs='?', help="next tram or time tram")
parser.add_argument("-f", "--fichier", action='store_true', help="create file")

args = parser.parse_args()


def main():
    """ This function, is the MAIN function :
    This function will check if the argument next or time has been entered by
    the user:

   If one of the two arguments was entered the program will continue and
   display the results to the user.
   If neither of the two arguments was entered by the user the program will
    display an error message and close.

    """
    logging.info('Demarrage de la fonction main')
    if not args.action:
        print("Error : il manque un argument action ('time' ou 'next')")
        logging.warning('il manque un argument action')
        return 1
    if args.action == 'time':
        if not args.station or not args.ligne or not args.destination:
            print("Error: il manque la ligne et/ou la station et/ou la destination dans les arguments")
            logging.warning('il manque la ligne et/ou la station et/ou la destination dans les arguments')
            return 1
    if args.action == 'next':
        if not args.station:
            print("Error: il manque la station dans les arguments")
            logging.warning('il manque la station dans les arguments')
            return 1

    conn = sqlite3.connect('tam.db')

    if not conn:  # si format ne convient pas, si la base est corrompue...etc
        print("Error : could not connect to database ")
        logging.warning('impossible de se connecter à la base de données')
        return 1

    c = conn.cursor()
    remove_table(c)
    if args.currentdb:
        create_schema(c)
        load_csv(args.currentdb, c)
    else:
        update_db()
        dl = 'tam.csv'
        remove_table(c)
        create_schema(c)
        load_csv(dl, c)
    if args.action == 'time':
        time_tram('tam.db', c)
    elif args.action == 'next':
        next_tram('tam.db', c)

    conn.commit()
    conn.close()
    logging.info('Programme fini !!!!!')


if __name__ == "__main__":
    sys.exit(main())
