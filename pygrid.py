import pygame
import PAdLib as padlib
pygame.init()

                                        ###
####### ### ### ####### ####### ### #######
### ### ### ### ### ### ###     ### ### ### ###
####### ####### ####### ###     ### ####### ###
###         ###     ###

''' grid based game engine for Python '''

# Copyright 2013 Jordan Zanatta
# This is free software, released under The GNU Lesser General Public License,
# version 3.
# You are free to use, distribute, and modify pyGrid. If modification is your
# game, it is recommended that you read the GNU LGPL license:
#   http://www.gnu.org/licenses/
#
# pyGrid uses the Pygame Advanced Graphics Library,
# by Ian Mallett: www.geometrian.com


class pyGrid:

    def __init__(self, x_cells=13, y_cells=10, cell_w=25, cell_h=25,
                 border_px=4, border_rgb=(204, 212, 163),
                 off=(191, 199, 149), on=(40, 50, 40),
                 radius=0, caption="pyGrid Project"):

        self.width  = x_cells
        self.height = y_cells

        self.border_weight = border_px
        self.border_color  = border_rgb

        self.cell_width  = cell_w
        self.cell_height = cell_h

        self.off_color = off
        self.on_color  = on

        self.radius = radius

        self.caption = caption

        pygame.display.set_caption(self.caption)

        self.screen_width  = (self.width * self.cell_width) \
                                + (self.width * self.border_weight) \
                                + self.border_weight
        self.screen_height = (self.height * self.cell_height) \
                                + (self.height * self.border_weight) \
                                + self.border_weight
        self.screen_size   = (self.screen_width, self.screen_height)
        self.screen        = pygame.display.set_mode(self.screen_size)

        self.cells = [] # Cells will be stores as a nested list
        # Nested lists are cumbersome, consider a list of tuples as implemented
        # in the snake example

        for y in xrange(0, self.height):
            self.cells.append([]) # insert y list in cells list, 'height' times
            for x in xrange(0, self.width):
                self.cells[y].append(0)

    def clear(self):
        self.screen.fill(self.border_color)

    def draw(self):
        self.screen.fill(self.border_color)
        for y in xrange(0, self.height):
            if y == 0:
                y_pos = self.border_weight
            else:
                y_pos = (self.border_weight * (y + 1)) + (self.cell_height * y)

            for x in xrange(0, self.width):

                if x == 0:
                    x_pos = self.border_weight
                else:
                    x_pos = (self.border_weight * (x + 1)) + (self.cell_width * x)

                if self.cells[y][x] > 0:
                    cell_state_color = self.on_color
                else:
                    cell_state_color = self.off_color

                if self.radius == 0:
                    pygame.draw.rect(self.screen, cell_state_color,
                    [x_pos, y_pos, self.cell_width, self.cell_height])
                else:
                    padlib.draw.rrect(self.screen, cell_state_color,
                    (x_pos, y_pos, self.cell_width, self.cell_height), self.radius, 0)

            # Flip screen and whatnot
            pygame.display.flip()

    def on(self, x, y, radius=None, color=()):
        if color == ():
            on_color = self.on_color
        else:
            on_color = color

        self.cells[y][x] = 1

        if y == 0:
            y_pos = self.border_weight
        else:
            y_pos = (self.border_weight * y) + (self.cell_height * y) + self.border_weight

        if x == 0:
            x_pos = self.border_weight
        else:
            x_pos = (self.border_weight * x) + (self.cell_width * x) + self.border_weight

        if radius == None:
            radius = self.radius

        if radius == 0:
            pygame.draw.rect(self.screen, on_color,
            [x_pos, y_pos, self.cell_width, self.cell_height])
        else:
            padlib.draw.rrect(self.screen, on_color,
            (x_pos, y_pos, self.cell_width, self.cell_height), radius, 0)

        # Flip screen and whatnot
        pygame.display.flip()

    def off(self, x, y):
        self.cells[y][x] = 0

        if y == 0:
            y_pos = self.border_weight
        else:
            y_pos = (self.border_weight * y) + (self.cell_height * y) + self.border_weight

        if x == 0:
            x_pos = self.border_weight
        else:
            x_pos = (self.border_weight * x) + (self.cell_width * x) + self.border_weight

        if self.radius == 0:
            pygame.draw.rect(self.screen, self.off_color,
            [x_pos, y_pos, self.cell_width, self.cell_height])
        else:
            padlib.draw.rrect(self.screen, self.off_color,
            (x_pos, y_pos, self.cell_width, self.cell_height), self.radius, 0)

        # Flip screen and whatnot
        pygame.display.flip()

    def cell_state(self, x, y):
        return self.cells[y][x]
