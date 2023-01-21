import pygame

from models.directions import Directions
from models.object import BasicObject


class MovableObject(BasicObject):
    def __init__(self,x,y,surface,size,color,renderer):
        self.renderer = renderer
        super().__init__(x, y, surface, size, color)
    
    def collides_with_wall(self, direction: Directions):
        x,y = Directions.add_to_position(self.position, direction)

        for wall in self.renderer.walls:
            ghost_coll = pygame.Rect(x, y, self.size, self.size)
            wall_coll = pygame.Rect(wall.position[0], wall.position[1], wall.size, wall.size)
            if pygame.Rect.colliderect(wall_coll, ghost_coll):
                return True
        
        return False
    
    def move(self, direction: Directions):
        if self.collides_with_wall(direction):
            return

        x, y = Directions.add_to_position(self.position, direction)
        
        if x > self.renderer.width - self.size // 2:
            x = self.size // 2
        if x < 0:
            x = self.renderer.width - self.size // 2

        if y > self.renderer.height - self.size // 2:
            y = self.size // 2
        if y < 0:
            y = self.renderer.height - self.size // 2

        self.position = (x,y)