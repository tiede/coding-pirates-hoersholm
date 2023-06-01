#!/bin/python3

# Import library code
from p5 import *
from random import randint

# The mouse_pressed function goes here

# The shoot_arrow function goes here

def setup():
# Setup your game here
  size(400, 400) # width and height

# Things to do in every frame
def draw():
  global wood
  sky = Color(92, 204, 206) # Red = 92, Green = 204, Blue = 206
  grass = Color(149, 212, 122)
  wood = Color(145, 96, 51)
  outer = Color(0, 120, 180)
  inner = Color(210, 60, 60) # Red
  middle = Color(220, 200, 0) # Yellow

  fill(sky)
  rect(0, 0, 400, 250)

# Keep this to run your code
run(frame_rate=2)