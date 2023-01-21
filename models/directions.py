from enum import Enum


class Directions(Enum):
    NONE = 0
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

    def add_to_position(position, direction):
        x, y = position
        if direction == Directions.DOWN:
            y += 1
        elif direction == Directions.UP:
            y -= 1
        elif direction == Directions.RIGHT:
            x += 1
        elif direction == Directions.LEFT:
            x -= 1
        
        return (x,y)