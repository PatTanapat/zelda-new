import math

from src.states.BaseState import BaseState
import random

class EntityStopState(BaseState):
    def __init__(self, entity):
        self.entity = entity
        

       
        # Add flag to track if the skeleton is dead
        self.is_dead = False
        
    def Enter(self, params):
        
        if params and 'is_dead' in params:
            self.is_dead = params['is_dead']  # Set dead status from parameters

        self.entity.velocity_x = 0
        self.entity.velocity_y = 0
        self.entity.rect.x = self.entity.rect.x
        self.entity.rect.y = self.entity.rect.y    

    def Exit(self):
        pass

    def update(self, dt, events):
        pass

    def ProcessAI(self, params, dt):
        if self.is_dead:
            return  # Skeleton stays idle and does nothing
        

    def render(self, screen):
       idle_image = self.entity.curr_animation.idleSprite

       screen.blit(idle_image, (math.floor(self.entity.rect.x - self.entity.offset_x),
                    math.floor(self.entity.rect.y - self.entity.offset_y)))