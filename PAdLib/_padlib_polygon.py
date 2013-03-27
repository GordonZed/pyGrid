import pygame
try:
    import numpy as np
    numpy_ok = True
except:
    numpy_ok = False

from .math_helpers import *

def trianglecolor(surface, c1,c2,c3, p1,p2,p3):
    if len(c1)==3: c1 = list(c1) + [255]
    if len(c2)==3: c2 = list(c2) + [255]
    if len(c3)==3: c3 = list(c3) + [255]

    if numpy_ok:
##        c1 = np.array(c1)
##        c2 = np.array(c2)
##        c3 = np.array(c3)
        def func(us,vs,ws, ins, bgra):
            bgra[:,:,2] = c1[0]*us + c2[0]*vs + c3[0]*ws
            bgra[:,:,1] = c1[1]*us + c2[1]*vs + c3[1]*ws
            bgra[:,:,0] = c1[2]*us + c2[2]*vs + c3[2]*ws
            bgra[:,:,3] = c1[3]*us + c2[3]*vs + c3[3]*ws
            bgra[:,:,3][np.logical_not(ins)] = 0
    else:
        func = lambda u,v,w: [
            c1[0]*u + c2[0]*v + c3[0]*w,
            c1[1]*u + c2[1]*v + c3[1]*w,
            c1[2]*u + c2[2]*v + c3[2]*w,
            c1[3]*u + c2[3]*v + c3[3]*w
        ]
    trianglecustom(surface, p1,p2,p3, func,numpy_ok)
def trianglecustom(surface, p1,p2,p3, shading_function,is_numpy):
    mins = [min([p1[0],p2[0],p3[0]]),min([p1[1],p2[1],p3[1]])]
    maxs = [max([p1[0],p2[0],p3[0]]),max([p1[1],p2[1],p3[1]])]

    size = ( ceil(maxs[0]-mins[0]), ceil(maxs[1]-mins[1]) )
    temp_surf = pygame.Surface(size).convert_alpha()

    #To find barycentric coordinates, we can treat the triangle's two vectors as
    #basis vectors a and b.  We then have to find a transformation from E to T
    #(E=[i,j] being the standard basis and T=[a,b] being the triangle's basis).
    #To do this, simply put a and b as column vectors of a 2x2 matrix and invert.
    #Multiplying by this matrix gives the barycentric coordinates.
    vec1 = vec_sub(p2,p1)
    vec2 = vec_sub(p3,p1)
    
    det = vec1[0]*vec2[1] - vec1[1]*vec2[0]
    if det == 0.0: return #Edge on triangle
    
    recip_det = 1.0 / det
    transformation_matrix = [
         vec2[1]*recip_det, -vec2[0]*recip_det,
        -vec1[1]*recip_det,  vec1[0]*recip_det
    ]
    #I derived this technique, and as far as I know it is original.

    start = [p1[0]-mins[0],p1[1]-mins[1]]
    if is_numpy:
        temp1 = pygame.surfarray.pixels2d(temp_surf)
        temp1.resize((size[0]*size[1],))
        temp2 = temp1.view(np.uint8)
        temp2.resize((size[1],size[0],4))
        arr_surf_bgra = temp2.transpose((1,0,2))

        arr_temp = np.empty((size[0],size[1],4))
        arr_in   = np.empty((size[0],size[1]),dtype=bool)

        #Setup the coordinates
        coords_x,coords_y = np.mgrid[0:size[0],0:size[1]]
        coords_x -= start[0]
        coords_y -= start[1]
        
        #Put the barycentric coordinates into arr_temp: (x,?,?,y) -> (x,b,c,y) -> (x,b,c,b+c) -> (a,b,c,b+c)
        arr_temp[:,:,1] = transformation_matrix[0]*coords_x + transformation_matrix[1]*coords_y #set b
        arr_temp[:,:,2] = transformation_matrix[2]*coords_x + transformation_matrix[3]*coords_y #set c
        arr_temp[:,:,3] = arr_temp[:,:,1] + arr_temp[:,:,2] #set b+c
        arr_temp[:,:,0] = 1.0 - arr_temp[:,:,3] #set a (which is 1.0-b-c which is 1.0-(b+c))

        #Put boolean whether the barycentric coordinates are inside
        np.logical_and(arr_temp[:,:,1]>=0.0,arr_temp[:,:,2]>=0.0, arr_in[:,:])
        np.logical_and(  arr_in[:,:  ],     arr_temp[:,:,3]<=1.0, arr_in[:,:])

        #Shade
        shading_function( arr_temp[:,:,0],arr_temp[:,:,1],arr_temp[:,:,2], arr_in, arr_surf_bgra )

        del temp1
        del temp2
        del arr_surf_bgra
    else:
        temp_surf.fill((0,0,0,0))
        for y in range(size[1]):
            py = y - start[1]
            for x in range(size[0]):
                p = [ x-start[0], py ]
                
                b = transformation_matrix[0]*p[0] + transformation_matrix[1]*p[1]
                if b < 0.0: continue
                c = transformation_matrix[2]*p[0] + transformation_matrix[3]*p[1]
                if c < 0.0: continue
                if b+c > 1.0: continue
                a = 1.0 - b - c

                temp_surf.set_at((x,y),list(map(rndint,shading_function(a,b,c))))

    surface.blit(temp_surf,mins)

    #The key algorithms here were originally from one of my other projects--one
    #of my CPU software rasterizers, and was originally more complicated to
    #handle perspective correction and whatnot.
def triangletexture(surface, texture, t1,t2,t3, p1,p2,p3, filter,should_clamp):
    w,h = texture.get_size()
    w1=w-1; h1=h-1
    def sample_nc(sx,sy): #nearest, with clamp
        return texture.get_at( (clamp(rndint(sx*w),0,w1),clamp(rndint(sy*h),0,h1)) )
    def sample_nr(sx,sy): #nearest, with repeat
        return texture.get_at( (rndint(sx*w)%w,rndint(sy*h)%h) )
    def sample_bc(sx,sy): #bilinear, with clamp
        sx*=w; sy*=h
        isx0=floor(sx); isy0=floor(sy); isx1=(isx0+1); isy1=(isy0+1) #can't use int(...); goes toward 0
        px=sx-isx0; py=sy-isy0; px1=1.0-px; py1=1.0-py
        isx0=clamp(isx0,0,w1); isx1=clamp(isx1,0,w1); isy0=clamp(isy0,0,h1); isy1=clamp(isy1,0,h1)
        c00 = texture.get_at( (isx0,isy0) )
        c10 = texture.get_at( (isx1,isy0) )
        c01 = texture.get_at( (isx0,isy1) )
        c11 = texture.get_at( (isx1,isy1) )
        return [rndint((c00[i]*px1+c10[i]*px)*py1+(c01[i]*px1+c11[i]*px)*py) for i in [0,1,2,3]]
    def sample_br(sx,sy): #bilinear, with repeat
        sx*=w; sy*=h
        isx0=floor(sx); isy0=floor(sy); isx1=(isx0+1); isy1=(isy0+1) #can't use int(...); goes toward 0
        px=sx-isx0; py=sy-isy0; px1=1.0-px; py1=1.0-py
        isx0=isx0%w; isx1=isx1%w; isy0=isy0%h; isy1=isy1%h
        c00 = texture.get_at( (isx0,isy0) )
        c10 = texture.get_at( (isx1,isy0) )
        c01 = texture.get_at( (isx0,isy1) )
        c11 = texture.get_at( (isx1,isy1) )
        return [rndint((c00[i]*px1+c10[i]*px)*py1+(c01[i]*px1+c11[i]*px)*py) for i in [0,1,2,3]]
    if filter:
        if should_clamp: sample_func = sample_bc
        else:            sample_func = sample_br
    else:
        if should_clamp: sample_func = sample_nc
        else:            sample_func = sample_nr
    def func(u,v,w):
        return sample_func(
            u*t1[0] + v*t2[0] + w*t3[0],
            u*t1[1] + v*t2[1] + w*t3[1]
        )
    trianglecustom(surface, p1,p2,p3, func,False)
def quadtexture(surface, texture, t1,t2,t3,t4, p1,p2,p3,p4, filter,clamp):
    triangletexture(surface, texture, t1,t2,t3, p1,p2,p3, filter,clamp)
    triangletexture(surface, texture, t1,t3,t4, p1,p3,p4, filter,clamp)


























