#!/bin/python3

from emoji import * 
from datetime import *
from random import randint

import requests

# Put function definitions under here
def oversaet_ugedag(dato):
    ugedag = dato.strftime('%A')
    match ugedag:
        case 'Monday':
            return 'Mandag'
        case 'Tuesday':
            return 'Tirsdag'
        case 'Wednesday':
            return 'Onsdag'
        case 'Thursday':
            return 'Torsdag'
        case 'Friday':
            return 'Fredag'
        case 'Saturday':
            return 'Lørdag'
        case 'Sunday':
            return 'Søndag'

# Useful characters :',()*_/.#

# Put code to run under here
print('Hello')
print('Hello', world)
print('Welcome to', python)
print(fire)

print(232*45*98+25/10)

nu = datetime.now()
print(nu)

print(datetime.now() - timedelta(hours=100))

navn = input('Hvad er dit navn?:')
print('Du hedder', navn)

dag = input('Hvilken dag blev du født?:')
maaned = input('Hvilken måned blev du født?:')
aar = input('Hvilket år blev du født?:')

dato = dag + '/' + maaned + '/' + aar

print(dato)

dato_som_date = datetime.strptime(dato, '%d/%m/%Y')

print(dato_som_date)

print('Du blev født på en', oversaet_ugedag(dato_som_date))