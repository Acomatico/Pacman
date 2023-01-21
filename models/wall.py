import pygame

from models.object import BasicObject

class Wall(BasicObject):
    def __init__(self, x, y, surface, size, color):
        super().__init__(x,y,surface,size,color)
    
    
    def draw(self):
        x,y = self.position
        rectangle = pygame.Rect(x, y, self.size, self.size)
        pygame.draw.rect(self.surface, self.color, rectangle)