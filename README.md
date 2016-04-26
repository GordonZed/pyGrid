                                            ###
    ####### ### ### ####### ####### ### #######
    ### ### ### ### ### ### ###     ### ### ### ###
    ####### ####### ####### ###     ### ####### ###
    ###         ###     ###

# pyGrid

Grid based game engine for Python

## What's all this?

Making games can be scary if you've never done it before, what with all the graphics stuff that can end up making a simple game into a long and complicated looking piece of code.

PyGrid attempts to make game programming easier for new programmers by providing you with a simple grid, it's also just fun to play with if you're already an experienced programmer. You can set the number of horizontal and vertical cells contained in the grid, their size, colour, look, feel, etc. Then you simply turn those cells "on" or "off" according to what's going on in your game.

requires Python (<3.0) and Pygame.

## How do I use it?

First of all, you'll need to install PyGame and import Pygame and PyGrid into your script.

    import pygame
    import pygrid

After that, you can create a grid, which can be done in one line:

    my_grid = pygrid.pyGrid()

This will give you a grid with the default settings. Although more than likely, you'll want to customize the grid for your program.
All attributes are optional. From a functional standpoint, you'll want to set the first for: width, height, cell_width and cell_height.
The first two dictate how many horizontal and vertical cells your grid will consist of. cell_width and cell_height set the size of each cell in pixels.

    my_grid = pygrid.pyGrid(10, 20, 10, 10)

The above line will give you a 10 x 20 grid, with cells that are 10 pixels wide by 10 pixels tall.
Below is a more complete grid, followed by a quick explanation of what each attribute means.

    my_grid = pygrid.pyGrid(10, 20, 5, 5, 1, (0,0,0), (50,50,50), (0,0,255), 2, "My Awesome Game")

The first four attributes are the ones we just talked about above, the others are listed as follows.

#### border_weight: 1

Size (in pixels) of the margins between cells

#### border_color: (0,0,0)

Color of margins between cells, RGB value (in this case, we set it to black)

#### off_color: (50,50,50)

Default color of grid cells, which we've set to a dark grey here

#### on_color: (0,0,255)

Color of 'on' cells. We'll see what this means in a moment. Here, we've set it to blue.

#### radius: 2

Corner radius of cells. We've set it to 2 pixels, which will subtly round the corners of our cells.

#### caption: "My Awesome Game"

This sets the title of your game window. If not set, it will default to "PyGrid Project" so make sure to set this for that professional touch!

That's all you need to fully customize your pyGrid. Remember, all of these are optional, but if you want to set the caption for example, you'll have to set all of the values that show up before it. You can get around this by changing it after creating your grid. All attributes can be changed except for the first 5: width, height, cell_width, cell_height, border_weight, as these affect the size of the grid window.

    my_grid = pygrid.pyGrid(10, 20, 10, 10, 2)
    my_grid.border_color = (0,0,0)
    my_grid.off_color = (50,50,50)
    my_grid.on_color = (0,0,255)
    my_grid.radius = 2

In this version of pyGrid, the caption is only set when your grid is created, and cannot be changed through pyGrid. But you can just do it the old fashioned Pygame way, which is just as easy.

    pygame.display.set_caption("My Awesome Game")

Now that your window and grid options are set up, use the following line to draw the grid on the screen. You should only have to do this once:

    my_grid.draw()

And that's all it take to set up your pyGrid. After that, using the grid in your game is as easy as turning cells 'on' and 'off.' This is where the off_color and on_color come in. By default, all cells in your grid are off, which means they'll show up as your off_color (we set them as grey in the example above, or (50,50,50)), cells that are turned on will change to your on_color, which we've set to blue.

Turning cells on is as easy as providing the x,y coordinates of the cell you wish to turn on. (1 and 4 are just the random numbers we're using in this example, any number will work, as long as it fits in your grid)

    my_grid.on(1, 4)

...and turning a cell off is just as simple:

    my_grid.off(1, 4)

Of course, most games use more than just two colors. If you want a cell to be a different color than the rest of the cells you've turned on (like the red apple in the snake_example), you can provide a custom color, although you'll have to set a custom radius attribute as well. We set our default radius as 2, so we'll just leave it at 2, then we'll set our custom color to red:

    my_grid.on(1, 4, 2, (255,0,0))

The reason we have to set the radius as well as the color, is because even if an argument is optional, it still had to show up in its original order. The only way Python knows that we're trying to set the on_color attribute for the cell, is because it's the fourth argument. Radius comes before colour because if all you want to do is set a custom radius, and leave the color as the default, you won't have to retype the on_color. As an example, let's say we wanted one cell to have a radius of 3, we could just add on the radius argument:

    my_grid.on(1, 4, 3)

And that's it for the basics of pyGrid. With the above knowledge, you can start playing with pyGrid and plot points on the screen. When you start making games with pyGrid, you may want to be able to check if a cell is on or off, for example, to find out if you've bumped into a wall or crashed into a car, depending on what kind of game you're working on. This is the final function built in to pyGrid.

    my_grid.cell_state(1, 4)

The line above will return either a 0 or a 1. 0 means that cell is off, and a 1 means the cell is on. Of course this won't do much good on its own, and will be more useful in an if statement:

    if my_grid.cell_state(1, 4) == 1:
        print("You lose!")

This doesn't mean much now outside of the context of a game, but these make up the pieces that will get you started on your game development journey. Everything else exists between your keyboard and your imagination. For help getting started taking keyboard input, look at the examples included with pyGrid. You can also check out the Pygame tutorials, as input functions, as well as controlling the framerate of your game are all functions outside of pyGrid, and Pygame has done a pretty good job of simplifying those parts.

Future versions of pyGrid will take over some of those functions and simplify them even further.

### Other features that are planned or in the works:

* Placing text or images in a cell
* Drawing functions: lines, circles, etc.
* ability to draw grid at any location in pygame canvas, rather than filling entire window
* Java port for Android
