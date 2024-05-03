# Imports
import sys
from os import path
from time import sleep
import random
import pygame
import pygame.freetype
from pygame.locals import *
import webbrowser

# settings
pygame.init()
pygame.mixer.init()
BLACK = (0, 0, 0)
RED = (255,0,0)
YELLOW = (255,255,0)
WHITE = (255, 255, 255)
size = width, height = ((1024, 1024))
FPS = 60
score = 1
font = pygame.font.Font("8-BIT WONDER.TTF", 16)
font2 = pygame.font.Font("8-BIT WONDER.TTF", 80)
laser_sound = pygame.mixer.Sound("laser.mp3")
enemy_kill_sound = pygame.mixer.Sound("enemy_kill.wav")

# Screen
screen = pygame.display.set_mode(size, 0, 32)
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, 1000)


# images
ship = pygame.image.load("ship.png")
enemy = pygame.image.load("enemy1.png").convert_alpha()
enemy.set_colorkey((255,255,255))
enemy = enemy.convert()
background  = pygame.image.load("background.png")
background = pygame.transform.scale(background, size)
background = background.convert()
menu1 = pygame.image.load("menu1.png")
menu1 = pygame.transform.scale(menu1, size)
menu1 = menu1.convert()
menu2 = pygame.image.load("menu2.png")
menu2 = pygame.transform.scale(menu2, size)
menu2 = menu2.convert()
credits = pygame.image.load("credits.png")
credits = pygame.transform.scale(credits, size)
credits = credits.convert()
finalScore = pygame.image.load("final score.png")
finalScore = pygame.transform.scale(finalScore, size)
finalScore = finalScore.convert()
heart = pygame.image.load("heart.png")
heart = pygame.transform.scale(heart, (44, 44))


# ship
class Ship(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = ship
        self.rect = self.image.get_rect()
        self.rect.centerx = width/2
        self.rect.y = 930
        self.speed_x = 0


    def movement(self):
        self.speed_x = 0
        events = pygame.key.get_pressed()
        if events[pygame.K_a] or events[pygame.K_LEFT]:
            self.speed_x = -13
        elif events[pygame.K_d] or events[pygame.K_RIGHT]:
            self.speed_x = 13
        self.rect.centerx += self.speed_x

    def boundary(self):
        if self.rect.left < 0:
            self.rect.left = -5
        elif self.rect.right > width:
            self.rect.right = width +10

    def update(self):
        self.movement()
        self.boundary()

# shots
class Shot(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((3,8))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.speed_y = -15
        self.rect.x = ship.rect.centerx
        self.rect.y = 930

    def update(self):
        self.rect.y = self.rect.y + self.speed_y
        if self.rect.bottom < 0:
            self.kill()


class Hearts(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = heart
        self.rect = self.image.get_rect()
        self.rect.x = 156
        # self.image2 = heart
        # self.rect2 = self.image2.get_rect()
        # self.rect1.x = 206
        # self.image3 = heart
        # self.rect3 = self.image3.get_rect()
        # self.rect1.x = 256
        # self.rect1.y = 14
        # self.rect2.y = 14
        self.rect.y = 14

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.speed_y = random.randint(4, 8)
        self.image = enemy
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, 1000)
        self.rect.y = 0

    def update(self):
        self.rect.y = self.rect.y + self.speed_y
        if self.rect.y > 1024:
            self.kill()
            Variables.lives -= 1


# message to screen
def message_to_screen(message, color, font_size, x, y):
    text = font.render(message, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)

def final_score_text(message, color, font_size, x, y):
    text = font2.render(message, True, BLACK)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    screen.blit(text, text_rect)


# global variables
class Variables():
    score = 1
    counter = 30
    lives = 3


# Group all spirtes
all_sprites = pygame.sprite.Group()
all_enemies = pygame.sprite.Group()
all_shots = pygame.sprite.Group()

ship = Ship()
all_sprites.add(ship)


# main game loop
def game():
    while (Variables.counter > 0 and Variables.lives > 0):

        # draw to screen
        screen.blit(background,(0,0))

        message_to_screen(str(Variables.score) + " Points", RED, 32, 940, 32)
        message_to_screen("Time " + str(Variables.counter), RED, 32, 80, 32 )
        while len(all_enemies) < 8:
            new_enemy = Enemy()
            all_sprites.add(new_enemy)
            all_enemies.add(new_enemy)


        heart1 = Hearts()
        hearts = []
        clock.tick(FPS)

        # check for events
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == USEREVENT:
                Variables.counter -= 1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    new_shot = Shot()
                    pygame.mixer.Sound.play(laser_sound)
                    pygame.mixer.music.stop()
                    all_shots.add(new_shot)
                    all_sprites.add(new_shot)

        # check if a shot is in the rectangle of an enemy sprite, if so, kill enemy and shot
        collision = pygame.sprite.groupcollide(all_shots, all_enemies, True, True)
        if collision:
            pygame.mixer.Sound.play(enemy_kill_sound)
            Variables.score +=  50

        # for enemy in all_enemies:
        #     if enemy.rect.y > 1000:
        #         Variables.lives = Variables.lives - 1
        #         print(Variables.lives)

        # update all sprites

        for i in range(Variables.lives):
            hearts.append(heart)
            screen.blit(hearts[i],(156  + (50 * i), 14))
        all_sprites.update()
        all_sprites.draw(screen)
        pygame.display.update()
        clock.tick(FPS)
    final_score()


# end of game loop
def menu():
    while True:

        clock.tick(FPS)
        screen.blit(menu1,(0,0))
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                    othermenu()
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    game()

        pygame.display.update()
        screen.blit(menu1,(0,0))

def othermenu():
    while True:
        screen.blit(menu2,(0,0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_w or event.key == pygame.K_UP:
                    menu()
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN  or event.key == pygame.K_SPACE:
                    credit()


        pygame.display.update()
        clock.tick(FPS)

def credit():
    while True:
        screen.blit(credits,(0,0))
        # pygame.Rect(left, top, width, height)
        rect = pygame.Rect(275, 545, 530, 30)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    game()
                elif event.key == pygame.K_BACKSPACE:
                    othermenu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                if rect.collidepoint(pos):
                    webbrowser.open("https://github.com/gutoarraes")


        pygame.display.update()
        clock.tick(FPS)

def final_score():
    sleep(1)
    while True:
        screen.blit(finalScore,(0,0))
        final_score_text(str(Variables.score), BLACK, 70, width*0.52, height*0.5)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN  or event.key == pygame.K_SPACE:
                    Variables.counter = 30
                    Variables.score = 1
                    for enemy in all_enemies:
                        enemy.kill()
                    for shot in all_shots:
                        shot.kill()
                    game()

        pygame.display.update()
        clock.tick(FPS)

menu()

