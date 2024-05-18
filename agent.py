import torch
import random
import numpy
from collections import deque
from game_settings import SETTINGS, DIRECTION, Point
from snake_game_ia import SnakeGameIA
from model import Linear_QNet, QTrainer
from helper import plot

class Agent:
    def __init__(self) -> None:
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.7 # discount rate
        self.memory = deque(maxlen=SETTINGS.MAX_MEMORY.value) # popleft()
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, lr=SETTINGS.LR.value, gamma= self.gamma)
    
    def get_state(self, game):
        head = game.snake.coordinates[0]
        point_l = Point(head.x - SETTINGS.BLOCK_SIZE.value, head.y)
        point_r = Point(head.x + SETTINGS.BLOCK_SIZE.value, head.y)
        point_u = Point(head.x, head.y - SETTINGS.BLOCK_SIZE.value)
        point_d = Point(head.x, head.y + SETTINGS.BLOCK_SIZE.value)
        
        dir_l = game.direction == DIRECTION.LEFT.value
        dir_r = game.direction == DIRECTION.RIGHT.value
        dir_u = game.direction == DIRECTION.UP.value
        dir_d = game.direction == DIRECTION.DOWN.value
        
        state = [
            # Danger straight
            (dir_r and game.is_collision(point_r)) or 
            (dir_l and game.is_collision(point_l)) or 
            (dir_u and game.is_collision(point_u)) or 
            (dir_d and game.is_collision(point_d)),

            # Danger right
            (dir_u and game.is_collision(point_r)) or 
            (dir_d and game.is_collision(point_l)) or 
            (dir_l and game.is_collision(point_u)) or 
            (dir_r and game.is_collision(point_d)),

            # Danger left
            (dir_d and game.is_collision(point_r)) or 
            (dir_u and game.is_collision(point_l)) or 
            (dir_r and game.is_collision(point_u)) or 
            (dir_l and game.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            game.food.coordinates.x < game.snake.head.x,  # food left
            game.food.coordinates.x > game.snake.head.x,  # food right
            game.food.coordinates.y < game.snake.head.y,  # food up
            game.food.coordinates.y > game.snake.head.y  # food down
        ]
        return numpy.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft()
    
    def train_long_memory(self):
        if len(self.memory) > SETTINGS.BATCH_SIZE.value:
            mini_sample = random.sample(self.memory, SETTINGS.BATCH_SIZE.value) # List of tuples
        else:    
            mini_sample = self.memory
            
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
            
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)
    
    def get_action(self, state):
        # Random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1
            
        return final_move
    
def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameIA()
    while True:
        # Get old state
        state_old = agent.get_state(game)
        
        # Get move
        final_move = agent.get_action(state_old)
        
        # Perform move and get nwe move
        reward, done, score = game.play_step(final_move)
        state_new = agent.get_state(game)
        
        # Train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        
        # Remember
        agent.remember(state_old, final_move, reward, state_new, done)
        
        if done:
            # Train long memory, plot result
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()
            
            if score > record:
                record = score
                agent.model.save()
                
            print("Game", agent.n_games, 'Score', score, 'Record', record)
            
            plot_scores.append(score)
            total_score += score
            mean_scores = total_score / agent.n_games
            plot_mean_scores.append(mean_scores)
            plot(plot_scores, plot_mean_scores)
            
if __name__ == '__main__':
    train()
