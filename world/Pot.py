from src.constants import *
from src.recourses import *
from src.GameObject import GameObject
from src.object_defs import *
import pygame

class Pot(GameObject):
    def __init__(self, conf, x, y):
        super().__init__(conf, x, y)
        self.is_carried = False      # Whether the pot is currently carried by the player
        self.is_thrown = False       # Whether the pot is currently thrown
        self.is_destroyed = False    # Whether the pot has been destroyed
        self.velocity_x = 0          # Horizontal velocity for throwing
        self.velocity_y = 0          # Vertical velocity for throwing
        self.speed = 300             # Speed when thrown, can be adjusted if needed
        self.image = conf.image
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt):
        # Only update position if the pot is thrown and not destroyed
        if self.is_thrown and not self.is_destroyed:
            # Move the pot based on its velocity
            self.x += self.velocity_x * dt
            self.y += self.velocity_y * dt

            # Update pot's rect position for collision detection
            self.rect.x = self.x
            self.rect.y = self.y

            # Check for wall collisions to stop the pot
            if self.CollidesWithWall():
                print("Pot hit a wall!")
                self.is_destroyed = True
                self.is_thrown = False  # Stop the pot's movement on collision

    def CollidesWithEntity(self, entity):
        # Use entity's rect attributes for collision detection
        return not (
            self.x + self.width < entity.rect.x or self.x > entity.rect.x + entity.width or
            self.y + self.height < entity.rect.y or self.y > entity.rect.y + entity.height
        )

    def CollidesWithWall(self):
        # Logic to check if the pot hits a wall
        return (self.x <= MAP_RENDER_OFFSET_X or
                self.x + self.width >= WIDTH - TILE_SIZE * 2 or
                self.y <= MAP_RENDER_OFFSET_Y or
                self.y + self.height >= HEIGHT - TILE_SIZE)

    def render(self, screen, offset_x=0, offset_y=0):
        # Only render the pot if it is not destroyed
        if not self.is_destroyed:
         if isinstance(self.image, list): 
            screen.blit(self.image[self.state_list[self.state]], (self.x + offset_x, self.y + offset_y))
