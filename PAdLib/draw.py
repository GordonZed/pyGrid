from . import _padlib_bezier
from . import _padlib_linepattern
from . import _padlib_rrect
from . import _padlib_spline
from . import _padlib_polygon

def bezier(surface, color, controlpointslist, steps, width=1):
    _padlib_bezier.draw(surface, color, controlpointslist, steps, False, width, False)
def aabezier(surface, color, controlpointslist, steps, blend=True):
    _padlib_bezier.draw(surface, color, controlpointslist, steps, True, 1, blend)

def spline(surface, color, closed, pointslist, steps, t=0.0,b=0.0,c=0.0, width=1):
    _padlib_spline.draw(surface, color, closed, pointslist, steps, t,b,c, False, width, False)
def aaspline(surface, color, closed, pointslist, steps, t=0.0,b=0.0,c=0.0, blend=True):
    _padlib_spline.draw(surface, color, closed, pointslist, steps, t,b,c, True, 1, blend)
    
def   linepattern(surface, p1,p2, shading_function, section_length,section_offset=0            ):
    _padlib_linepattern.draw(surface, p1,p2, shading_function, section_length,section_offset)
def aalinepattern(surface, p1,p2, shading_function, section_length,section_offset=0, blend=True):
    _padlib_linepattern.aadraw(surface, p1,p2, shading_function, section_length,section_offset, blend)

def rrect(surface, color, rect, radius, width=0):
    _padlib_rrect.draw(surface, color, rect, radius, width)

def trianglecolor(surface, c1,c2,c3, p1,p2,p3):
    _padlib_polygon.trianglecolor(surface, c1,c2,c3, p1,p2,p3)
def trianglecustom(surface, p1,p2,p3, shading_function,is_numpy=False):
    _padlib_polygon.trianglecustom(surface, p1,p2,p3, shading_function,is_numpy)
def triangletexture(surface, texture, t1,t2,t3, p1,p2,p3, filter=False,clamp=False):
    _padlib_polygon.triangletexture(surface, texture, t1,t2,t3, p1,p2,p3, filter,clamp)
def quadtexture(surface, texture, t1,t2,t3,t4, p1,p2,p3,p4, filter=False,clamp=False):
    _padlib_polygon.quadtexture(surface, texture, t1,t2,t3,t4, p1,p2,p3,p4, filter,clamp)
