import pygame

def draw(surface, color, rect, radius, width):
    if color[0] + color[1] + color[2] == 0:
        colorkey = (1,1,1)
    else:
        colorkey = (0,0,0)

    surf_temp = pygame.Surface((rect[2],rect[3]))
    surf_temp.fill(colorkey)

    pygame.draw.rect(surf_temp,color,(0,radius,rect[2],rect[3]-2*radius),0)
    pygame.draw.rect(surf_temp,color,(radius,0,rect[2]-2*radius,rect[3]),0)

    for point in [
        [radius,radius],
        [rect[2]-radius,radius],
        [radius,rect[3]-radius],
        [rect[2]-radius,rect[3]-radius]
    ]:
        pygame.draw.circle(surf_temp,color,point,radius,0)

    if width != 0:
        draw(surf_temp,colorkey,(width,width,rect[2]-2*width,rect[3]-2*width),radius-width,0)
    
    surf_temp.set_colorkey(colorkey)
    surface.blit(surf_temp,(rect[0],rect[1]))
