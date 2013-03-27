from .math_helpers import *

import random

class Particle(object):
    def __init__(self, particle_system, position,velocity, life,colors):
        self.particle_system = particle_system
        
        self.position = list(position)
        self.velocity = list(velocity)

        self.time = 0.0
        self.life = life

        self.colors = list(colors)
        self._padlib_num_colors = len(self.colors)
        self._padlib_color_needs_update = True
        
    def get_color(self):
        if self._padlib_color_needs_update:
            part = self.time / self.life
            part *= self._padlib_num_colors
            index = int(part)
            if index >= self._padlib_num_colors:
                index = self._padlib_num_colors - 1

            color1 = self.colors[index]
            if index + 1 >= self._padlib_num_colors:
                color2 = color1
            else:
                color2 = self.colors[index+1]

            delta = [color2[i]-color1[i] for i in [0,1,2]]
            
            part = part - int(part)
            self.color = [rndint(color1[i]+part*delta[i]) for i in [0,1,2]]
            
            self._padlib_color_needs_update = False

        return self.color
    
    def update(self, dt, accel):
        self.velocity[0] += accel[0]*dt
        self.velocity[1] += accel[1]*dt
        
        self.position[0] += self.velocity[0]*dt
        self.position[1] += self.velocity[1]*dt
        
        self.time += dt
        self._padlib_color_needs_update = True
        
    def draw(self, surface):
        surface.set_at( (rndint(self.position[0]),rndint(self.position[1])), self.get_color() )
        
class Emitter(object):
    def __init__(self):
        self.position = [0.0,0.0]
        
        self.density = 1 #in new particles created / second on average
        self.angle = 0.0 #in radians
        self.spread = 0.0 #in radians
        self.speed = [0.0,0.0] #in pixels / second
        self.life = [1.0,1.0] #in seconds
        self.colors = [(255,255,255)]
    
    def set_position(self, emitter_position):
        self.position = list(emitter_position)

    #Average density per second
    def set_density(self, particles_per_second):
        self.density = particles_per_second
    #degrees_spread is the entire spread of the particles
    def set_angle(self, degrees_angle,degrees_spread=0):
        self.angle = radians(degrees_angle)
        self.spread = radians(degrees_spread)
    def set_speed(self, speed_range):
        self.speed = list(speed_range)
    def set_life(self, life_range):
        self.life = list(life_range)
    def set_colors(self, colors):
        self.colors = list(colors)

    #Function used to get a new random angle.  Can be overridden by user.
    def get_angle(self, center_rad,spread_rad):
        #Note that doesn't work nicely for omnidirectional sources
        #return center_rad + random.triangular(-0.5,0.5,0.0)*self.spread
        #Good, but too evenly spread in some cases
        return center_rad + (random.random()-0.5)*spread_rad

    def _padlib_update(self, parent, dt):
        for i in range(self.density):
            if random.random() < dt:
                angle = self.get_angle(self.angle,self.spread)
                
                speed = random.uniform(self.speed[0],self.speed[1])
                vel = [speed*cos(angle),speed*sin(angle)]
                
                r = random.random() * dt
                pos = [self.position[i] + r*vel[i] for i in [0,1]]
                
                life = random.uniform(self.life[0],self.life[1])
                
                parent.particles.append(Particle(parent, pos,vel, life,self.colors))

class ParticleSystem(object):
    def __init__(self):
        self.particles = []
        self.emitters = {}
        
        self.accel = [0.0,0.0]
        self.occluders = []
        
    def add_emitter(self, emitter,name=-1):
        if name == -1: name = "_padlib_"+str(hash(emitter))
        self.emitters[name] = emitter

    def set_particle_acceleration(self, acceleration):
        self.accel = list(acceleration)
    def set_particle_occluders(self, occluders):
        self.occluders = list(occluders)
        
    def update(self, dt):
        for emitter in self.emitters.values():
            emitter._padlib_update(self,dt)
            
        for particle in self.particles:
            particle.update(dt,self.accel)
            if particle.time > particle.life:
                self.particles.remove(particle)
                continue
            for occluder in self.occluders:
                occluder._padlib_collide(particle)
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)
