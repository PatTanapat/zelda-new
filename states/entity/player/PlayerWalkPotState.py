from src.states.BaseState import BaseState
import math
from src.world.Pot import Pot
import pygame

class PlayerWalkPotState(BaseState):
    def __init__(self, player, dungeon=None):
        self.player = player
        self.dungeon = dungeon
        self.pot = None
        self.last_vertical_direction = None
        
    def Enter(self, params):
        self.pot = params['pot']
        # Set the walking pot animation based on the current direction
        self.player.ChangeAnimation('walk_pot_' + self.player.direction)
        self.player.curr_animation.Refresh()
        # Adjust initial offsets for the pot relative to the player
        if self.player.direction == 'left':
            self.player.offset_x = 16
            self.player.offset_y = 0
        elif self.player.direction == 'right':
            self.player.offset_x = -16
            self.player.offset_y = 0
        elif self.player.direction == 'up':
            self.player.offset_x = 0
            self.player.offset_y = -24
        elif self.player.direction == 'down':
            self.player.offset_x = 0
            self.player.offset_y = -24

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()

        # Sync the pot's position with the player's position as they move
        if self.pot and self.pot.is_carried:
            self.pot.x = self.player.x
            self.pot.y = self.player.y - self.player.height // 2

        # Handle player movement while carrying the pot
        if pressedKeys[pygame.K_LEFT]:
            self.player.direction = 'left'
            self.player.ChangeAnimation('walk_pot_left')
            self.player.x -= self.player.walk_speed * dt
            
            
            self.player.offset_x = 0
            self.player.offset_y = 8
            
            self.update_pot_position()

        elif pressedKeys[pygame.K_RIGHT]:
            self.player.direction = 'right'
            self.player.ChangeAnimation('walk_pot_right')
            self.player.x += self.player.walk_speed * dt
            
           
            self.player.offset_x = 0
            self.player.offset_y = 8
            
            self.update_pot_position()

        elif pressedKeys[pygame.K_UP]:
            self.player.direction = 'up'
            self.player.ChangeAnimation('walk_pot_up')
            self.player.y -= self.player.walk_speed * dt
            
           
            self.player.offset_x = 0
            self.player.offset_y = 16
            self.pot.offset_x = 0
            self.pot.offset_y = 16
            self.update_pot_position()

        elif pressedKeys[pygame.K_DOWN]:
            self.player.direction = 'down'
            self.player.ChangeAnimation('walk_pot_down')
            self.player.y += self.player.walk_speed * dt
            self.pot.y = self.player.y  # Sync pot y position
            
            self.player.offset_x = 0
            self.player.offset_y = 16
            self.pot.offset_x = 0
            self.pot.offset_y = 16
            self.update_pot_position()
        # Event handling for throwing the pot
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.ChangeState('throw_pot', {'pot': self.pot})
        self.player.curr_animation.update(dt)
    def render(self, screen):
        # Render the player with current animation and offset
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x - self.player.offset_x), math.floor(self.player.y - self.player.offset_y)))
    
        # Render the pot
        if self.pot and self.pot.is_carried:
            self.pot.render(screen)
    def update_pot_position(self):
        # Align pot position directly to player's position for consistent following
        self.pot.x = self.player.x
        self.pot.y = self.player.y - self.player.height // 2
    def Exit(self):
        # Reset any necessary state when exiting the "walk with pot" state
        if self.pot:
            self.pot.is_carried = False  # Pot is no longer carried when exiting
