import pygame

from .math_helpers import *

def draw(surface, p1,p2, shading_function, section_length,section_offset):
    #Adapted Bresenham's line algorithm from
    #http://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
    x0,y0 = p1
    x1,y1 = p2

    dx = abs(x1 - x0)
    dy = abs(y1 - y0) 
    if x0 < x1: sx =  1
    else:       sx = -1
    if y0 < y1: sy =  1
    else:       sy = -1

    err = dx - dy

    while True:
        displacement = vec_length(vec_sub([x0,y0],p1)) + section_offset
        surface.set_at((x0,y0),shading_function( (displacement%section_length)/section_length ))
        if x0 == x1 and y0 == y1: break

        e2 = 2 * err
        if e2 > -dy:
            err = err - dy
            x0 = x0 + sx
        if e2 <  dx:
            err = err + dx
            y0 = y0 + sy
def aadraw(surface, p1,p2, shading_function, section_length,section_offset, blend):
    #Adapted Xiaolin Wu's line algorithm from
    #http://en.wikipedia.org/wiki/Xiaolin_Wu%27s_line_algorithm
    x0,y0 = p1
    x1,y1 = p2

    def plot(x,y, c):
        displacement = vec_length(vec_sub([x,y],p1)) + section_offset
        color2 = shading_function( (displacement%section_length)/section_length )
        if blend:
            color1 = surface.get_at((x,y))
            color = [rndint(color1[i]*(1-c) + c*color2[i]) for i in [0,1,2]]
        else:
            color = [rndint(c*color2[i]) for i in [0,1,2]]
        surface.set_at((x,y),color)
    def fpart(x): return x - int(x)
    def rfpart(x): return 1 - fpart(x)

    steep = abs(y1 - y0) > abs(x1 - x0)

    if steep:
        x0,y0 = y0,x0
        x1,y1 = y1,x1
    if x0 > x1:
        x0,x1 = x1,x0
        y0,y1 = y1,y0

    dx = x1 - x0
    dy = y1 - y0
    gradient = dy / dx

    #handle first endpoint
    xend = round(x0)
    yend = y0 + gradient * (xend - x0)
    xgap = rfpart(x0 + 0.5)
    xpxl1 = xend #this will be used in the main loop
    ypxl1 = int(yend)
    if steep:
        plot(ypxl1,   xpxl1, rfpart(yend) * xgap)
        plot(ypxl1+1, xpxl1,  fpart(yend) * xgap)
    else:
        plot(xpxl1, ypxl1,   rfpart(yend) * xgap)
        plot(xpxl1, ypxl1+1,  fpart(yend) * xgap)
    intery = yend + gradient # first y-intersection for the main loop

    #handle second endpoint
    xend = round(x1)
    yend = y1 + gradient * (xend - x1)
    xgap = fpart(x1 + 0.5)
    xpxl2 = xend #this will be used in the main loop
    ypxl2 = int(yend)
    if steep:
        plot(ypxl2  , xpxl2, rfpart(yend) * xgap)
        plot(ypxl2+1, xpxl2,  fpart(yend) * xgap)
    else:
        plot(xpxl2, ypxl2,  rfpart(yend) * xgap)
        plot(xpxl2, ypxl2+1, fpart(yend) * xgap)

    #main loop
    for x in range(xpxl1+1, xpxl2, 1):
    #for x from xpxl1 + 1 to [through] xpxl2 - 1 do
        if steep:
            plot(int(intery),   x, rfpart(intery))
            plot(int(intery)+1, x,  fpart(intery))
        else:
            plot(x, int(intery),  rfpart(intery))
            plot(x, int(intery)+1, fpart(intery))
        intery = intery + gradient
