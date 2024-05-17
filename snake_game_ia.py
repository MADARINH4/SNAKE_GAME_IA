import pygame
import numpy

#Necessary settings
from game_settings import SETTINGS, DIRECTION, COLORS

#Necessary class
from module.snake_class import Snake
from module.food_class import Food

pygame.init()
font = pygame.font.Font('arial.ttf', 25)

# Reset
# Reward
# play(action) -> direction
# game_iteration
# is_collision

class SnakeGameIA:
    def __init__(self, w=SETTINGS.GAME_WIDTH.value, h=SETTINGS.GAME_HEIGHT.value):
        self.w = w
        self.h = h
        
        #Init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Snake')
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        #Init game state
        self.score = 0
        self.direction = DIRECTION.RIGHT.value
        self.snake = Snake()
        self.food = None
        self._place_food()
        self.frame_iteration = 0
            
    def _place_food(self):
        self.food = Food()
        #Verify (X, Y) the food its the same of snake
        if self.food.coordinates in self.snake.coordinates:
            self._place_food()  

    def _move(self, action):
        # [ straight, right, left]
        clock_wise = [DIRECTION.RIGHT.value, DIRECTION.DOWN.value, DIRECTION.LEFT.value, DIRECTION.UP.value]
        idx = clock_wise.index(self.direction)
        
        if numpy.array_equal(action, [1, 0, 0]):
            new_dir = clock_wise[idx] # No change
        elif numpy.array_equal(action, [0, 1, 0]):
            next_idx = (idx + 1) % 4 # When idx = 3, next_idx return to 0
            new_dir = clock_wise[next_idx] # Right turn r -> d -> l -> u  
        else: # [0, 0, 1]
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx] # Left turn r -> u -> l -> d
        
        self.direction = new_dir   
          
        if self.direction == DIRECTION.RIGHT.value:
            self.snake._go_right()
        elif self.direction == DIRECTION.LEFT.value:
            self.snake._go_left()
        elif self.direction == DIRECTION.DOWN.value:
            self.snake._go_down()
        elif self.direction == DIRECTION.UP.value:
            self.snake._go_up()
            
    def is_collision(self, point = None):
        if point is None:
            point = self.snake.head
        #Hits boundary
        if point.x > self.w - SETTINGS.BLOCK_SIZE.value or point.x < 0 or point.y > self.h - SETTINGS.BLOCK_SIZE.value or point.y < 0:
            return True
        #Hits itself
        if point in self.snake.coordinates[1:]:
            return True
        
        return False
    
    def _update_ui(self):
        #Background of display
        self.display.fill(COLORS.BLACK.value)
        #Define display of snake
        for point in self.snake.coordinates:
            pygame.draw.rect(self.display, COLORS.BLUE1.value, pygame.Rect(point.x, point.y, SETTINGS.BLOCK_SIZE.value, SETTINGS.BLOCK_SIZE.value))
            pygame.draw.rect(self.display, COLORS.BLUE2.value, pygame.Rect(point.x+4, point.y+4, 12, 12))
        #Define display of food
        pygame.draw.rect(self.display, COLORS.RED.value, pygame.Rect(self.food.coordinates.x, self.food.coordinates.y, SETTINGS.BLOCK_SIZE.value, SETTINGS.BLOCK_SIZE.value))
        
        text = font.render("Score: "+ str(self.score), True, COLORS.WHITE.value)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def play_step(self, action):
        self.frame_iteration += 1
        #Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
        #Move
        self._move(action) #Update the head of snake
        #Check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 100*len(self.snake.coordinates):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        #Place a new food or just move
        if self.snake.head == self.food.coordinates:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.coordinates.pop()
        #Update ui an clock
        self._update_ui()
        self.clock.tick(SETTINGS.SPEED.value)
        #Finally
        return reward, game_over, self.score         