from src.states.entity.EntityIdleState import EntityIdleState
from src.world.Dungeon import Dungeon
from src.world.Pot import Pot
import pygame

class PlayerIdleState(EntityIdleState):
    def __init__(self, player):
        super(PlayerIdleState, self).__init__(player)

    def Enter(self, params):
        self.entity.offset_y = 15
        self.entity.offset_x = 0
        super().Enter(params)

    def Exit(self):
        pass

    def update(self, dt, events):
        pressedKeys = pygame.key.get_pressed()
        if pressedKeys[pygame.K_LEFT] or pressedKeys [pygame.K_RIGHT] or pressedKeys [pygame.K_UP] or pressedKeys [pygame.K_DOWN]:
            self.entity.ChangeState('walk')

       

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_RETURN:
                    for obj in self.entity.dungeon.current_room.objects:
                        if isinstance(obj, Pot) and self.entity.Collides(obj):
                            self.entity.ChangeState('lift_pot', {'pot': obj})
                            font = pygame.font.Font(None, 36)
                            text = font.render("Press Enter to lift", True, (255, 255, 255))
                            screen = pygame.display.get_surface()
                            screen.blit(text, (self.entity.x, self.entity.y - 20))  # Display near the player   
                elif event.key == pygame.K_SPACE:
                    self.entity.ChangeState('swing_sword')
        if self.entity.dungeon and self.entity.dungeon.current_room:
            for obj in self.entity.dungeon.current_room.objects:
            # Process objects in the current room
                pass
        else:
            print("Warning: Dungeon or current_room is not set")            