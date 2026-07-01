import turtle
import pygame
from sense_hat import SenseHat
import time
import random
sense = SenseHat()
snakes = [turtle.Turtle(), turtle.Turtle(), turtle.Turtle()]
s = turtle.Screen()
s.colormode(255)
gridmaker = turtle.Turtle()
gridmaker.hideturtle()
gridmaker.color("grey")
gridmaker.speed(0)
gridmaker.penup()
gridmaker.goto(-200, 200)
gridmaker.pendown()
for i in range(4):
    gridmaker.fd(400)
    gridmaker.rt(90)
    gridmaker.fd(50)
    gridmaker.rt(90)
    gridmaker.fd(400)
    gridmaker.lt(90)
    gridmaker.fd(50)
    gridmaker.lt(90)
gridmaker.penup()
gridmaker.goto(200, 200)
gridmaker.rt(90)
gridmaker.pendown()
for i in range(4):
    gridmaker.fd(400)
    gridmaker.rt(90)
    gridmaker.fd(50)
    gridmaker.rt(90)
    gridmaker.fd(400)
    gridmaker.lt(90)
    gridmaker.fd(50)
    gridmaker.lt(90)
gridmaker.lt(90)
gridmaker.color("black")
for i in range(4):
    gridmaker.fd(400)
    gridmaker.rt(90)
apple = turtle.Turtle()
apple.penup()
apple.shape("square")
apple.color((255, 0, 0))
apple.shapesize(2.5)
apple.speed(0)
for snake in snakes:
    snake.penup()
    snake.shape("square")
    snake.color((0, 255, 0))
    snake.shapesize(2.5)
    snake.speed(0)
snakes[0].color((0, 50, 0))
snakes[0].goto(-75, 175)
snakes[1].goto(snakes[0].xcor()-50, snakes[0].ycor())
snakes[2].goto(snakes[0].xcor()-100, snakes[0].ycor())
pygame.init()
sense.clear()
r = (255, 0, 0)
g = (0, 255, 0)
w = (255, 255, 255)
h = (0, 50, 0)
sense.set_pixels([w, w, w, w, w, w, w, w,
                  w, w, w, w, w, w, w, w,
                  w, w, w, w, w, w, w, w,
                  w, w, w, w, w, w, w, w,
                  w, w, w, w, w, w, w, w,
                  w, w, w, w, w, w, w, w,
                  w, w, w, w, w, w, w, w,
                  w, w, w, w, w, w, w, w])
pos = [0, 2]
posses = [pos, [pos[0], pos[1]-1], [pos[0], pos[1]-2]]
applePos = [random.choice([-4, -3, -2, -1, 1, 2, 3, 4]), random.choice([-4, -3, -2, -1, 1, 2, 3, 4])]
heading = 1
lost = False
def moveSnakeHead():
    global pos
    global snakes
    global heading
    global lost
    global apple
    global moveTheApple
    snake = snakes[0]
    if heading == 0:
        if snake.xcor() < -125:
            lost = True
        else:
            pos = [pos[0], pos[1] - 1]
    elif heading == 1:
        if snake.xcor() > 125:
            lost = True
        else:
            pos = [pos[0], pos[1] + 1]
    elif heading == 2:
        if snake.ycor() < -125:
            lost = True
        else:
            pos = [pos[0] - 1, pos[1]]
    elif heading == 3:
        if snake.ycor() > 125:
            lost = True
        else:
            pos = [pos[0] + 1, pos[1]]
    if (snake.xcor() == apple.xcor()) and (snake.ycor() == apple.ycor()):
        moveTheApple = True
        snakes.append(turtle.Turtle(shape = "square"))
        for snakey in snakes:
            snakey.penup()
    for snakey in snakes:
        if (snake.xcor() == snakey.xcor()) and (snakey.ycor() == snake.ycor()) and snakey != snake:
            lost = True

def moveRestOfSnake():
    global snakes
    snakesToMove = len(snakes)-1
    for i in range(snakesToMove):
        body = snakes[snakesToMove-(i)]
        body.goto(snakes[snakesToMove-(i)-1].xcor(), snakes[snakesToMove-(i)-1].ycor())
def moveApple():
    global applePos
    global apple
    global moveTheApple
    moving = moveTheApple
    if moving:
        applePos = [random.choice([-4, -3, -2, -1, 1, 2, 3, 4]), random.choice([-4, -3, -2, -1, 1, 2, 3, 4])]
    if applePos[0] > 0 and applePos[1] > 0:
        apple.goto(applePos[0]*50-25, applePos[1]*50-25)
    elif applePos[0] < 0 and applePos[1] > 0:
        apple.goto(applePos[0]*50+25, applePos[1]*50-25)
    elif applePos[0] > 0 and applePos[1] < 0:
        apple.goto(applePos[0]*50-25, applePos[1]*50+25)
    elif applePos[0] < 0 and applePos[1] < 0:
        apple.goto(applePos[0]*50+25, applePos[1]*50+25)
    moveTheApple = False
moveTheApple = False
while lost != True:
    for event in sense.stick.get_events():
        if event.direction == 'left' and event.action == 'released':
            if (heading != 0 and heading != 1):
                    heading = 0
        elif event.direction == 'right' and event.action == 'released':
            if (heading != 0 and heading != 1):
                    heading = 1
        elif event.direction == 'down' and event.action == 'released':
            if (heading != 2 and heading != 3):
                    heading = 2
        elif event.direction == 'up' and event.action == 'released':
            if (heading != 2 and heading != 3):
                    heading = 3
    moveApple()
    sense.clear()
    sense.set_pixels([w, w, w, w, w, w, w, w,
                      w, w, w, w, w, w, w, w,
                      w, w, w, w, w, w, w, w,
                      w, w, w, w, w, w, w, w,
                      w, w, w, w, w, w, w, w,
                      w, w, w, w, w, w, w, w,
                      w, w, w, w, w, w, w, w,
                      w, w, w, w, w, w, w, w])
    for i in range(len(snakes)):
        snake = snakes[i]
        snake.penup()
        snake.shape("square")
        snake.shapesize(2.5)
        snake.speed(0)
        posses[i] = [((snake.xcor()+25)/50)-1, ((snake.ycor()+25)/50)-1]
        if snake != snakes[0]:
            snake.color((0, 255, 0))
            sense.set_pixel(posses[i][1], posses[i][0], h)
        else:
            sense.set_pixel(posses[i][1], posses[i][0], g)
    if applePos[0] > 0 and applePos[1] > 0:
        sense.set_pixel(applePos[0]+3, applePos[1]+3)
    elif applePos[0] < 0 and applePos[1] > 0:
        sense.set_pixel(applePos[0]+4, applePos[1]+3)
    elif applePos[0] > 0 and applePos[1] < 0:
        sense.set_pixel(applePos[0]+3, applePos[1]+4)
    elif applePos[0] < 0 and applePos[1] < 0:
        sense.set_pixel(applePos[0]+4, applePos[1]+4)
        
    origin = pos
    moveSnakeHead()
    moveRestOfSnake()
    snakes[0].goto(snakes[0].xcor() + ((pos[1]-origin[1])*50), snakes[0].ycor() + ((pos[0]-origin[0])*50))
    moveApple()
    print(applePos)
    time.sleep(0.1/((len(snakes)-2)**2))
print("Game over. Your score was: " + str(len(snakes)-3))
s.mainloop()