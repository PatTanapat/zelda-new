import math
from src.world.Pot import Pot
from src.states.BaseState import BaseState
from src.HitBox import Hitbox
import pygame
from src.recourses import *

class PlayerLiftPotState(BaseState):
    def __init__(self, player, dungeon=None):
        self.player = player
        self.dungeon = dungeon
        

        
        
        
        self.pot = None  # To store the pot object
        # self.player.ChangeAnimation("lift_pot_"+self.player.direction)
    
    def Enter(self, params):
        #sounds
        self.player.curr_animation.Refresh()
        direction = self.player.direction

        if direction == 'left':
            self.player.offset_x =-8
            self.player.offset_y =8
        elif direction == 'right':
            self.player.offset_x =8
            self.player.offset_y =8
        elif direction == 'up':
            self.player.offset_x =0
            self.player.offset_y =8
        elif direction == 'down':
            self.player.offset_x =0
            self.player.offset_y =8
        

        for obj in self.dungeon.current_room.objects:
            if isinstance(obj, Pot) and self.player.PotCollides(obj):
                self.pot = obj
                self.pot.is_carried = True
                break

        self.player.ChangeAnimation("lift_pot_" + self.player.direction)

    def Exit(self):
        pass

    def update(self, dt, events):
        
        if self.pot and self.pot.is_carried:
            self.pot.x = self.player.x
            self.pot.y = self.player.y - self.player.height // 2
        
            

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Switch to throw pot state
                    self.player.ChangeState('throw_pot', {'pot': self.pot})
                elif event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP or pygame.K_DOWN:
                    self.player.ChangeState('walk_pot',{'pot': self.pot} )
        self.player.curr_animation.update(dt)
       

    def render(self, screen):
        # Call the player's render function to render the player
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x - self.player.offset_x), math.floor(self.player.y - self.player.offset_y)))
        

        # Render the pot if it is being carried
        if self.pot and self.pot.is_carried:
            self.pot.render(screen)

    def Exit(self):
        # Reset pot carry state when exiting this state
        if self.pot:
            self.pot.is_carried = False



