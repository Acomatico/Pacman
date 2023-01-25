from models.directions import Directions

class Pathfinder:
    def __init__(self, renderer) -> None:
        self.renderer = renderer

    def shortest_path_to_player(self, ghost):
        player = self.renderer.player_character
        wall_matrix = self.renderer.maze_matrix
        base_size = 64

        ghost_position_x = ghost.position[0] // base_size
        ghost_position_y = ghost.position[1] // base_size
        hero_position = (player.position[0] // base_size, player.position[1] // base_size)

        stack = [((ghost_position_x, ghost_position_y), dict())]

        shortest_path = dict()

        while stack:
            cur_position, cur_path = stack.pop()

            x,y = cur_position
            if x >= len(wall_matrix):
                x = 0
            if x < 0:
                x = len(wall_matrix) - 1
            
            if y >= len(wall_matrix[x]):
                y = 0
            if y < 0:
                y = len(wall_matrix[x]) - 1

            if cur_position in cur_path or wall_matrix[x][y] == 0:
                continue
            
            cur_path[cur_position] = True
            moves = len(cur_path)

            if cur_position == hero_position:
                if moves < len(shortest_path) or len(shortest_path) == 0:
                    shortest_path = cur_path
            
            stack.append(((x-1, y), cur_path.copy()))
            stack.append(((x+1, y), cur_path.copy()))
            stack.append(((x, y-1), cur_path.copy()))
            stack.append(((x, y+1), cur_path.copy()))
        
        return self.path_to_directions(list(shortest_path.keys()))
    
    def path_to_directions(self, path):
        result = []

        prev = path.pop(0)

        while path:
            cur = path.pop(0)
            x_diff = cur[0] - prev[0]
            y_diff = cur[1] - prev[1]
            diff = (x_diff, y_diff)

            if diff == (0,1):
                result.append(Directions.DOWN)
            elif diff == (0,-1):
                result.append(Directions.UP)
            elif diff == (1,0):
                result.append(Directions.RIGHT)
            elif diff == (-1,0):
                result.append(Directions.LEFT)

            prev = cur

        return result
    