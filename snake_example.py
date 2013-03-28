import pygame
import pygrid
import random

# pySnake : Sample game using pyGrid
# Copyright 2013 Jordan Zanatta
# This is free software, released under The GNU Lesser General Public License, version 3.
# You are free to use, distribute, and modify pyGrid. If modification is your game,
# it is recommended that you read the GNU LGPL license: http://www.gnu.org/licenses/

grid = pygrid.pyGrid(40, 40, 10, 10, 2)

half_width = (grid.width / 2)
body = [(half_width, half_width + 1),
        (half_width, half_width),
        (half_width, half_width - 1)]

pygame.display.set_caption("pySnake - Score: 0")

grid.radius = 2

direction = 'up'
idle = True

food_x = random.randrange(1, grid.width - 1)
food_y = random.randrange(1, grid.height - 1)

ate_apple = False

clock = pygame.time.Clock()
done = False

score = 0.0
difficulty = 0.0

collide = False

grid.clear()
grid.draw()


for count in xrange(0, len(body)):
    grid.on(body[count][0], body[count][1])

grid.on(food_x, food_y, 2, (255, 0, 0))

while done == False:
    event = pygame.event.poll()

    if event.type == pygame.QUIT:
        done = True
    elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_ESCAPE:
            done = True
        if event.key == pygame.K_UP:
            if direction <> 'down':
                direction = 'up'
                idle = False
        elif event.key == pygame.K_RIGHT:
            if direction <> 'left':
                direction = 'right'
                idle = False
        elif event.key == pygame.K_DOWN:
            if direction <> 'up':
                direction = 'down'
                idle = False
        elif event.key == pygame.K_LEFT:
            if direction <> 'right':
                direction = 'left'
                idle = False


    difficulty = len(body) * .4
    ate_apple  = False

    if body[len(body) - 1][0] == food_x and body[len(body) - 1][1] == food_y:
        ate_apple = True

    if (direction == 'right') and (body[len(body) - 1][0] <> grid.width - 1) and not idle:
        x = body[len(body) - 1][0] + 1
        y = body[len(body) - 1][1]
        body.append((x, y))
    elif (direction == 'left') and (body[len(body) - 1][0] <> 0) and not idle:
        x = body[len(body) - 1][0] - 1
        y = body[len(body) - 1][1]
        body.append((x, y))
    elif (direction == 'up') and (body[len(body)-1][1] <> 0) and not idle:
        x = body[len(body) - 1][0]
        y = body[len(body) - 1][1] - 1
        body.append((x, y))
    elif (direction == 'down') and (body[len(body)-1][1] <> grid.height - 1) and not idle:
        x = body[len(body) - 1][0]
        y = body[len(body) - 1][1] + 1
        body.append((x, y))

    for num in xrange(0, len(body) - 2): #ignore last item (head)
        if body[len(body) - 1][0] == body[num][0] and body[len(body) - 1][1] == body[num][1]:
            collide = True

    if collide is True:
        done = True

    if idle <> True: #following line prevents flickering when idle
        grid.off(body[0][0], body[0][1])

        # del last segment unless apple is eaten, this effectively adds a body segment
        if ate_apple is False:
            grid.off(body[0][0], body[0][1])
            del body[0]

    if ate_apple is True:
        score = score + 10.0 + (5 * difficulty)
        grid.caption = "pySnake - Score: " + str(int(score))
        pygame.display.set_caption(grid.caption)
        grid.on(food_x, food_y)
        food_x = random.randrange(1, grid.width - 1)
        food_y = random.randrange(1, grid.height - 1)

        while grid.cell_state(food_x, food_y) == 1:
            # Make sure food doesn't spawn on the snake.
            food_x = random.randrange(1, grid.width - 1)
            food_y = random.randrange(1, grid.height - 1)
            
        grid.on(food_x, food_y, 2, (255, 0, 0))

    if (body[len(body) - 1][0] == grid.width - 1) and (direction == 'right'):
        idle = True
    if (body[len(body) - 1][0] == 0) and (direction == 'left'):
        idle = True
    if (body[len(body) - 1][1] == grid.height - 1) and (direction == 'down'):
        idle = True
    if (body[len(body) - 1][1] == 0) and (direction == 'up'):
        idle = True

    grid.on((body[len(body) - 1][0]), (body[len(body) - 1][1]))

    clock.tick(12 + difficulty)

if collide is True:
    done = False
    print("You hit your tail and died painfully. Final score: " + str(int(score)))
    print("Press ESC or close window to exit.")
    while done is False:
        event = pygame.event.poll()

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

pygame.quit()
