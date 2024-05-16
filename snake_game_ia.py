import pygame

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
        
        #Init game state
        self.score = 0
        self.direction = DIRECTION.RIGHT.value
        self.snake = Snake()
        self.food = None
        self._place_food()
        
    def  _place_food(self):
        self.food = Food()
        #Verify (X, Y) the food its the same of snake
        if self.food.coordinates in self.snake.coordinates:
            self._place_food()  

    def _move(self, direction):
        if direction == DIRECTION.RIGHT.value:
            self.snake._go_right()
        elif direction == DIRECTION.LEFT.value:
            self.snake._go_left()
        elif direction == DIRECTION.DOWN.value:
            self.snake._go_down()
        elif direction == DIRECTION.UP.value:
            self.snake._go_up()
            
    def _is_collision(self):
        #Hits boundary
        if self.snake.head.x > self.w - SETTINGS.BLOCK_SIZE.value or self.snake.head.x < 0 or self.snake.head.y > self.h - SETTINGS.BLOCK_SIZE.value or self.snake.head.y < 0:
            return True
        #Hits itself
        if self.snake.head in self.snake.coordinates[1:]:
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
        
    def play_step(self):
        #Collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if self.direction != DIRECTION.RIGHT.value:
                        self.direction = DIRECTION.LEFT.value
                elif event.key == pygame.K_RIGHT:
                    if self.direction != DIRECTION.LEFT.value:
                        self.direction = DIRECTION.RIGHT.value
                elif event.key == pygame.K_UP:
                    if self.direction != DIRECTION.DOWN.value:
                        self.direction = DIRECTION.UP.value
                elif event.key == pygame.K_DOWN:
                    if self.direction != DIRECTION.UP.value:
                        self.direction = DIRECTION.DOWN.value
                elif event.key == pygame.K_a:
                    if self.direction != DIRECTION.RIGHT.value:
                        self.direction = DIRECTION.LEFT.value
                elif event.key == pygame.K_d:
                    if self.direction != DIRECTION.LEFT.value:
                        self.direction = DIRECTION.RIGHT.value
                elif event.key == pygame.K_w:
                    if self.direction != DIRECTION.DOWN.value:
                        self.direction = DIRECTION.UP.value
                elif event.key == pygame.K_s:
                    if self.direction != DIRECTION.UP.value:
                        self.direction = DIRECTION.DOWN.value
        #Move
        self._move(self.direction) #Update the head of snake
        #Check if game over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score
        #Place a new food or just move
        if self.snake.head == self.food.coordinates:
            self.score += 1
            self._place_food()
        else:
            self.snake.coordinates.pop()
        #Update ui an clock
        self._update_ui()
        self.clock.tick(SETTINGS.SPEED.value)
        #Finally
        return game_over, self.score         

if __name__ == '__main__':
    game = SnakeGameIA()
    
    #Game loop
    while True:
        game_over, score = game.play_step()
        
        if game_over == True:
            break
        
    print('Final Score: {}'.format(score))
    
    pygame.quit()