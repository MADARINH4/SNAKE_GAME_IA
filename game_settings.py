from enum import Enum
from collections import namedtuple

Point = namedtuple('Point', 'x, y')

class DIRECTION(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
class COLORS(Enum):
    WHITE = (255, 255, 255)    
    RED = (200, 0, 0)    
    BLUE1 = (0, 0, 255)    
    BLUE2 = (0, 100, 255)    
    BLACK = (0, 0, 0)
    
class SETTINGS(Enum):    
    BLOCK_SIZE = 20    
    SPEED = 50
    GAME_WIDTH = 640
    GAME_HEIGHT = 480
    MAX_MEMORY = 100_000
    BATCH_SIZE = 1000
    LR = 0.001
        