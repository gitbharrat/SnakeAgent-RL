import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.SysFont('arial.ttf',25)


class Direction(Enum):
    RIGHT = 1
    LEFT =  2
    UP =    3
    DOWN =  4


Point = namedtuple("Point", "x, y")

#RGB Colors
WHITE   = (255,255,255)
BLACK   = (0,0,0)
RED     = (200,0,0)
BLUE1   = (0,0,255)
BLUE2   = (0,100,255)
GREY    = (50,50,50)
GREEN   = (0,110,0)


#Parameters
BLOCK_SIZE  = 20
SPEED       = 200


class SnakeGameAI:

 
    def __init__(self, width=640, height=480) -> None:
        self.width      = width
        self.height     = height

        # Display Window
        self.display    = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Agent")
        
        self.clock      = pygame.time.Clock()
        self.reset()

    def reset(self):

        # Initialize Game State
        self.direction  = Direction.RIGHT
        self.head       = Point(self.width/2, self.height/2)
        self.snake      = [self.head, 
                            Point(self.head.x - BLOCK_SIZE, self.head.y),
                            Point(self.head.x - (2*BLOCK_SIZE), self.head.y)]
        self.score      = 0
        self.food       = Point(None, None)
        self.speed      = SPEED

        self._place_food()
        self.frame_iteration = 0

    
    def _place_food(self) -> None:
        x = random.randint(0, (self.width - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    
    def play_step(self, action):
        
        self.frame_iteration += 1

        # Capture User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Move the Block
        self._move(action)
        self.snake.insert(0, self.head)

        # Check if Game Over
        reward = 0
        game_over = False
        if self._is_collision() or self.frame_iteration > 100*len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score

        # Update New food
        if self.head == self.food:
            self.score += 1
            reward = 10
            self.speed += 0.5
            self._place_food()
        else:
            self.snake.pop()

        # Update UI and Clock
        self._update_ui()
        self.clock.tick(self.speed)
        
        return reward, game_over, self.score


    def _is_collision(self, pt=None) -> bool:
        if pt is None:
            pt = self.head

        # Hits Boundary
        if self.head.x > (self.width - BLOCK_SIZE) or self.head.x < 0:
            return True
        if self.head.y > (self.height - BLOCK_SIZE) or self.head.y < 0:
            return True
        if self.head in self.snake[1:]:
            return True
        
        return False

    def _update_ui(self) -> None:
        self.display.fill(GREEN)

        for pt in self.snake:
            pygame.draw.rect(self.display,GREEN,pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE),1)
            pygame.draw.rect(self.display,GREY,pygame.Rect(pt.x+3, pt.y+3, 16,16))

        pygame.draw.rect(self.display,GREEN,pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE),1)
        pygame.draw.rect(self.display,GREY,pygame.Rect(self.food.x+3, self.food.y+3, 16, 16))

        text = font.render("Score:" + str(self.score), True, GREY)
        self.display.blit(text, [0,0])
        pygame.display.flip()


    def _move(self, action):
        clock_wise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clock_wise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            # No Change
            new_dir = clock_wise[idx]
        elif np.array_equal(action, [0,1,0]):
            # Right Turn
            next_idx = (idx + 1) % 4
            new_dir = clock_wise[next_idx]
        else:
            # Left Turn
            next_idx = (idx - 1) % 4
            new_dir = clock_wise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)

