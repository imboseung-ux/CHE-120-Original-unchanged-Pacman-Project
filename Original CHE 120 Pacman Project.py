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


def change(x, y):
    """Change pacman aim if valid."""
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()
Logo


