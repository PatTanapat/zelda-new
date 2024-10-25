import random

from src.entity_defs import *
from src.constants import *
from src.Dependencies import *
from src.world.Doorway import Doorway
from src.EntityBase import EntityBase
from src.entity_defs import EntityConf
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState
from src.states.entity.EntityStopState import EntityStopState
from src.world.Pot import Pot
from src.StateMachine import StateMachine
from src.GameObject import GameObject
from src.object_defs import *
import pygame


class Room:
    def __init__(self, player):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT

        self.tiles = []
        self.GenerateWallsAndFloors()

        self.entities = []
        self.GenerateEntities()

        self.objects = []
        self.GenerateObjects()

        self.doorways = []
        self.doorways.append(Doorway('top', False, self))
        self.doorways.append(Doorway('botoom', False, self))
        self.doorways.append(Doorway('left', False, self))
        self.doorways.append(Doorway('right', False, self))


        # for collisions
        self.player = player
        self.pot_carried =None

        # centering the dungeon rendering
        self.render_offset_x = MAP_RENDER_OFFSET_X
        self.render_offset_y = MAP_RENDER_OFFSET_Y

        self.render_entity=True

        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0

    def GenerateWallsAndFloors(self):
        for y in range(1, self.height+1):
            self.tiles.append([])
            for x in range(1, self.width+1):
                id = TILE_EMPTY

                # Wall Corner
                if x == 1 and y == 1:
                    id = TILE_TOP_LEFT_CORNER
                elif x ==1 and y == self.height:
                    id = TILE_BOTTOM_LEFT_CORNER
                elif x == self.width and y == 1:
                    id = TILE_TOP_RIGHT_CORNER
                elif x == 1 and y == self.height:
                    id = TILE_BOTTOM_RIGHT_CORNER

                #Wall, Floor
                elif x==1:
                    id = random.choice(TILE_LEFT_WALLS)
                elif x == self.width:
                    id = random.choice(TILE_RIGHT_WALLS)
                elif y == 1:
                    id = random.choice(TILE_TOP_WALLS)
                elif y == self.height:
                    id = random.choice(TILE_BOTTOM_WALLS)
                else:
                    id = random.choice(TILE_FLOORS)

                self.tiles[y-1].append(id)

    def GenerateEntities(self):
        types = ['skeleton']

        for i in range(NUMBER_OF_MONSTER):
            type = random.choice(types)

            conf = EntityConf(animation = ENTITY_DEFS[type].animation,
                              walk_speed = ENTITY_DEFS[type].walk_speed,
                              x=random.randrange(MAP_RENDER_OFFSET_X+TILE_SIZE, WIDTH - TILE_SIZE * 2 - 48),
                              y=random.randrange(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(HEIGHT-MAP_HEIGHT*TILE_SIZE)+MAP_RENDER_OFFSET_Y - TILE_SIZE - 48),
                              width=ENTITY_DEFS[type].width, height=ENTITY_DEFS[type].height, health=ENTITY_DEFS[type].health)

            self.entities.append(EntityBase(conf))

            self.entities[i].state_machine = StateMachine()
            self.entities[i].state_machine.SetScreen(pygame.display.get_surface())
            self.entities[i].state_machine.SetStates({
                "walk": EntityWalkState(self.entities[i]),
                "idle": EntityIdleState(self.entities[i]),
                "stop": EntityStopState(self.entities[i])
            })

            self.entities[i].ChangeState("walk")

    def GenerateObjects(self):
        switch = GameObject(GAME_OBJECT_DEFS['switch'],
                            x=random.randint(MAP_RENDER_OFFSET_X + TILE_SIZE, WIDTH-TILE_SIZE*2 - 48),
                            y=random.randint(MAP_RENDER_OFFSET_Y+TILE_SIZE, HEIGHT-(HEIGHT-MAP_HEIGHT*TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 48))

        def switch_function():
            if switch.state == "unpressed":
                switch.state = "pressed"

                for doorway in self.doorways:
                    doorway.open = True
                gSounds['door'].play()

        switch.on_collide = switch_function

        self.objects.append(switch)
        
         # Add pots randomly in the room
        for i in range(random.randint(1, 3)):  # Randomly add 1 to 3 pots
            x = random.randint(MAP_RENDER_OFFSET_X + TILE_SIZE, WIDTH - TILE_SIZE * 2 - 48)
            y = random.randint(MAP_RENDER_OFFSET_Y + TILE_SIZE, HEIGHT-(HEIGHT-MAP_HEIGHT*TILE_SIZE) + MAP_RENDER_OFFSET_Y - TILE_SIZE - 48)

        # Pass the x and y coordinates to GameObject constructor

            pot = Pot(GAME_OBJECT_DEFS['pot'], x, y)
            self.objects.append(pot)
    def update(self, dt, events):
        if self.adjacent_offset_x != 0 or self.adjacent_offset_y != 0:
            return
        if self.player is not None:
            self.player.update(dt, events)

        
            
        skeleton_killed = False
        for entity in self.entities:
            if entity.health <= 0:
                gSounds['healing'].play()
                
                entity.is_dead = True
                skeleton_killed = True  # Mark that a skeleton has been killed
                self.entities.remove(entity)  # Remove the dead skeleton from the room
            if skeleton_killed:
                while self.player.health < 6:  # Assuming full health is 6
                    if self.player.health % 2 == 1:  # If the player has half a heart
                        self.player.health += 1  # Fill half a heart
                    else:
                        self.player.health += 2  # Fill a full heart
                    if self.player.health > 6:
                        self.player.health = 6  # Cap the health at full (3 full hearts)
                for entity in self.entities:
                    if not entity.is_dead:
                        entity.ChangeState("stop")
            elif not entity.is_dead:
                entity.ProcessAI({"room":self}, dt)
                entity.update(dt, events)

            if not entity.is_dead and self.player.Collides(entity) and not self.player.invulnerable:
                gSounds['hit_player'].play()
                self.player.Damage(1)
                self.player.SetInvulnerable(1.5)
                
        if self.pot_carried:
            for entity in self.entities:
                if entity.Collides(self.pot_carried):  # Skeleton hits the pot, player takes no damage
                    print("Skeleton hit the pot!")
                elif self.player.Collides(entity) and not self.player.invulnerable:  # Player takes damage normally
                    gSounds['hit_player'].play()
                    self.player.Damage(1)
                    self.player.SetInvulnerable(1.5)
            

        # Handle pot following player when carried
        if self.pot_carried:
            self.pot_carried.x = self.player.x
            self.pot_carried.y = self.player.y - self.player.height // 2
    
            for event in events:
                    if event.key == pygame.K_LEFT or pygame.K_RIGHT or pygame.K_UP or pygame.K_DOWN:
                        self.player.ChangeState('walk_pot',{'pot': self.pot} )
                        self.pot_carried.x = self.player.x
                        self.pot_carried.y = self.player.y - self.player.height // 2

        for object in self.objects:
            object.update(dt)
            if self.player.Collides(object):
                if object.on_collide is not None:
                    object.on_collide()
            


    def render(self, screen, x_mod, y_mod, shifting):
        for y in range(self.height):
            for x in range(self.width):
                tile_id = self.tiles[y][x]
                # need to access tile_id - 1  <-- actual list is start from 0
                screen.blit(gRoom_image_list[tile_id-1], (x * TILE_SIZE + self.render_offset_x + self.adjacent_offset_x + x_mod,
                            y * TILE_SIZE + self.render_offset_y + self.adjacent_offset_y + y_mod))


        for doorway in self.doorways:
            doorway.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)

        for object in self.objects:
            object.render(screen, self.adjacent_offset_x+x_mod, self.adjacent_offset_y+y_mod)


        if not shifting:
            for entity in self.entities:
                if not entity.is_dead:
                    entity.render(self.adjacent_offset_x, self.adjacent_offset_y + y_mod)
            if self.player:
                self.player.render()
