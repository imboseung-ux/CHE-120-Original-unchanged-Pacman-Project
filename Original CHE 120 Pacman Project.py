"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice
from turtle import *

from freegames import floor, vector

state = {'score': 0}
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0)
pacman = vector(-40, -80)
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

tiles = [
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]
#Es: This function draws a games borders Our code uses Turtle graphics, so when drawing an object the code works with a pen.
def square(x, y):
    """Draw square using path at (x, y).""" 
    path.up() #ES: Lifts the pen up to allow it to move without drawing
    path.goto(x, y)#ES: Moves the pen to the top left corner of the square
    path.down() #ES: Puts the pen down to start initiating the drawing 
    path.begin_fill() #ES: This starts to fill in the shape

    for count in range(4): #ES: Using a for loop to draw 4 sides 
        path.forward(20) #ES: Moves the pen forward by 20 pixels to draw a straight line
        path.left(90) #ES: Then it turns it left by 90 degrees to draw the next line untill count reaches 3 (total of 4 times)

    path.end_fill() #ES: Finishes filling in the square

#Es: This function is in charge of the tiling system. Essentially tells us which tile Pac-Man or a Ghost is on currently
def offset(point): #ES: 
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20 #ES: Converts the x coordinate to a column number. First it uses floor to round down to nearest multiple of 20, and then shifts the leftmost tile to 0 by adding 200. Finally it divides by 20 to convert the pixels to column number (0 to 19)
    y = (180 - floor(point.y, 20)) / 20 #ES: Converts the y coordinte to a row number. First it also uses floor to round down to nearest multiple of 20, and next flips the y-axis so the top left is at 0,0 by subtracting the point.y value from 180. Finally it divides by 20 to convert the pixels to row number (0 to 19)
    index = int(x + y * 20)#ES:  Converts both the row and column to the "1D" list index .By ensuring we have an integer index, we use the int function. Then, (Y*20) skips all the tiles in previous rows, and (+x) moves the column in the current row
    return index#ES: Returns the variable index

#Es: This function is used to check if the point is a valid location for Pac-Man or a ghost
def valid(point):#ES: 
    """Return True if point is valid in tiles."""
  
index = offset(point)  
# ES: Converts the point's pixel coordinate to a tile index in the tiles array  
# ES: Checks the top-left corner of the sprite to see if it is inside a wall  
if tiles[index] == 0:  
    # ES: If the top-left corner is a wall, the move is not valid  
    return False  

index = offset(point + 19)  
# ES: Converts the bottom-right corner of the sprite to a tile index  
# ES: Checks this corner to make sure the rest of the 20x20 sprite does not overlap a wall  
if tiles[index] == 0:   # ES: If the bottom-right corner is a wall, the move is not valid 
    
    return False  

    return point.x % 20 == 0 or point.y % 20 == 0 #ES: Only allow moves when Pac-Man or the ghost is aligned to the 20 pixel grid  
                                                # ES: This prevents clipping through walls between tiles 
def world():
    """Draw world using path."""
    bgcolor('black')
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')


def move():
    """Move pacman and all ghosts."""
    writer.undo()
    writer.write(state['score'])

    clear()

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
            options = [
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options)
            course.x = plan.x
            course.y = plan.y

        up()
        goto(point.x + 10, point.y + 10)
        dot(20, 'red')

    update()

    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

    ontimer(move, 100)

#CJ: This function changes the pacman movement direction taking in an x direction and y direction
def change(x, y):
    """Change pacman aim if valid."""
    #CJ: Uses valid function above to check if the direction the user wants pacman to turn to is allowed.  So not a wall
    if valid(pacman + vector(x, y)):
        #CJ: If the direction change is to a valid location, change the directin to the new direction wanted
        aim.x = x
        aim.y = y

#CJ: This is a function from the turtle module that specifies the dimensions of the screen.  The first two arguments give the width and height.  The
#last two arguments are the position the turtle will begin drawing from.  So this board will be 420 pixels by 420 pixels and the turtle will start
#at pixel 370 on the x axis and pixel 0 on the y axis
setup(420, 420, 370, 0)
#CJ: This function hides the icon for the turtle while it is drawing since it is not a part of the game
hideturtle()
#CJ: This function controls the automatic screen updates.  By setting it to false, it means the screen will not update with whatever the turtle is drawing
#until it is told to update the screen.  This prevents the turtle from updating after every single change which would cause lag
tracer(False)
#CJ: This line tells the turtle to go to a specific spot on the game screen, pixel 160 by 160
writer.goto(160, 160)
#CJ: Tells the turtle to draw in the colour white
writer.color('white')
#CJ: tells the turtle to write what ever the value inside the () is.  In this case, it is pulling a value from the dictionary, state using the key, 'score'
#This is where the game score is stored in the game so the turtle will write whatever the game score is
writer.write(state['score'])
#CJ: This function tells python to start detecting keyboard inputs
listen()
#CJ: The following four lines detects if the user has pressed an arrow key.  They are denoted by the last argument of the function
#Such as "Right" being the right arrow key.  Onkey works using two arguments.  When the key specified in the last one is pressed,
#It will run the function in the first argument.  Since the onkey function wants a function and not the result of a function, lambda
#is used to create a nameless function that when run, calls the change function.  For example, since change(5,0) is not a funcition, but
#the result of a function, it will not work with the onkey function as intended.  It wants to call the change function when the right arrow
#key is pressed, not run whatever the result of it is
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
#CJ: calls world function above to draw the map
world()
#CJ: Calls move function above to set the pacman and ghosts into motion
move()
#CJ: This tells the screen to stay open and active even after all the turtle drawing has been complete and starts an event loop so that the 
#program will continue detecting keyboard inputs
done()
Logo



