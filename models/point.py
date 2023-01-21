from models.object import BasicObject
import pygame

class Point(BasicObject):
    def __init__(self, x, y, surface, size, color):
        super().__init__(x, y, surface, size, color)

    def draw(self):
        x, y = self.position

        pygame.draw.circle(self.surface, self.color, (x,y), self.size // 2)   