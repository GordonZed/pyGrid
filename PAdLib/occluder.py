from .math_helpers import *

class Occluder(object):
    def __init__(self, ccw_point_list):
        self.points = list(ccw_point_list)
        self.numof_points = len(self.points)
        
        self._padlib_lines = []
        for i in range(self.numof_points):
            self._padlib_lines.append([
                self.points[ i                     ],
                self.points[(i+1)%self.numof_points]
            ])
        self._padlib_normals = []
        for l0,l1 in self._padlib_lines:
            delta = vec_sub(l1,l0)
            norm = [-delta[1],delta[0]]
            self._padlib_normals.append(vec_norm(norm))
        
        self.bounce = 1.0
        
    def set_bounce(self, bounce):
        self.bounce = bounce

    def intersects(self, point):
        #http://stackoverflow.com/questions/1119627/how-to-test-if-a-point-is-inside-of-a-convex-polygon-in-2d-integer-coordinates
        sign = 0
        for l0,l1 in self._padlib_lines:
            affine_segment = vec_sub(l1,l0)
            affine_point = vec_sub(point,l0)
            
            k = affine_segment[0]*affine_point[1] - affine_segment[1]*affine_point[0]
            if k == 0.0: return False
            if k > 0: k = 1
            else: k = -1

            if sign == 0: sign = k
            elif k != sign: return False
        return True
    def _padlib_collide(self, particle):
        if not self.intersects(particle.position): return
        
        projected_points = []
        for l0,l1 in self._padlib_lines:
            point = point_project_line(particle.position, l0,l1)
            projected_points.append([vec_length_sq(vec_sub(point,particle.position)),point])
        m = 99999999.0
        for dist,point in projected_points:
            if dist < m:
                m = dist
        for i in range(self.numof_points):
            if projected_points[i][0] == m:
                particle.position = projected_points[i][1]
                particle.velocity = vec_reflect(vec_scale(-self.bounce,particle.velocity),self._padlib_normals[i])
                return
