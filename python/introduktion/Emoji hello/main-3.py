#!/bin/python3

from emoji import * 
from datetime import *
from random import randint

# Put function definitions under here

# Useful characters :',()*_/.#

# Put code to run under here
print('Hello')
print('Hello', world)
print('Welcome to', python)

print(python, 'is very good at', sums)
print(230 * 5782 ** 2 / 23781)

print( (2 + 4) * (5 + 3) )

print('The', calendar, clock, 'is', datetime.now()) #Print with emoji

print(datetime.now() + timedelta(days=100))

date_str = '24/02/1975'
date = datetime.strptime(date_str, '%d/%m/%Y')
print(date.weekday())
print('You were born on', date.strftime('%A'))