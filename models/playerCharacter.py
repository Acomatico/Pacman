import pygame

from models.directions import Directions
from models.movableObject import MovableObject


class PlayerCharacter(MovableObject):
    def __init__(self, x, y, surface, size, color, renderer):
        super().__init__(x, y, surface, size, color, renderer)
    
    def draw(self):
        x, y = self.position[0] + self.size // 2, self.position[1] + self.size // 2

        pygame.draw.circle(self.surface, self.color, (x,y), self.size // 2)
    
    def move(self, direction: Directions):
        super().move(direction)

    def tick(self):
        pass

    def collides_with_ghosts(self, direction: Directions):
        x,y = Directions.add_to_position(self.position, direction)

        for ghost in self.renderer.ghosts:
            if self == ghost:
                continue
            player_coll = pygame.Rect(x, y, self.size, self.size)
            other_coll = pygame.Rect(ghost.position[0], ghost.position[1], ghost.size, ghost.size)
            if pygame.Rect.colliderect(other_coll, player_coll):
                return True
        
        return False