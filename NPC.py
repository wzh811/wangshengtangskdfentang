# -*- coding:utf-8 -*-

import pygame as pg
from Settings import *
from random import randint


class NPC(pg.sprite.Sprite):
    def __init__(self, num, player_name):
        super().__init__()
        k = WindowSettings.outdoorScale
        # self.x = randint(100, WindowSettings.width*k-100)
        # self.y = randint(100, WindowSettings.height*k-100)
        if num == 0:
            self.x = 100
            self.y = 100
        elif num == 1:
            self.x = 300
            self.y = 100
        elif num == 2:
            self.x = 500
            self.y = 100
        elif num == 3:
            self.x = 1000
            self.y = 100
        elif num == 4:
            self.x = 300
            self.y = 400
        self.image = pg.image.load(GamePath.NPC[num])
        self.image = pg.transform.scale(self.image, (NPCSettings.NPCWidth, NPCSettings.NPCHeight))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.talking = False
        self.id = num
        self.talk_CD = 0
        self.talked = False
        n = open(GamePath.saves + "\\" + player_name + "\\" + "NPCs.txt", 'a+')
        talking = 1 if self.talking else 0
        talked = 1 if self.talking else 0
        n.seek(0)
        if n.readlines:
            for line in n.readlines():
                if line.split(',')[0] == str(self.id):
                    break
            else:
                n.write(f'{self.id},{self.talk_CD},{talking},{talked}\n')
        n.close()

    def update(self, dx, dy):
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy
        self.talk_CD -= 1
        if self.talk_CD < 0:
            self.talk_CD = 0

    def can_talk(self):
        if self.talk_CD > 0:
            return False
        else:
            return not self.talking

    def reset_talk_CD(self):
        self.talk_CD = 150
