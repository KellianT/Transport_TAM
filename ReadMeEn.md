Transport_TAM

Projet_TAM


Welcome to our Python 3 program which will allow you to have the next live passages of the Montpellier tramways.

To execute the script you will have to enter in your command line :


C:\Users_path_of_the_program> Python tam2.py arguments*


Then, several arguments* will be possible:

The argument -s will allow you to indicate a station.

The argument -l will allow you to indicate a line.

The argument -d will allow you to specify a destination.

The argument -f will download a text file with the results of your search.

The next argument will tell you the next departures to the desired station.

The time argument will tell you the next departure from a desired station to the desired destination.


Here are a few examples:


C:\Users_path_of_program> Python tam2.py next -s COMEDIE


In this example the user has used the next argument to know the next passes to the COMEDIE station he has defined with the -s argument.


HERE IS THE RESULT :


Ligne 1 vers MOSSON départ dans : 01 min 37 sec

Ligne 1 vers MOSSON départ dans : 10 min 05 sec

Ligne 1 vers MOSSON départ dans : 14 min 46 sec

Ligne 1 vers ODYSSEUM départ dans : 04 min 29 sec

Ligne 1 vers ODYSSEUM départ dans : 16 min 49 sec

Ligne 1 vers ODYSSEUM départ dans : 31 min 08 sec

Ligne 2 vers JACOU départ dans : 02 min 20 sec

Ligne 2 vers JACOU départ dans : 14 min 49 sec

Ligne 2 vers ND DE SABLASSOU départ dans : 26 min 39 sec

Ligne 2 vers SABINES départ dans : 03 min 10 sec

Ligne 2 vers SABINES départ dans : 16 min 43 sec

Ligne 2 vers ST-JEAN DE VEDAS départ dans : 09 min 44 sec



In this example the user will use the time argument to know the next passes from a station he wants with the -s argument to a destination he has defined with the -d argument.


C:\Users_program_path> Python tam2.py time -s COMEDIE -l 1 -d MOSSON


HERE IS THE RESULT:


Prochain passage de la ligne 1 passant à COMEDIE vers MOSSON départ dans : 02 min 00 sec

Prochain passage de la ligne 1 passant à COMEDIE vers MOSSON départ dans : 07 min 06 sec
