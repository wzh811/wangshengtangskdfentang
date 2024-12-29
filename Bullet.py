# -*- coding:utf-8 -*-
import math

import pygame as pg
from Settings import *
from random import randint


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, num, m_x=0, m_y=0, atk=0, alive=True):
        super().__init__()
        self.x = x
        self.y = y
        self.delete = not alive
        self.type = num
        self.atk = atk
        self.image = pg.image.load(GamePath.bullet[num])
        self.image = pg.transform.scale(self.image, (BulletSettings.bulletWidth[num], BulletSettings.bulletHeight[num]))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        speed = BulletSettings.bulletSpeed[num]
        if num == 0 or num == 2 or num == 4:
            if m_x == x:
                if m_y > y:
                    self.direction_x = 0
                    self.direction_y = speed
                else:
                    self.direction_x = 0
                    self.direction_y = -speed
            else:
                d = ((m_y - y) ** 2 + (m_x - x) ** 2)**0.5
                self.direction_x = speed * ((m_x - x) / d)
                self.direction_y = speed * ((m_y - y) / d)
            # print(self.direction_y, self.direction_x)

    def update(self):
        self.rect.x = self.rect.x+self.direction_x
        self.rect.y = self.rect.y+self.direction_y
        if self.rect.y <= 0 or self.rect.x <= 0 or self.rect.y > WindowSettings.height or self.rect.x > WindowSettings.width:
            self.delete = True


class Bomb(Bullet):
    def __init__(self, x, y, num, m_x=0, m_y=0, atk=0, alive=True, index=0):
        super().__init__(x, y, num, m_x, m_y, atk, alive)
        self.direction_y = 0
        self.direction_x = 0
        self.timer = BulletSettings.bombTimer
        self.delete = not alive
        self.index = index

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            pg.mixer.Sound(GamePath.sound['bomb']).play()
            self.delete = True

    def fix_to_middle(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy


class Circle(Bullet):
    def __init__(self, x, y, num, m_x=0, m_y=0, atk=0, radius=120, alive=True):
        super().__init__(x, y, num, m_x, m_y, atk, alive)
        self.direction_y = 0
        self.direction_x = 0
        self.delete = not alive
        self.radius = radius
        self.angle = 0
        self.timer = BulletSettings.circleTimer

    def update(self, m_x=0, m_y=0):
        self.angle += 15
        if self.angle > 360:
            self.angle = 0
        self.timer -= 1
        radians = self.angle*(math.pi / 180)
        x = m_x + self.radius*math.cos(radians)
        y = m_y + self.radius*math.sin(radians)
        self.rect.center = (int(x), int(y))
        if self.timer <= 0:
            self.delete = True
            self.kill()
