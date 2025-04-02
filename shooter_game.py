#Создай собственный Шутер!
from pygame import *
font.init()
from random import randint
import time as t
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, QRadioButton, QGroupBox, QButtonGroup

mixer.init()
font.init()

game = True
mixer.music.load("war_music.mp3")
win = display.set_mode((700, 500))
win_height = 500
win_width = 700
display.set_caption("Битва на самолётах: Оборона Москвы")
icon = transform.scale(image.load("ww2_image.jpeg"), (35,35))
display.set_icon(icon)
background = transform.scale(image.load("war_back.png"), (700, 500))
mixer.music.play(-1)
mixer.music.set_volume(0.5)


clock = time.Clock()
FPS = 60
finish = 0
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        self.speed = player_speed

    def reset(self):
        win.blit(self.image,(self.rect.x, self.rect.y))

class Player(GameSprite):
    cooldown = 0
    def update(self):
        self.cooldown -= 1
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 630:
            self.rect.x += self.speed
        if keys_pressed[K_SPACE] and self.cooldown <= 0:
            bullets.add(Bullet("bullet_762.png", self.rect.centerx, self.rect.top, 30, 30, 4))
            self.cooldown = 30



class Enemy(GameSprite):
    def respawn(self):
        self.rect.x = randint(0, win_width - 80)
        self.rect.y = randint(-70 - 50, -70)
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.respawn()
            plane.lost = plane.lost + 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y == 0:
            self.kill()
        
        

plane = Player("player_plane.png",300, 400, 70, 70, 5)
plane.lost = -4
win_points = 0
lost_font = font.SysFont("Arial", 30)
lost_font1 = lost_font.render('Пропущено: ' + str(plane.lost), 1, (0, 0, 0))
win_font = font.SysFont("Arial", 30)
win_font1 = win_font.render('Сбито: ' + str(win_points), 1, (0, 0, 0))
enemy_planes = sprite.Group()
bullets = sprite.Group()
for i in range(4):
    enemy_planes.add(Enemy("enemy_plane.png",1000, 1000, 70, 70, 2))


while game:
    if plane.lost == 5:
        lose_font = font.SysFont("Arial", 30)
        lose_font1 = lose_font.render('ПОРАЖЕНИЕ! Немцы вошли в Москву.', 1, (255, 0, 0))
        finish = -1
    if win_points == 20:
        victory_font = font.SysFont("Arial", 30)
        victory_font1 = victory_font.render('ПОБЕДА! Немцы отступили от Москвы!', 1, (0, 0, 128))
        finish = 1  
    lost_font1 = lost_font.render('Пропущено: ' + str(plane.lost), 1, (0, 0, 0))
    win_font1 = win_font.render('Сбито: ' + str(win_points), 1, (0, 0, 0))
    win.blit(background, (0, 0))
    if finish == -1:
        win.blit(lose_font1, (170,250))
    if finish == 1:
        win.blit(victory_font1, (170,250))
    for a in event.get():
        if a.type == QUIT:
            game = False
    if finish != 1 and finish != -1:
        win.blit(background, (0,0))
        plane.update()
        enemy_planes.update()
        bullets.update()
        win.blit(lost_font1, (50,50))
        win.blit(win_font1, (50,100))

        sprites_collide = sprite.groupcollide(enemy_planes, bullets, True, True)
        for i in sprites_collide:
            enemy_planes.add(Enemy("enemy_plane.png",1000, 1000, 70, 70, 2))
            plane.lost -= 1
            win_points += 1
        plane.reset()
        enemy_planes.draw(win)
        bullets.draw(win)
        

    clock.tick(FPS)
    display.update()