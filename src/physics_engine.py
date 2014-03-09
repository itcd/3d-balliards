from parameter import *
from ball import *

from vector_utils import *

import math

class PhysicsEngine:
    
    def __init__(self, scene):
        self.scene = scene
        
    
    def reset(self):
        for ball in self.scene.balls:
            ball.responsed = False
        

    def collide(self, ball1, ball2):
        return (ball1.position[0]-ball2.position[0])**2+(ball1.position[1]-ball2.position[1])**2+(ball1.position[2]-ball2.position[2])**2<(2*R)**2
        

    def check_rebounce(self, ball):
        if ball.position[0]<=MIN_X+R:
            ball.position[0]=2*(MIN_X+R)-ball.position[0]
            ball.velocity[0]=-ball.velocity[0]
            self.scene.bounce_sound.play()
        if ball.position[0]>=MAX_X-R:
            ball.position[0]=2*(MAX_X-R)-ball.position[0]
            ball.velocity[0]=-ball.velocity[0]
            self.scene.bounce_sound.play()

        if ball.position[1]<=MIN_Y+R:
            ball.position[1]=2*(MIN_Y+R)-ball.position[1]
            ball.velocity[1]=-ball.velocity[1]
            self.scene.bounce_sound.play()
        if ball.position[1]>=MAX_Y-R:
            ball.position[1]=2*(MAX_Y-R)-ball.position[1]
            ball.velocity[1]=-ball.velocity[1]
            self.scene.bounce_sound.play()

        if ball.position[2]<=MIN_Z+R:
            ball.position[2]=2*(MIN_Z+R)-ball.position[2]
            ball.velocity[2]=-ball.velocity[2]
            self.scene.bounce_sound.play()
        if ball.position[2]>=MAX_Z-R:
            ball.position[2]=2*(MAX_Z-R)-ball.position[2]
            ball.velocity[2]=-ball.velocity[2]
            self.scene.bounce_sound.play()
    
    def check_fell(self, ball):
        for p1 in [MIN_X, MAX_X]:
            for p2 in [MIN_Y, MAX_Y]:
                for p3 in [MIN_Z, MAX_Z]:
                    if (ball.position[0]-p1)**2+(ball.position[1]-p2)**2+(ball.position[2]-p3)**2<(4*R)**2:
                        ball.living = False
                        if ball.number == 0:
                            self.scene.oops_sound.play()
                        else:
                            self.scene.yay_sound.play()
                   


    def response(self, ball1, ball2):
        collision_vector = sub(ball2.position, ball1.position)
        normalize(collision_vector)
        collision_vector2 = [-collision_vector[0], -collision_vector[1], -collision_vector[2]]

        d1 = dot_product(ball1.velocity, collision_vector)
        p1 = [d1*collision_vector[0], d1*collision_vector[1], d1*collision_vector[2]]
        
         
        d2 = dot_product(ball2.velocity, collision_vector2)
        p2 = [d2*collision_vector2[0], d2*collision_vector2[1], d2*collision_vector2[2]]
        
        if dot_product(sub(p1,p2),collision_vector)<0: return
        
        #print "p1: ", p1 
        #print "p2: ", p2
        
                
        ball1.velocity = add(sub(ball1.velocity, p1), p2)
        ball2.velocity = add(sub(ball2.velocity, p2), p1)
        
        
    
    
    def apply_friction(self, ball):
        for i in [0,1,2]:
                ball.velocity[i]*=FRICTION         
        if(modulus(ball.velocity)<0.01): ball.velocity=[0,0,0]
    

    def move(self, ball):
        ball.position[0]+=ball.velocity[0]
        ball.position[1]+=ball.velocity[1]
        ball.position[2]+=ball.velocity[2]
        
        self.apply_friction(ball)
        self.check_fell(ball)
        self.check_rebounce(ball)
        
        if ball.responsed==True or ball.living==False:
            return
        for another_ball in self.scene.balls:
            if another_ball!=ball:
                if self.collide(ball,another_ball):
                    #ball.velocity[0]=0
                    #ball.velocity[1]=0
                    #ball.velocity[2]=0
                    self.response(ball,another_ball)
                    ball.responsed = True
                    another_ball.responsed = True
                    
                    self.scene.bounce_sound.play()

    
