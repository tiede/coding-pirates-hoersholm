#!/bin/python3

from emoji import * 
from datetime import *
from random import randint

# Put function definitions under here
def roll_dice():
  print(python, 'can make a', dice)
  max = input('How many sides?:') #Wait for input from the user
  print('That\'s a D', max) #Use the number the user entered
  roll = randint(1, int(max)) #randint needs max to be an 'integer'
  print('You rolled a', roll)
  print(fire * roll)

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

roll_dice() # Call the roll dice function

born_day = input('Enter day of your birthday?:')
born_month = input('Enter month of your birthday?:')
born_year = input('Enter year of your birthday?:')

#date_str = '24/02/1975'
date_str = born_day + '/' + born_month + '/' + born_year
date = datetime.strptime(date_str, '%d/%m/%Y')6
print('You were born on', date.strftime('%A'))