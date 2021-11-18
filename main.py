import pygame
from pygame.locals import *
import time
import random

Size = 40
Background_Color = (3, 255, 49)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("./resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = Size*3
        self.y = Size*3

    def draw(self):

        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    
    def move(self):
        self.x = random.randint(0, 19)*Size
        self.y = random.randint(0, 14)*Size

class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load("./resources/block.jpg").convert()
        self.direction = 'down'

        self.length = length
        self.x = [Size]*length
        self.y = [Size]*length

    def increase(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)
        

    

    def draw(self):
        self.parent_screen.fill(Background_Color)
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
       
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    

    def walk(self):

        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i  -1]
            self.y[i] = self.y[i  -1]

        if self.direction == 'up':
            self.y[0] -= Size
        if self.direction == 'down':
            self.y[0] += Size
        if self.direction == 'left':
            self.x[0] -= Size
        if self.direction == 'right':
            self.x[0] += Size
        
        self.draw()
        

        
        

class Game:
    def __init__(self):
        pygame.init()

        self.surface = pygame.display.set_mode((800, 600))
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + Size:
            if y1 >= y2 and y1 < y2 + Size:
                return True

        return False

    def sound(self, sound_name):
        if sound_name == "crash":
            sound = pygame.mixer.Sound("./resources/crash.mp3")
        elif sound_name == 'bite':
            sound = pygame.mixer.Sound("./resources/bite.mp3")

        pygame.mixer.Sound.play(sound)


    def play(self):
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.flip()

        if self.collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.sound("bite")
            self.snake.increase()
            self.apple.move()
        
        for i in range(3,self.snake.length):
            if self.collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.sound("crash")
                raise "Game Over"
        

    def score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length}", True, (255,255,255))
        self.surface.blit(score,(600,10))


    def game_over(self):
        self.surface.fill(Background_Color)
        font = pygame.font.SysFont('arial', 30)
        line = font.render(f"Game Over! Final Score: {self.snake.length}", True,(255, 0, 0))
        self.surface.blit(line, (250,270))
        line2 = font.render("To Restart Press Enter", True,(255, 0, 0))
        self.surface.blit(line2, (250,220))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):

        running = True
        pause = False
    
        while running:
            
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pause = False 

                    if not pause:   

                        if event.key == K_UP:
                            self.snake.move_up()
                        
                        if event.key == K_DOWN:
                            self.snake.move_down()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False
            try:
                if not pause:
                    self.play()

            except Exception as e:
                self.game_over()
                pause = True
                self.reset()
            

            time.sleep(.25)



if __name__ == "__main__":
    game = Game()
    game.run()



