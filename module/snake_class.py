from game_settings import SETTINGS, Point

class Snake:
    def __init__(self):
        self.head = Point(SETTINGS.GAME_WIDTH.value/2, SETTINGS.GAME_HEIGHT.value/2)
        self.coordinates = [self.head, Point(self.head.x - SETTINGS.BLOCK_SIZE.value, self.head.y), Point(self.head.x - (2*SETTINGS.BLOCK_SIZE.value), self.head.y)]
    
    def _go_up(self):
        self.head = Point(self.head.x, (self.head.y - SETTINGS.BLOCK_SIZE.value))
        self.coordinates.insert(0, self.head)   
    def _go_down(self):
        self.head = Point(self.head.x, (self.head.y + SETTINGS.BLOCK_SIZE.value))
        self.coordinates.insert(0, self.head)     
    def _go_right(self):
        self.head = Point((self.head.x + SETTINGS.BLOCK_SIZE.value), self.head.y)
        self.coordinates.insert(0, self.head)     
    def _go_left(self):
        self.head = Point((self.head.x - SETTINGS.BLOCK_SIZE.value), self.head.y)
        self.coordinates.insert(0, self.head)  