'''
Created on Apr 2, 2009

@author: hyh
'''
import pygame
from pygame.locals import *

from parameter import *

import sys
import random
# import Image
from PIL import Image

from numpy import matrix

from ball import *
from physics_engine import *
from parameter import *
from vector_utils import *
from controller import *

try:
  from OpenGL.GLUT import *
  from OpenGL.GL import *
  from OpenGL.GLU import *
except:
  print '''
ERROR: PyOpenGL not installed properly.  
        '''
  sys.exit()



class Controller:
    
    
    oldx = 0
    oldy = 0
    oldz = 0
        
    width = 1000
    height = 1000
        
    drag_mode = 0
        
    rotate_radius = LENGTH_X / 2
        
    stick_direction = [0,0,1]
    old_stick_direction = [0,0,1]
    
    def __init__(self, scene):
        self.scene = scene
    
    
    def process_input(self):
        
        scale_factor = 1.2
            
        e = pygame.event.poll()
        if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
            return 0
        if e.type == KEYDOWN and e.key == K_SPACE:
            mat = glGetFloat(GL_MODELVIEW_MATRIX)
            
            A = matrix(mat)
            B = A.I

            x = B[0, 0] * self.stick_direction[0] + B[1, 0] * self.stick_direction[1] + B[2, 0] * self.stick_direction[2] + B[3, 0]
            y = B[0, 1] * self.stick_direction[0] + B[1, 1] * self.stick_direction[1] + B[2, 1] * self.stick_direction[2] + B[3, 1]
            z = B[0, 2] * self.stick_direction[0] + B[1, 2] * self.stick_direction[1] + B[2, 2] * self.stick_direction[2] + B[3, 2]                
            
            self.scene.balls[0].velocity = [x, y, z]
            normalize(self.scene.balls[0].velocity)
        
            scale(self.scene.balls[0].velocity, - 0.5)

            
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                self.drag_mode = 1
                #self.scene.bounce_sound.play()
                #print "bang!"
                
            if e.button == 3:
                self.drag_mode = 2
            if e.button == 4:
                self.rotate_radius *= scale_factor
                glScalef(scale_factor, scale_factor, scale_factor)
            if e.button == 5:
                self.rotate_radius /= scale_factor
                glScalef(1 / scale_factor, 1 / scale_factor, 1 / scale_factor)
            self.oldx = - 1
            self.oldy = - 1
            self.oldz = - 1    
        elif e.type == MOUSEBUTTONUP:
            self.drag_mode = 0
            self.oldx = - 1
            self.oldy = - 1
            self.oldz = - 1    

            
        if e.type == VIDEORESIZE:
#             win = pygame.display.set_mode(e.size, RESIZABLE)
            pass

        if e.type == MOUSEMOTION:
            (x, y) = pygame.mouse.get_pos()
            self.drag(x, y)
            
        return 1
    
    
    def drag(self, x, y):
        ''' mouse left button for rotating scene, mouse right button for rotating stick '''
        if self.drag_mode == 1:
            self.rotate_scene(x, y)
        elif self.drag_mode == 2:
            self.rotate_stick(x, y)
        
    def rotate_stick(self, x, y):
        ''' not actually rotate the stick, but collect stick_direction for redrawing the stick'''
        x = (x - self.width/2)*1.0/self.width*LENGTH_X
        y = (-y + self.height/2)*1.0/self.height*LENGTH_X
        if (self.rotate_radius)**2 - x*x - y*y<0:
            return
        z = ((self.rotate_radius)**2 - x*x - y*y)**0.5
            
        if self.oldx==-1 or self.oldy==-1:
            self.oldx = x
            self.oldy = y
            self.oldz = z
            return
            
            
        self.stick_direction = [x,y,z]
        self.stick_direction = [self.oldx, self.oldy, self.oldz]
            
        self.oldx = x
        self.oldy = y
        self.oldz = z
        

            
            
            
    def rotate_scene(self, x, y):
        ''' rotate the scene by grasping a imaginary sphere '''        
            
        x = (x - self.width/2)*1.0/self.width*LENGTH_X
        y = (-y + self.height/2)*1.0/self.height*LENGTH_X
        if (self.rotate_radius)**2 - x*x - y*y<0:
            return
        z = ((self.rotate_radius)**2 - x*x - y*y)**0.5
            
        if self.oldx==-1 or self.oldy==-1:
            self.oldx = x
            self.oldy = y
            self.oldz = z
            return
            
            
        position = [x,y,z]
        old_position = [self.oldx, self.oldy, self.oldz]
        
        a = cos(position, old_position)
        if a>1:a=1
        if a<-1:a=-1
        angle = math.acos(a)*360/(2*math.pi)
        
        rotate_axis = cross_product (old_position, position) 
        normalize(rotate_axis)
            
        self.oldx = x
        self.oldy = y
        self.oldz = z
            
        glMatrixMode (GL_MODELVIEW)      
        
        ''' first rotate the scene, then multiply the previous saved matrix '''
        mat = glGetFloat(GL_MODELVIEW_MATRIX)
    
        glLoadIdentity()
        glRotatef(angle, rotate_axis[0], rotate_axis[1], rotate_axis[2])
        glMultMatrixf(mat)
        
        ''' reset the stick direction '''
        self.stick_direction = [0,0,1]
        self.old_stick_direction = [0,0,1]
        
        #glMatrixMode (GL_PROJECTION)
        #gluLookAt(0, 0, 5, 0, 0, -1, 0, 1, 0)
        #glLoadIdentity()
        #glOrtho (-2, 2, -2, 2, 0.1, 50.0)
        #glFrustum (-2, 2, -2, 2, 0.1, 50.0)
        #gluPerspective(45, 1, 0.1, 10)
        #glMatrixMode (GL_MODELVIEW)
            
            
#        if self.oldx==-1 or self.oldy==-1:
#            self.oldx = x
#            self.oldy = y
#            return
#        
#        d = x - self.oldx
#        if d > 0:
#            spin_horizontal_direction = 1
#        else:
#            spin_horizontal_direction = -1
#        spin_horizontal_angle = math.fabs(d)*0.5
#
#        d = y - self.oldy
#        if d > 0:
#            spin_vertical_direction = 1
#        else:
#            spin_vertical_direction = -1
#        spin_vertical_angle = math.fabs(d)*0.5
#        
#        self.oldx = x
#        self.oldy = y           
#                    
#        glMatrixMode (GL_MODELVIEW)
#        
#        mat = glGetFloat(GL_MODELVIEW_MATRIX)
#        glLoadIdentity()
#        glRotatef(spin_horizontal_angle, 0, spin_horizontal_direction, 0)
#        glRotatef(spin_vertical_angle, spin_vertical_direction, 0, 0)
#        glMultMatrixf(mat)
    