from cmath import pi
from random import randrange
import pygame
import numpy

from models.directions import Directions
from models.movableObject import MovableObject


class Ghost(MovableObject):
    def __init__(self, x, y, surface, size, color, renderer):
        self.original_position = (x,y)
        self.direction = Directions.NONE
        self.time_random = 0
        self.time_dead = 0
        self.queued_movements = []
        super().__init__(x, y, surface, size, color, renderer)


    def move(self, direction: Directions):        
        super().move(direction)
        self.direction = direction

    def draw(self):
        x, y = self.position[0] + self.size // 2, self.position[1] + self.size // 2

        pygame.draw.circle(self.surface, self.color, (x,y), self.size // 2)
    
    def tick(self):
        if self.time_dead > pygame.time.get_ticks():
            return

        if self.queued_movements:
            self.move(self.queued_movements.pop(0))
            return

        if self.renderer.is_power_mode_on() or self.time_random > pygame.time.get_ticks():
            self.move_random_direction()
        else:
            self.move_towards_player()

    def move_towards_player(self):
        player_x, player_y = self.renderer.player_character.position
        ghost_x, ghost_y = self.position

        x_diff = player_x - ghost_x
        y_diff = ghost_y - player_y

        angle = numpy.arctan2(y_diff, x_diff) * 180 / numpy.pi 
        
        direction = Directions.RIGHT

        if angle > 45:
            direction = Directions.UP
        if angle > 135 or angle <= -135:
            direction = Directions.LEFT
        if angle > -135 and angle < - 45:
            direction = Directions.DOWN
        

        if self.collides_with_wall(direction):
            self.move_random_direction()
            self.time_random = 5 * self.size + pygame.time.get_ticks()
            return
        for _ in range(self.size):
            self.queued_movements.append(direction)

        self.move(self.queued_movements.pop(0))
        
    def move_random_direction(self):
        available_directions = []

        if self.direction != Directions.NONE and not self.collides_with_wall(self.direction):
            for i in range(5):
                available_directions.append(self.direction)
        if not self.collides_with_wall(Directions.RIGHT):
            available_directions.append(Directions.RIGHT)
        if not self.collides_with_wall(Directions.LEFT):
            available_directions.append(Directions.LEFT)
        if not self.collides_with_wall(Directions.DOWN):
            available_directions.append(Directions.DOWN)
        if not self.collides_with_wall(Directions.UP):
            available_directions.append(Directions.UP)

        if not available_directions:
            return

        new_direction = available_directions[randrange(0, len(available_directions))]
        for _ in range(self.size):
            self.queued_movements.append(new_direction)

        self.move(self.queued_movements.pop(0))


    
    def reset(self):
        self.position = self.original_position
        self.time_dead = pygame.time.get_ticks() + 2000

