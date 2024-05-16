import random
from game_settings import SETTINGS, Point

class Food:
    def __init__(self):
        x = random.randint(0, (SETTINGS.GAME_WIDTH.value-SETTINGS.BLOCK_SIZE.value)//SETTINGS.BLOCK_SIZE.value)*SETTINGS.BLOCK_SIZE.value
        y = random.randint(0, (SETTINGS.GAME_HEIGHT.value-SETTINGS.BLOCK_SIZE.value)//SETTINGS.BLOCK_SIZE.value)*SETTINGS.BLOCK_SIZE.value
        self.coordinates = Point(x, y)