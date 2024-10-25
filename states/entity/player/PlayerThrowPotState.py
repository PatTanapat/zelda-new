from src.states.BaseState import BaseState
import math
from src.constants import *

class PlayerThrowPotState(BaseState):
    def __init__(self, player, dungeon=None):
        self.player = player
        self.dungeon = dungeon
        self.pot = None
        
    def Enter(self, params):
        print("Entering PlayerThrowPotState")  # Debugging
        self.pot = params['pot']
        if self.pot:
            self.pot.is_carried = False  # Pot is no longer carried
            self.pot.is_thrown = True  # Pot is thrown
            # Set the throw velocity based on the player's direction at throw time
            throw_direction = self.player.direction
            if throw_direction == 'left':
                self.pot.velocity_x = -self.pot.speed
                self.pot.velocity_y = 0
            elif throw_direction == 'right':
                self.pot.velocity_x = self.pot.speed
                self.pot.velocity_y = 0
            elif throw_direction == 'up':
                self.pot.velocity_x = 0
                self.pot.velocity_y = -self.pot.speed
            elif throw_direction == 'down':
                self.pot.velocity_x = 0
                self.pot.velocity_y = self.pot.speed

            print(f"Pot thrown with velocity ({self.pot.velocity_x}, {self.pot.velocity_y})")

        # Ensure the player does not reset position
        self.player_x_at_throw = self.player.x
        self.player_y_at_throw = self.player.y
        self.player.ChangeState('idle')  # Player goes back to idle after throw

    def update(self, dt, events):
        # Ensure the player stays in position after the throw
        self.player.x = self.player_x_at_throw
        self.player.y = self.player_y_at_throw

        # Update pot's position after throw
        if self.pot and self.pot.is_thrown:
            self.pot.update(dt)  # Let the pot handle its own movement

            # Check if pot collides with any entities in the current room
            for entity in self.dungeon.current_room.entities:
                if self.pot.CollidesWithEntity(entity):
                    print("Pot hit an entity!")  # Debugging
                    entity.health -= 1  # Inflict damage on the entity
                    if entity.health <= 0:
                        entity.is_dead = True  # Mark entity as dead if health is 0 or less
                    self.dungeon.current_room.objects.remove(self.pot)  # Remove pot after hit
                    self.pot.is_thrown = False
                    break

            # Check if pot collides with a wall and remove it
            if self.pot.CollidesWithWall():
                print("Pot hit a wall!")  # Debugging
                self.dungeon.current_room.objects.remove(self.pot)
                self.pot.is_thrown = False

    def render(self, screen):
        animation = self.player.curr_animation.image
        screen.blit(animation, (math.floor(self.player.x - self.player.offset_x), math.floor(self.player.y - self.player.offset_y)))
        if self.pot:
            self.pot.render(screen)

    def Exit(self):
        # Reset pot velocity when exiting the state
        if self.pot:
            self.pot.velocity_x = 0
            self.pot.velocity_y = 0
