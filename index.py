import pygame
from models.directions import Directions

from models.ghost import Ghost
from models.playerCharacter import PlayerCharacter
from models.powerBall import PowerBall
from models.wall import Wall
from models.point import Point

class Controller:
    def __init__(self, maze_matrix) -> None:
        self.maze_matrix = maze_matrix
        self.point_spaces = []
        self.reachable_spaces = []
        self.ghosts_spaces = []
        self.size = (0,0)


class Renderer:
    def __init__(self, width, height) -> None:
        pygame.init()

        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.objects = []
        self.clock = pygame.time.Clock()
        self.walls = []
        self.timed_wall = None
        self.timeout = 0
        self.points = []
        self.power_balls = []
        self.ghosts = []
        self.power_mode_time = 0
        self.player_character = None
        self.finished = False
    
    def tick(self, fps):
        while not self.finished:
            if not self.points:
                print("EZ clap")
                break
            for wall in self.walls:
                wall.tick()
                wall.draw()

            for point in self.points:
                point.tick()
                point.draw()

            for power_ball in self.power_balls:
                power_ball.tick()
                power_ball.draw()

            for ghost in self.ghosts:
                ghost.tick()
                ghost.draw()

            self.player_character.tick()
            self.player_character.draw()
            self.is_point_eaten()
            self.is_power_ball_eaten()
            self.is_player_eaten()

            if self.timed_wall and pygame.time.get_ticks() > self.timeout:
                self.remove_timed_wall()

            pygame.display.flip()
            self.clock.tick(fps)
            self.screen.fill((0,0,0))
            if self.is_power_mode_on():
                self.screen.fill((255,255,255))

            self.handle_events()
        print("Game Over boys")
    
    def add_object(self, object):
        self.objects.append(object)
    
    def add_wall(self, wall):
        self.walls.append(wall)
    
    def add_wall_with_timeout(self, wall, timeout):
        if not self.timed_wall:
            self.timed_wall = wall
            self.timeout = timeout
            self.add_wall(wall)

    def remove_timed_wall(self):
        for idx, wall in enumerate(self.walls):
            if self.timed_wall == wall:
                del self.walls[idx]

        self.timed_wall.color = (0,0,0)
        
    def add_ghost(self, ghost):
        self.ghosts.append(ghost)

    def add_player(self, player):
        self.player_character = player

    def handle_events(self):
        for event in pygame.event.get():
            if pygame.QUIT == event.type:
                self.finished = True
        
        if not self.player_character:
            return

        key = pygame.key.get_pressed()
        if True == key[pygame.K_RIGHT]:
            self.player_character.move(Directions.RIGHT)
        elif True == key[pygame.K_LEFT]:
            self.player_character.move(Directions.LEFT)
        elif True == key[pygame.K_UP]:
            self.player_character.move(Directions.UP)
        elif True == key[pygame.K_DOWN]:
            self.player_character.move(Directions.DOWN)
    
    def add_point(self, point):
        self.points.append(point)
    
    def add_power_ball(self, power_ball):
        self.power_balls.append(power_ball)

    def is_power_ball_eaten(self):
        x,y = self.player_character.position
        player_coll = pygame.Rect(x, y, self.player_character.size, self.player_character.size)
        for idx, power_ball in enumerate(self.power_balls):
            ball_x, ball_y = power_ball.position
            power_ball_coll = pygame.Rect(ball_x - power_ball.size // 2, ball_y - power_ball.size // 2, power_ball.size, power_ball.size)
            if pygame.Rect.colliderect(player_coll, power_ball_coll):
                self.set_power_mode()
                del self.power_balls[idx]

    def is_point_eaten(self):
        x,y = self.player_character.position
        player_coll = pygame.Rect(x, y, self.player_character.size, self.player_character.size)
        for idx, point in enumerate(self.points):
            point_coll = pygame.Rect(point.position[0] - point.size // 2, point.position[1] - point.size // 2, point.size, point.size)
            if pygame.Rect.colliderect(player_coll, point_coll):
                del self.points[idx]

    def is_player_eaten(self):
        x,y = self.player_character.position
        player_size = self.player_character.size
        player_coll = pygame.Rect(x + player_size // 2, y + player_size // 2, 1, 1)

        pygame.draw.rect(self.screen, (0,255,0), player_coll)
        for idx, ghost in enumerate(self.ghosts):
            ghost_coll = pygame.Rect(ghost.position[0], ghost.position[1], ghost.size, ghost.size)
            if pygame.Rect.colliderect(player_coll, ghost_coll):
                if self.is_power_mode_on():
                    ghost.reset()
                else:
                    self.finished = True
    
    def set_power_mode(self):
        self.power_mode_time = pygame.time.get_ticks() + 5000

    def is_power_mode_on(self):
        return pygame.time.get_ticks() < self.power_mode_time

    
matrix = [
    [0,0,0,0,0,0,1,0,0,0,0,0,0],
    [0,5,1,1,1,1,1,1,1,1,1,5,0],
    [0,1,0,1,0,0,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,1,1,0,1,0,1,0],
    [0,1,0,1,1,1,0,1,1,1,0,1,0],
    [1,1,1,0,0,0,0,0,0,0,1,1,1],
    [0,0,1,0,0,4,4,4,0,0,1,0,0],
    [0,0,1,0,0,4,4,4,0,0,1,0,0],
    [0,1,1,0,0,4,4,4,0,0,1,1,0],
    [1,1,0,0,0,0,2,0,0,0,0,1,1],
    [0,1,0,1,1,1,1,1,1,1,0,1,0],
    [0,1,0,0,0,0,1,0,0,0,0,1,0],
    [0,5,1,1,1,1,3,1,1,1,1,5,0],
    [0,0,0,0,0,0,1,0,0,0,0,0,0],
]

if __name__ == "__main__":
    size = 64
    character_size = size * 80 // 100
    point_size = size * 20 // 100
    power_ball_size = size * 50 // 100
    renderer = Renderer(size * len(matrix[0]), size * len(matrix))
    game = Controller(matrix)
    ghost_colors = [(255,0,0), (0,120,250), (255,0,250)]

    for i in range(len(matrix)):
        row = matrix[i]
        for j in range(len(row)):
            value = row[j]
            if value == 0:
                renderer.add_wall(Wall(j*size, i*size, renderer.screen, size, (0,0,180)))
            if value == 1:
                renderer.add_point(Point(size//2+j*size, size//2+i*size, renderer.screen, point_size, (200,200,0)))
            if value == 2:
                renderer.add_wall_with_timeout(Wall(j*size, i*size, renderer.screen, size, (0,0,180)), 3000)
            if value == 4 and ghost_colors:
                ghost_color = ghost_colors.pop()
                renderer.add_ghost(Ghost(j*size, i*size, renderer.screen, size, ghost_color, renderer))
            if value == 3:
                renderer.add_player(PlayerCharacter(j*size, i*size, renderer.screen, character_size, (255,255,0), renderer))
            if value == 5:
                renderer.add_power_ball(PowerBall(size//2+j*size, size//2+i*size, renderer.screen, power_ball_size, (200,200,0)))
    renderer.tick(100)
