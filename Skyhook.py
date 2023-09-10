#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#pip install pygame
#pip install PyOpenGL


# In[1]:


import pygame
import OpenGL
import OpenGL_accelerate
import numpy as np
import random
import math
from enum import Enum


# In[2]:


from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *


# In[3]:


class Vertex:
    
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.coordinate = ((x, y, z))
        


# In[4]:


class Cargo(Vertex):
    
    def __init__(self, x, y, z, hook=None):
        super().__init__(x, y, z)
        
        self.speed = 0
        self.direction = 0
        self.hook = hook
        
    def move(self):
        
        if self.hook is None:
            self.x += math.cos(self.direction) * self.speed
            self.y += math.sin(self.direction) * self.speed
            self.coordinate = ((self.x, self.y, self.z))
            
        else:
            self.x = self.hook.hookx
            self.y = self.hook.hooky
            self.speed = math.sin(self.hook.w) * self.hook.r
            self.direction = self.hook.f+math.pi/2
            self.coordinate = ((self.x, self.y, self.z))


# In[5]:


class Hook(Vertex):
    
    def __init__(self, x, y, z, r, w):
        super().__init__(x, y, z)
    
        self.w = w
        self.r = r
        self.f = 0
        self.cargo = None
        self.released = False
        
    def rotate(self):
        
        self.f += self.w
        self.hookx = self.x + math.cos(self.f)*self.r
        self.hooky = self.y + math.sin(self.f)*self.r
        self.hook_coordinate = ((self.hookx, self.hooky, self.z))
        if self.catch_cargo(game.cargo):
            #self.x += self.cargo.x
            #self.y += self.cargo.y
            return True
        
    def catch_cargo(self, cargo):
        distance = np.linalg.norm((self.hookx-cargo.x, self.hooky-cargo.y, 0))
        # distance, or how easy it is to catch the cargo
        if distance < 0.5 and not self.released and self.cargo is None:
        
            self.cargo = cargo
            cargo.hook = self
            return True

    def release_cargo(self):
        if not self.cargo == None:
            self.cargo.hook = None
            self.cargo = None
            self.released = True
        


# In[6]:


class Game:
    
    def __init__(self, cargo):
        self.hooks = []
        self.cargo = cargo
        self.cargo_loc = 0
    def play_step(self):
        for i, hook in enumerate(self.hooks):
            if hook.rotate():
                old = self.cargo_loc
                self.cargo_loc = i
                print(old, self.cargo_loc)
                self.hooks[old].released = False
                
            
                
        cargo.move()


# In[7]:


cargo = Cargo(-4, 2, 0)
cargo.speed = 0.03


# In[8]:


game = Game(cargo)


# In[9]:


hook = Hook(-4,2,0,2,0.01)
hook2 = Hook(4,3,0,1,0.02)
hook3 = Hook(0, -2, 0, 2, 0.04)


# In[10]:


game.hooks.append(hook)
game.hooks.append(hook2)
game.hooks.append(hook3)


# In[11]:


def main():
    pygame.init()
    display = (1800,1000)
    #width, length
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption("Skyhook")
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    glTranslatef(0.0,0.0, -12)
    #sağ, sol; yukarı, aşağı; ileri, geri
    #glRotatef(90, 1, 0, 0)

    
    while True:
        release = False    
        #glTranslatef(0,0, -12)
        #glRotatef(1, 0, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            if event.type == pygame.KEYDOWN:
                
    
                if event.key == pygame.K_SPACE:
                    #hook.release_cargo()
                    release = True
                if event.key ==pygame.K_UP:
                    cargo.__init__(-4, 2, 0)
                    cargo.speed = 0.03
                    game.hooks[0].released = False

        glPointSize(3)
        glColor3f(255, 255, 255)
        
        game.play_step()
        glBegin(GL_LINES)
        #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        for hooke in game.hooks:
        
            glVertex3fv(hooke.coordinate)
            glVertex3fv(hooke.hook_coordinate)
            if release:
                hooke.release_cargo()
        
        glEnd()
        
        glPointSize(10)
        glColor3f(0, 255, 255)
        glBegin(GL_POINTS)
        #glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        
        glVertex3fv(game.cargo.coordinate)
    
    
        glEnd()

        pygame.display.flip()
        pygame.time.wait(20)
        #glEnd()


# In[ ]:





# In[12]:


main()


# In[ ]:




