import sqlite3
import argparse
import sys
import urllib.request
#import csv
from time import *

    

def clear_rows(cursor):
    cursor.execute("""DELETE FROM infoarret""")


def insert_csv_row(csv_row, cursor):   
    cursor.execute("""INSERT INTO infoarret VALUES (?,?,?,?,?,?,?,?,?,?,?) """,
                   csv_row.strip().split(";"))


def load_csv(path, cursor):
    with open(path, "r") as f:
        # ignore the header
        f.readline()
        line = f.readline()
        # loop over the lines in the file
        while line:
            insert_csv_row(line, cursor)
            line = f.readline()

def remove_table(cursor):
    cursor.execute("""DROP TABLE IF EXISTS infoarret""")

def create_schema(cursor):
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

def temps_arrive(horaire):
    return strftime('%M min %S sec', gmtime(horaire))

def time_tram(database, cursor):  # argument 'time' tram
    cursor.execute("""
    SELECT * FROM infoarret
    WHERE stop_name = ? AND trip_headsign = ? AND route_short_name = ?
    """, (args.station, args.destination, args.ligne))
    for row in cursor:
        print(f'Prochain passage de la ligne {row[4]} passant à {row[3]} vers {row[5]} départ dans : {temps_arrive(row[9])}')

def next_tram(database, cursor):  # argument 'next' tram
    cursor.execute("""
    SELECT * FROM infoarret
    WHERE stop_name = ?
    """, (args.station, ))
    for row in cursor:
        print(f'Ligne {row[4]} vers {row [5]} départ dans : {temps_arrive(row[9])}')


def update_db():
    csv_url = 'https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv'
    urllib.request.urlretrieve(csv_url, 'tam.csv')

parser = argparse.ArgumentParser("Script to interact with data from the TAM API")
parser.add_argument("-l", "--ligne", type=str, help="entre une ligne de tram")
parser.add_argument("-d", "--destination", type=str, help="entre une destination" )
parser.add_argument("-s", "--station", type=str, help="entre une station" )
parser.add_argument("-c", "--currentdb", type=str, help="Use exciting database")
parser.add_argument("action", help="next tram or time tram")
parser.add_argument("-f", "--fichier", action='store_true', help="créer un fichier" )

args = parser.parse_args()



def generer_doc():

    fichier = open('passages.txt', 'w', encoding='utf8')
    fichier = fichier.writelines()
    for lignes in fichier:
        print(lignes)


def main():
    if not args.action:
        print("Error : il manque un argument action ('time' ou 'next')")
        return 1
    if args.action == 'time': 
        if not args.station or not args.ligne or not args.destination: 
            print("Error: il manque la ligne et/ou la station et/ou la destination dans les arguments")
            return 1
    if args.action == 'next':
        if not args.station: 
            print("Error: il manque la station dans les arguments")
            return 1

    conn = sqlite3.connect('tam.db')

    if not conn: # si format ne convient pas, si la base est corrompue...etc
        print("Error : could not connect to database ")
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

    

    

    
if __name__ == "__main__":
    sys.exit(main())
