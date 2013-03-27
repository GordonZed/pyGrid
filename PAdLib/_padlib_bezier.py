import pygame

from .math_helpers import *

def draw(surface, color, controlpointslist, steps, aa, width, blend):
    #Algorithm derived from geometric animations on
    #http://en.wikipedia.org/wiki/Bezier_curve
    
    points = []
    
    def draw_curve(controlpointslist):
        l = len(controlpointslist)
        
        def lerp(p1,p2):
            return vec_add(
                vec_scale(1.0-t,p1),
                vec_scale(    t,p2)
            )
        if l == 2:
            points.append(lerp(*controlpointslist))
        else:
            controlpointslist2 = []
            for i in range(l-1):
                controlpointslist2.append(lerp(
                    controlpointslist[i],
                    controlpointslist[i+1]
                ))
            draw_curve(controlpointslist2)
                
    for i in range(steps):
        t = float(i) / float(steps-1)
        draw_curve(controlpointslist)

    if aa:
        #This function can take floating-point values for endpoints.
        pygame.draw.aalines(surface,color,False,points,blend)
    else:
        points = [list(map(rndint,p)) for p in points]
        pygame.draw.lines(surface,color,False,points,width)
