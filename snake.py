import pygame
import random
from enum import Enum
from collections import namedtuple

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
SPEED       = 2


class SnakeGame:

 
    def __init__(self, width=640, height=480) -> None:
        self.width      = width
        self.height     = height

        # Display Window
        self.display    = pygame.display.set_mode((self.width, self.height))
        self.clock      = pygame.time.Clock()
        
        pygame.display.set_caption("Snake Agent")

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

    
    def _place_food(self) -> None:
        x = random.randint(0, (self.width - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.height - BLOCK_SIZE)//BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x,y)
        if self.food in self.snake:
            self._place_food()

    
    def play_step(self):

        # Capture User Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

        # Move the Block
        self._move(self.direction)
        self.snake.insert(0, self.head)

        # Check if Game Over
        game_over = False
        if self._is_collision():
            game_over = True
            return game_over, self.score

        # Update New food
        if self.head == self.food:
            self.score += 1
            self.speed += 0.5
            self._place_food()
        else:
            self.snake.pop()

        # Update UI and Clock
        self._update_ui()
        self.clock.tick(self.speed)
        
        return game_over, self.score


    def _is_collision(self) -> bool:
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


    def _move(self, direction):
        x = self.head.x
        y = self.head.y

        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x,y)


if __name__ == '__main__':
    game = SnakeGame()

    # Game Loop
    while True:
        game_over, score = game.play_step()

        if game_over == True:
            break

    print('Final Score:',score)
    pygame.quit()


