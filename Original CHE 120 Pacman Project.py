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
#<<<<<<< patch-1
# ---------------------- DRAWING FUNCTIONS -----------------

#Es: This function draws a games borders Our code uses Turtle graphics, so when drawing an object the code works with a pen.
#>>>>>>> main
def square(x, y):
    """Draw square using path at (x, y)."""
    path.up() #ES: Lifts the pen up to allow it to move without drawing
    path.goto(x, y) #ES: Moves the pen to the top left corner of the square
    path.down() #ES: Puts the pen down to start initiating the drawing 
    path.begin_fill() #ES: This starts to fill in the shape

    for count in range(4): #ES: Using a for loop to draw 4 sides 
        path.forward(20) #ES: Moves the pen forward by 20 pixels to draw a straight line
        path.left(90) #ES: Then it turns it left by 90 degrees to draw the next line untill count reaches 3 (total of 4 times)

    path.end_fill() #ES: Finishes filling in the square

#Es: This function is in charge of the tiling system. Essentially tells us which tile Pac-Man or a Ghost is on currently
def offset(point):
    x = (floor(point.x, 20) + 200) / 20 #ES: Converts the x coordinate to a column number. First it uses floor to round down to nearest multiple of 20, and then shifts the leftmost tile to 0 by adding 200. Finally it divides by 20 to convert the pixels to column number (0 to 19)
    y = (180 - floor(point.y, 20)) / 20 #ES: Converts the y coordinte to a row number. First it also uses floor to round down to nearest multiple of 20, and next flips the y-axis so the top left is at 0,0 by subtracting the point.y value from 180. Finally it divides by 20 to convert the pixels to row number (0 to 19)
    index = int(x + y * 20)#ES:  Converts both the row and column to the "1D" list index .By ensuring we have an integer index, we use the int function. Then, (Y*20) skips all the tiles in previous rows, and (+x) moves the column in the current row
    return index#ES: Returns the variable index


#Es: This function is used to check if the point is a valid location for Pac-Man or a ghost
def valid(point):

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




