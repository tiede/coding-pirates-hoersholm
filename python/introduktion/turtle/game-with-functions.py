import turtle
import random

RADIUS = 40

def turn(player, playername, die):
    player_turn = input(playername + ": Press 'Enter' to roll the die ")
    die_outcome = random.choice(die)
    print("The result of the die roll is: ")
    print(die_outcome)
    print("The number of steps will be: ")
    print(20*die_outcome)
    player.fd(20*die_outcome)

def draw_goal(player):
    original_position = player.pos()
    player.goto(300, original_position[1] - RADIUS)
    player.pendown()
    player.circle(RADIUS)
    player.penup()
    player.goto(original_position)

def initialize(color, x, y):
    player = turtle.Turtle()
    player.color(color)
    player.shape("turtle")
    player.penup()
    player.goto(x,y)
    return player  

def in_goal(player):
    return round(player.xcor()) >= 300-RADIUS

player_one = initialize("green", -200, 100)
player_two = initialize("blue", -200, -100)

draw_goal(player_one)
draw_goal(player_two)

die = [1,2,3,4,5,6]

for i in range(20): 
    turn(player_one, "Player 1", die)
    turn(player_two, "Player 2", die)
 
    print(round(player_one.xcor()))
    print(round(player_two.xcor()))

    if in_goal(player_one) and in_goal(player_two):
        print("Its a draw")
        break
    elif in_goal(player_one):
        print("Player One Wins!")
        break
    elif in_goal(player_two):
        print("Player Two Wins!")
        break