"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.
"""

from random import choice #BK: This is for random ghost movement
from turtle import * #BK: Turtle Graphic

from freegames import floor, vector #BK: Vector math + grid allignment from freegames

# ---------------------- GAME STATE ------------------------
state = {'score': 0} #BK: display the score as zero when the game starts

# ---------------------- TURTLE SETUP ---------------------
path = Turtle(visible=False) # For drawing maze
writer = Turtle(visible=False) # For showing score
aim = vector(5, 0)  # BK: direction and magnitude 
# Pacman starting position and direction
pacman = vector(-40, -80) #BK: pacman's direction of movement

# Ghosts with starting positions and directions
ghosts = [
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]

# ---------------------- MAP ------------------------------
#BK: Make a map 20 by 20 grid using 0, which is a wall, and 1 ,which is the tile
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
# ---------------------- DRAWING FUNCTIONS -----------------
def square(x, y):
    """Draw square using path at (x, y)."""
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()


def offset(point):
    """Return offset of point in tiles."""
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index


def valid(point):
    """Return True if point is valid in tiles."""
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0


def world(): #SC: The function creates the overall game board for the Pac-Man game, so the maze with its walls, as well as the dots
    """Draw world using path."""
    bgcolor('black') #SC: Sets the background color for the game as black
    path.color('blue') #SC: Sets the maze path color blue to tell the difference between the path and the walls

    for index in range(len(tiles)): #SC: This is a for loop that loops through all the tiles in the map. Since there are 400 tiles in the map, it will loop through this function 400 times
        tile = tiles[index] #SC: Sets a new variable for each specific tile due to the index going through all 400 positions

        if tile > 0: #SC: If statement, if the tile is a one on the map (the 20x20 grid above), also converting the 1D list to a 2D grid position, which is why you need to %20 and //20 to convert to column and row
            x = (index % 20) * 20 - 200 #SC: Since the x-coordinate system works the same in code and in the game, to center the game, the x coordinates need to shift over -200, the *20 converts grid units to pixels
            y = 180 - (index // 20) * 20 #SC: Y-coordinate system for the game is inversely proportional to the computer coordinate system, so that is why you need to inverse it
            square(x, y) #SC: At that position, draws a blue pathway for Pac-Man to go on to

            if tile == 1: #SC: If statement, if the tile is equal to one, which represents the white pellet/dot
                path.up() #SC: lifts the "pen" or object/turtle's pen so it doesn't draw anything
                path.goto(x + 10, y + 10) #SC: moves the "pen" to the center of the cell
                path.dot(2, 'white') #SC: Draws the white dot/pellet for the Pac-Man to eat
                
# ---------------------- GAME LOOP -------------------------
def move(): #SC: This function runs the entire game, as it does movement for everything and the game logic for the game
    """Move pacman and all ghosts."""
    writer.undo()  #SC: clears the last thing the writer wrote, aka the score
    writer.write(state['score']) #SC: writes the new current score of the game

    clear() #SC: Clears all moving elements of the game, but not things drawn in the world function as they do not change 

    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman) #SC: recalls the offset function, translating the pixel position of Pac-Man to the grid index to tell the game what Pac-Man is standing on

    if tiles[index] == 1: #SC: If statement, if the tile Pac-Man is on is a dot(because of the 1 on the grid)
        tiles[index] = 2 #SC: This marks the dot as collected, so it will no longer show up
        state['score'] += 1 #SC: updates the score after the dot has been collected
        x = (index % 20) * 20 - 200 #SC: the position is then redrawn with another square, with the dot no longer appearing with the square function
        y = 180 - (index // 20) * 20
        square(x, y)

    up() #SC: Lifts the "pen" of the object or turtle's pen so it stops drawing
    goto(pacman.x + 10, pacman.y + 10) #SC: Goes to the center of the cell 
    dot(20, 'yellow') #SC: Draws the pacman as the yellow dot in the center of the cell

    for point, course in ghosts: #SC: Ghost movement loop/ movement AI
        if valid(point + course): #SC: calculates the ghosts' next position, checking if it's valid or not, so not a wall
            point.move(course) #SC: if the next position is valid, it continues in that direction 
        else: #SC: if the ghost is blocked (the new position is not valid)
            options = [     #SC: randomly picks a new choice out of the 4 available, left, right, up, or down
                vector(5, 0),
                vector(-5, 0),
                vector(0, 5),
                vector(0, -5),
            ]
            plan = choice(options) #SC: randomly picks a new choice out of the 4 available, left, right, up, or down
            course.x = plan.x #SC: these then make the ghost go in the desired direction. If the new direction the ghost chooses is also a wall, it chooses a new direction until a valid direction is chosen
            course.y = plan.y

        up() #SC: Lifts the "pen" of the object or turtle's pen so it stops drawing
        goto(point.x + 10, point.y + 10) #SC: Goes to the center of the cell 
        dot(20, 'red')  #SC: draws the ghost as a red dot

    update() #SC: this function then refreshes the graphics, so it gives all the latest changes

    for point, course in ghosts: #SC: this for ghost in ghosts loop is for collision detection of the ghost and Pac-Man
        if abs(pacman - point) < 20: #SC: This if statement checks if Pac-Man and a ghost are within 20 pixels both vertically and horizontally of each other
            return #SC: if the collision is detected, it stops the move function and doesn't execute the next frame, and the onTimer function won't be called

    ontimer(move, 100) #SC: schedules the next frame to run after 100 milliseconds 


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


