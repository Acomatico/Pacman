class BasicObject:
    def __init__(self, x, y, surface, size, color):
        self.position = (x,y)
        self.size = size
        self.surface = surface
        self.color = color

    def draw(self):
        pass

    def tick(self):
        pass