import pygame

from .math_helpers import *

def draw(surface, color, closed, pointslist, steps, t,b,c, aa, width, blend):
    #Kochanek-Bartels spline implementation, written long ago and updated.
    t_inc = 1.0/float(steps)

    #This allows us to draw through all visible control points (normal Kochanek-Bartels
    #splines do not draw through their last endpoints).
    if closed:
        pointslist = [pointslist[-2],pointslist[-1]] + pointslist + [pointslist[0],pointslist[1]]
    else:
        pointslist = [pointslist[0]] + pointslist + [pointslist[-1]]

    cona = (1-t)*(1+b)*(1-c)*0.5
    conb = (1-t)*(1-b)*(1+c)*0.5
    conc = (1-t)*(1+b)*(1+c)*0.5
    cond = (1-t)*(1-b)*(1-c)*0.5

    tans = []
    tand = []
    for x in range(len(pointslist)-2):
        tans.append([])
        tand.append([])
    i = 1
    while i < len(pointslist)-1:
        pa = pointslist[i-1]
        pb = pointslist[i  ]
        pc = pointslist[i+1]
        x1 = pb[0] - pa[0]
        y1 = pb[1] - pa[1]
        x2 = pc[0] - pb[0]
        y2 = pc[1] - pb[1]
        tans[i-1] = (cona*x1+conb*x2, cona*y1+conb*y2)
        tand[i-1] = (conc*x1+cond*x2, conc*y1+cond*y2)
        i += 1

    for i in range(1,len(pointslist)-2,1):
        p0 = pointslist[i  ]
        p1 = pointslist[i+1]
        m0 = tand[i-1]
        m1 = tans[i  ]
        
        #draw curve from p0 to p1
        points = [(p0[0],p0[1])]
        t_iter = t_inc
        while t_iter < 1.0:
            h00 = ( 2*(t_iter*t_iter*t_iter)) - ( 3*(t_iter*t_iter)) + 1
            h10 = ( 1*(t_iter*t_iter*t_iter)) - ( 2*(t_iter*t_iter)) + t_iter
            h01 = (-2*(t_iter*t_iter*t_iter)) + ( 3*(t_iter*t_iter))
            h11 = ( 1*(t_iter*t_iter*t_iter)) - ( 1*(t_iter*t_iter))
            px = h00*p0[0] + h10*m0[0] + h01*p1[0] + h11*m1[0]
            py = h00*p0[1] + h10*m0[1] + h01*p1[1] + h11*m1[1]
            points.append((px,py))
            t_iter += t_inc
        points.append((p1[0],p1[1]))
        
        if aa:
            #This function can take floating-point values for endpoints.
            pygame.draw.aalines(surface,color,False,points,blend)
        else:
            points = [list(map(rndint,p)) for p in points]
            pygame.draw.lines(surface,color,False,points,width)
