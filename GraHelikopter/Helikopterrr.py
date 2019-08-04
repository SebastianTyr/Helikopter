import pygame
import os
import random
import math

pygame.init()
w = 600
h = 600
screen = pygame.display.set_mode((w,h))

def write(text,x, y, size):
    font = pygame.font.SysFont("Arial", size)
    rend = font.render(text, 1, (255,100,100))
    # x = (w - rend.get_rect().width)/2 Wyśrodkowanie napisu
    # y = (h - rend.get_rect().height)/2
    screen.blit(rend, (x,y))
    
_display = "end"

class Obstacle():
    def __init__(self, x, width):
        self.x = x
        self.width = width
        self.y_up = 0
        self.height_up = random.randint(150,250)
        self.space = 250
        self.y_down = self.height_up + self.space
        self.height_down = h - self.y_down
        self.color = (160,140,190)
        self.form_up = pygame.Rect(self.x, self.y_up, self.width, self.height_up)
        self.form_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)
    def draw(self):
        pygame.draw.rect(screen, self.color, self.form_up, 0)
        pygame.draw.rect(screen, self.color, self.form_down, 0)
    def move(self, v):
        self.x = self.x - v
        self.form_up = pygame.Rect(self.x, self.y_up, self.width, self.height_up)
        self.form_down = pygame.Rect(self.x, self.y_down, self.width, self.height_down)
    def collision(self, player):
        if self.form_up.colliderect(player) or self.form_down.colliderect(player):
            return True
        else:
            return False
        
class Helicopter():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 30
        self.height = 50
        self.form = pygame.Rect(self.x, self.y, self.width, self.height)
        self.graph = pygame.image.load(os.path.join('helicoptrr.png'))
    def draw(self):
        screen.blit(self.graph, (self.x, self.y))
    def move(self ,v):
        self.y = self.y + v
obstacle = []
for i in range(21):
    obstacle.append(Obstacle(i*w/20, w/20))
    
game = Helicopter(250,250)
dy = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                dy = -0.5
            elif event.key == pygame.K_DOWN:
                dy = 0.5
            if event.key == pygame.K_SPACE:
                if _display != "play":
                    player = Helicopter(250,250)
                    dy = 0
                    _display = "play"
                    score = 0
    screen.fill((0,0,0))
    
    if _display == "menu":
        write("Naciśnij spację, aby zacząć", 80, 290, 40)
        logo = pygame.image.load(os.path.join('logo.png'))
        screen.blit(logo, (80,30))
    elif _display == "play":
        for o in obstacle:
            o.move(1)
            o.draw()
            if o.collision(game.form):
                _display = "end"
        for o in obstacle:
            if o.x <= -o.width:
                obstacle.remove(o)
                obstacle.append(Obstacle(w, w/20))
                score = score + math.fabs(dy)
        game.draw()
        game.move(dy)
        write("Twój wynik: " + str(score), 50, 50, 20)
    elif _display == "end":
        logo = pygame.image.load(os.path.join('logo.png'))
        screen.blit(logo, (80,30))
        write("Niestety przegrywasz", 50, 450, 20)
        write("Naciśnij spację, aby zagrać ponownie", 50, 500, 20)
        write("Twój wynik to: ", 50, 550, 20)
        
    pygame.display.update()
