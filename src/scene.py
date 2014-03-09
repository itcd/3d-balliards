#!/usr/bin/python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

import os,pygame
from pygame.locals import *

if not pygame.mixer: print 'Warning, sound disabled'


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
		

class Scene:

	balls = []
		
	
		

	#  Main Loop
	#  Open window with initial window size, title bar, 
	#  RGBA display mode, and handle input events.
	def __init__(self):
		''' create windows and set up callback function '''
		
		
		

		
		pygame.init()
		pygame.display.set_mode((1000,1000), OPENGL|DOUBLEBUF)
		glEnable(GL_DEPTH_TEST)
		#glutSolidSphere(1,50,50)
		
		self.init()
		#pygame.mixer.pre_init(buffersize=256)
		#pygame.mixer.init(buffer = 256)
		
		self.controller = Controller(self)
		self.bounce_sound = self.load_sound('bounce.wav')
		self.yay_sound = self.load_sound('yay.wav')
		self.oops_sound = self.load_sound('oops.wav')
		
	def run(self):
		
		while 1:
			#check for quit'n events
			if not self.controller.process_input():
				break
				
			self.reshape(1000, 1000)
			self.display()
			
			pygame.display.flip()
			pygame.time.wait(10)
			
		

	def make_balls(self, num):
		''' make all the balls and init the physics engine '''
		self.physics_engine = PhysicsEngine(self)
		n = 0
		while n<num:
			r = random.random()
			g = random.random()
			b = random.random()

			x = MIN_X + R + random.random()*(MAX_X - MIN_X - 2*R)
			y = MIN_Y + R + random.random()*(MAX_Y - MIN_Y - 2*R)
			z = MIN_Z + R + random.random()*(MAX_Z - MIN_Z - 2*R)

#			vx = random.random()*0.1
#			vy = random.random()*0.1
#			vz = random.random()*0.1
			vx = 0
			vy = 0
			vz = 0

			new_ball = Ball([x,y,z],[vx,vy,vz],[r,g,b,1],1)

			collided = 0
			for ball in self.balls:
				if self.physics_engine.collide(new_ball, ball):
					collided = 1
					break
				
			if not collided:
				self.balls.append(new_ball)
				n = n + 1
								

	def make_ball(self, color, position, number=1):
		''' make one ball '''
		self.balls.append(Ball(position,[0,0,0],color, number))
				

	def display_hole(self, position):
		
		glMaterialfv(GL_FRONT, GL_AMBIENT, [0,0,0,0])
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0,0,0,0])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [0,0,0,0])
		#glMaterialf(GL_FRONT, GL_SHININESS, 128)
		
		quadric = gluNewQuadric()
		
		glPushMatrix()
		glTranslatef(position[0], position[1], position[2])
		gluSphere(quadric, 1.2*R, 50, 50)	
		glPopMatrix()
		
	def display_ball(self, ball):
		
		glMaterialfv(GL_FRONT, GL_DIFFUSE, ball.color)
		glMaterialfv(GL_FRONT, GL_SPECULAR, ball.color)
		glMaterialf(GL_FRONT, GL_SHININESS, 128)
		
		
		glPushMatrix()
		glTranslatef(ball.position[0], ball.position[1], ball.position[2])
		#glutSolidSphere(R, 50, 50)
		quadric = gluNewQuadric()
		gluSphere(quadric, R, 50, 50,)
		
		glPopMatrix()
				
	def display_stick(self):
			
		light_ambient =  [1.0, 1.0, 1.0, 1.0]
		light_diffuse =  [1.0, 1.0, 1.0, 1.0]
		light_specular = [1.0, 1.0, 1.0, 1.0]
			
		ball = self.balls[0]			
			
		position = self.controller.stick_direction
		old_position = self.controller.old_stick_direction
		angle = math.acos(cos(position, old_position))*360/(2*math.pi)
			
		rotate_axis = cross_product (old_position, position) 
		normalize(rotate_axis)
			
		glPushMatrix()
		
		mat = glGetFloat(GL_MODELVIEW_MATRIX)

		ball = self.balls[0]        
		x = mat[0][0]*ball.position[0] + mat[1][0]*ball.position[1] + mat[2][0]*ball.position[2] + mat[3][0]
		y = mat[0][1]*ball.position[0] + mat[1][1]*ball.position[1] + mat[2][1]*ball.position[2] + mat[3][1]
		z = mat[0][2]*ball.position[0] + mat[1][2]*ball.position[1] + mat[2][2]*ball.position[2] + mat[3][2]				
		
		glLoadIdentity()
		glTranslatef(x, y, z)
		glRotatef(angle, rotate_axis[0], rotate_axis[1], rotate_axis[2])
		
		
		glMaterialfv(GL_FRONT, GL_AMBIENT, [1,1,1,1])
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [1,1,1,1])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [1,1,1,1])		
		#glutSolidCone(0.2, 4.0, 50, 50)
		quadric = gluNewQuadric()
		glTranslatef(0,0,1)
		gluCylinder(quadric, 0.1, 0.2, 5, 50, 50)
		gluSphere(quadric, 0.1, 50, 50,)
		glTranslatef(0,0,5)
		gluSphere(quadric, 0.2, 50, 50,)
		
		glMaterialfv(GL_FRONT, GL_AMBIENT, [1,0,0,1])
		glBegin(GL_LINES)
		glVertex3f(0,0,0)
		glVertex3f(0,0,-100)
		glEnd()
		
		glPopMatrix()

	
	def display_walls(self):
		''' make six walls, let the front faces of the walls be transparent '''
		glEnable (GL_BLEND)
		glDepthMask (GL_FALSE)
		glEnable(GL_TEXTURE_2D)
		


		glMaterialfv(GL_FRONT, GL_AMBIENT, [0.1, 0.0, 0.0, 0.2])
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.1, 0.0, 0.0, 0.2])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [0.1, 0.0, 0.0, 0.2])
		
		
		glMaterialfv(GL_BACK, GL_AMBIENT, [0.0, 0.1, 0.0, 1.0])
		glMaterialfv(GL_BACK, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])
		glMaterialfv(GL_BACK, GL_SPECULAR, [0.0, 0.0, 0.0, 1.0])
						
		glBlendFunc (GL_SRC_ALPHA, GL_DST_ALPHA)
		
		f1 = 10
		f2 = 10
		f3 = 10
		
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)	 
		glVertex3f(MIN_X, MAX_Y, MIN_Z)
		glTexCoord2f(0.0, f1)	
		glVertex3f(MAX_X, MAX_Y, MIN_Z)
		glTexCoord2f(f1, f1)	
		glVertex3f(MAX_X, MIN_Y, MIN_Z)
		glTexCoord2f(f1, 0.0)	
		glVertex3f(MIN_X, MIN_Y, MIN_Z)  
		glEnd()

		
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)	
		glVertex3f(MIN_X, MIN_Y, MAX_Z)
		glTexCoord2f(0.0, f1)	
		glVertex3f(MAX_X, MIN_Y, MAX_Z)
		glTexCoord2f(f1, f1)	
		glVertex3f(MAX_X, MAX_Y, MAX_Z)
		glTexCoord2f(f1, 0.0)	
		glVertex3f(MIN_X, MAX_Y, MAX_Z)
		glEnd()


		glBegin(GL_QUADS)
		glTexCoord2f(0.0, f2)
		glVertex3f(MIN_X ,MIN_Y, MIN_Z)
		glTexCoord2f(0.0, 0.0)	
		glVertex3f(MIN_X ,MIN_Y, MAX_Z)
		glTexCoord2f(f2, 0.0)
		glVertex3f(MIN_X ,MAX_Y, MAX_Z)
		glTexCoord2f(f2, f2)
		glVertex3f(MIN_X ,MAX_Y, MIN_Z)
		glEnd()

	
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(MAX_X, MIN_Y, MIN_Z)
		glTexCoord2f(f2, 0.0)
		glVertex3f(MAX_X, MAX_Y, MIN_Z)
		glTexCoord2f(f2, f2)
		glVertex3f(MAX_X, MAX_Y, MAX_Z)
		glTexCoord2f(0.0, f2)
		glVertex3f(MAX_X, MIN_Y, MAX_Z)
		glEnd()

		
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(MIN_X, MIN_Y, MAX_Z)
		glTexCoord2f(f3, 0.0)
		glVertex3f(MIN_X, MIN_Y, MIN_Z)
		glTexCoord2f(f3, f3)
		glVertex3f(MAX_X, MIN_Y, MIN_Z)
		glTexCoord2f(0.0, f3)
		glVertex3f(MAX_X, MIN_Y, MAX_Z)
		glEnd()
		
		
		glBegin(GL_QUADS)
		glTexCoord2f(0.0, 0.0)
		glVertex3f(MAX_X, MAX_Y, MAX_Z)
		glTexCoord2f(f3, 0.0)
		glVertex3f(MAX_X, MAX_Y, MIN_Z)
		glTexCoord2f(f3, f3)
		glVertex3f(MIN_X, MAX_Y, MIN_Z)
		glTexCoord2f(0.0, f3)
		glVertex3f(MIN_X, MAX_Y, MAX_Z)
		glEnd()
		
		glDisable(GL_TEXTURE_2D)
		glDepthMask (GL_TRUE);

		glDisable(GL_BLEND)

	
	def make_lights(self):
		''' make three light sources for the scene '''
		glEnable(GL_LIGHTING)
		glEnable(GL_DEPTH_TEST)
		glLightModelf(GL_LIGHT_MODEL_TWO_SIDE, 1)
		   
		light_ambient =  [1.0, 1.0, 1.0, 1.0]
		light_diffuse =  [1.0, 1.0, 1.0, 1.0]
		light_specular = [1.0, 1.0, 1.0, 1.0]
				
		scale(light_ambient,0.3)
		scale(light_diffuse,0.3)
		scale(light_specular,1)
				
		glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
		glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
		glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
		glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 10.0, 0.0])
		glEnable(GL_LIGHT0)
			 
				
		glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient)
		glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse)
		glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular)
		glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, -10.0, 0.0])
		glEnable(GL_LIGHT1)
				
				
		glLightfv(GL_LIGHT2, GL_AMBIENT, light_ambient)
		glLightfv(GL_LIGHT2, GL_DIFFUSE, light_diffuse)
		glLightfv(GL_LIGHT2, GL_SPECULAR, light_specular)
		glLightfv(GL_LIGHT3, GL_POSITION, [10.0, 0.0, 0.0, 0.0])
		glEnable(GL_LIGHT2)
				
		glLightfv(GL_LIGHT3, GL_AMBIENT, light_ambient)
		glLightfv(GL_LIGHT3, GL_DIFFUSE, light_diffuse)
		glLightfv(GL_LIGHT3, GL_SPECULAR, light_specular)
		glLightfv(GL_LIGHT3, GL_POSITION, [-10.0, 0.0, 0.0, 0.0])
		glEnable(GL_LIGHT3)
		
	
	def display(self):
		''' draw the whole scene '''
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

		glMatrixMode (GL_PROJECTION)
		glPushMatrix()
		glTranslatef(0, 0, -20)

		
		glMatrixMode (GL_MODELVIEW)
		
		
		if not self.balls[0].living:
			self.balls[0].velocity=[0,0,0]
			self.balls[0].position=[0,0,0]
			self.balls[0].living=True
		self.physics_engine.reset()
		for ball in self.balls:
			if ball.living:
				self.physics_engine.move(ball)
				self.display_ball(ball)
		
		if modulus(self.balls[0].velocity)<10e-5:
			self.display_stick()
		self.display_walls()
		
		
		for p1 in [MIN_X, MAX_X]:
			for p2 in [MIN_Y, MAX_Y]:
				for p3 in [MIN_Z, MAX_Z]:
					self.display_hole([p1, p2, p3])
			
		
		
		glMatrixMode (GL_PROJECTION)
		glPopMatrix()
		
		glMatrixMode (GL_MODELVIEW)
		
		glFlush()				


	
	def init(self):
		''' init texture, light and balls in the scene '''   
		self.load_textures()
		
		self.make_lights()
		self.make_ball([1,1,1,1], [0,0,0], 0)
		self.make_balls(BALL_NUM)
		
		''' reset the stick direction '''
		self.stick_direction = [0,0,1]
		self.old_stick_direction = [0,0,1]
		
	
	def reshape(self, w, h):
		''' reset the clipping volume using glFrustum '''
		self.width = w
		self.height = h
		glViewport(0, 0, w, h)
	
		glMatrixMode (GL_PROJECTION)
		#gluPerspective(45, 1, 0.1, 100)
		glLoadIdentity()
			
		scale = 0.1
		if w <= h:
			glFrustum(scale*MIN_X, scale*MAX_X, scale*MIN_X*h/w, scale*MAX_X*h/w, 1, 100)
		else: 
			glFrustum(scale*MIN_X*w/h, scale*MAX_X*w/h, scale*MIN_X, scale*MAX_X, 1, 100)

		glMatrixMode(GL_MODELVIEW)



		
	def load_textures(self):
		image = Image.open('data/wall.bmp')
		width = image.size[0]
		height = image.size[1]
		image = image.tostring('raw', 'RGBX', 0, -1)
		glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
		glPixelStorei(GL_UNPACK_ALIGNMENT,1)
		glTexImage2D(GL_TEXTURE_2D, 0, 3, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
		glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
		glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
		
	def load_sound(self, name):
		pygame.mixer.quit()
		pygame.mixer.init(22050, -16, 2, 64)
		
		class NoneSound:
			def play(self): pass
		if not pygame.mixer or not pygame.mixer.get_init():
			return NoneSound()
		
		fullname = os.path.join('data', name)
		#fullname = name
		print fullname
		try:
			sound = pygame.mixer.Sound(fullname)
		except pygame.error, message:
			print 'Cannot load sound:', fullname
			raise SystemExit, message
		return sound
		
scene = Scene()
scene.run()
