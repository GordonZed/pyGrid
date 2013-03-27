import pygame
from pygame.locals import *

from .math_helpers import *

class Shadow(object):
    def __init__(self):
        self.position = [0,0]
        self.occluders = []

        self.set_radius(100.0)

    def set_light_position(self, position):
        self.position = list(position)
        self._padlib_needs_update = True

    def set_radius(self, radius):
        self.radius = radius
        self.mask = pygame.Surface([rndint(self.radius)*2]*2)
        self._padlib_needs_update = True

    def set_occluders(self, occluders):
        self.occluders = list(occluders)
        self._padlib_needs_update = True

    def get_mask_and_position(self, fill_occluders):
        #Functions by considering all obstacles in light space.  Projects each
        #back face onto the edges of self.surf.  Fails when inside obstacle, so
        #check for that specifically.

        #Basic idea is to start with an unoccluded light (a white circle), then
        #draw black polygons from each back face out to infinity.  Since we only
        #care about shading the area of the polygons within self.surf, we don't
        #actually draw to infinity; we clip to the edges of self.surf.

        if self._padlib_needs_update:
            self.mask.fill((0,0,0))

            inside = False
            for occluder in self.occluders:
                if occluder.intersects(self.position):
                    inside = True
                    break

            if not inside:
                pygame.draw.circle(self.mask,(255,255,255),[rndint(self.radius)]*2,rndint(self.radius),0)
                
                center = [self.radius,self.radius]
                for occluder in self.occluders:
                    for i in range(occluder.numof_points):
                        l0 = occluder.points[i]
                        delta1 = vec_sub(l0,self.position)
                        if vec_dot(delta1,occluder._padlib_normals[i]) > 0.0: #backface
                            l1 = occluder.points[(i+1)%occluder.numof_points]
                            delta2 = vec_sub(l1,self.position)

                            p1 = vec_add(center,delta1)
                            p2 = vec_add(center,delta2)
                            def ray_box(ray):
                                #Cast the ray until it hits the box's edge, knowing that it starts at "center"
                                #The worst case is when a back face produces a right triangle.  The diagonal of
                                #this triangle must be outside the radius, so we instead cast all rays to a
                                #box not of width 2*self.radius, but 2*sqrt(2)*self.radius + epsilon.
                                length = self.radius / max([abs(ray[0]),abs(ray[1])])
                                return vec_scale(length,ray)

                            p3 = vec_add(center,ray_box(delta1))
                            p4 = vec_add(center,ray_box(delta2))

                            #To make the polygon not take a shortcut across the light surface (and therefore not
                            #shadow enough, walk counterclockwise around until we reach the same edge.
                            poly = [p2,p1,list(p3)]
                            def get_side(point): #arranged counterclockwise
                                if abs(point[0]                      ) < 1.0: return 0 #left
                                if abs(point[0]-self.mask.get_width()) < 1.0: return 2 #right
                                if abs(point[1]                      ) < 1.0: return 3 #top
                                return                                               1 #bottom
                            s3 = get_side(p3)
                            s4 = get_side(p4)
                            while True:
                                poly.append(list(p3))
                                if s3 == s4:
                                    break
                                else:
                                    if   s3 == 0: p3 = [0.0,self.mask.get_height()]
                                    elif s3 == 1: p3 = self.mask.get_size()
                                    elif s3 == 2: p3 = [self.mask.get_width(),0.0]
                                    else:         p3 = [0.0,0.0]
                                    s3 = (s3+1) % 4
                            poly.append(p4)
                            
                            pygame.draw.polygon(
                                self.mask,
                                (0,0,0),
                                list(map(lambda p:(rndint(p[0]),rndint(p[1])),poly)),
                                0
                            )
                    if fill_occluders:
                        pygame.draw.polygon(
                            self.mask,
                            (0,0,0),
                            [[rndint(point[i]-self.position[i]+self.radius) for i in [0,1]] for point in occluder.points],
                            0
                        )
            self._padlib_needs_update = False
        return self.mask, (rndint(self.position[0]-self.radius),rndint(self.position[1]-self.radius))
