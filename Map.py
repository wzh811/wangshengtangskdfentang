# -*- coding:utf-8 -*-

import pygame as pg
from random import randint
from Settings import *
from Monster import Monster
import os


class Chest(pg.sprite.Sprite):
    def __init__(self,index):
        super().__init__()
        k = WindowSettings.outdoorScale
        self.x = randint(100, WindowSettings.width * k - 100)
        self.y = randint(100, WindowSettings.height * k - 100)
        self.image = pg.image.load(GamePath.chest)
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.index = index
        self.lvl = (index+1)//2

    def update_pos(self,x,y):
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def update(self, dx, dy):
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy


def gen_wild_map(player):
    images = [pg.image.load(tile) for tile in GamePath.groundTiles]
    images = [pg.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]
    m = open(GamePath.saves + "\\" + player.name + "\\" + "wild_map.txt", 'w')
    map_Obj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            k = randint(0, len(images) - 1)
            tmp.append(images[k])
            m.write(str(k))
        m.write("\n")
        map_Obj.append(tmp)
    m.close()

    return map_Obj


def load_wild_map(player_name):
    images = [pg.image.load(tile) for tile in GamePath.groundTiles]
    images = [pg.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    map_Obj = []
    m = open(GamePath.saves + "\\" + player_name + "\\" + "wild_map.txt", 'r')
    lines = m.readlines()
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            k = lines[i][j]
            tmp.append(images[int(k)])
        map_Obj.append(tmp)
    m.close()

    return map_Obj


def gen_city_map(player):
    images = [pg.image.load(tile) for tile in GamePath.cityTiles]
    images = [pg.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    map_Obj = []
    m = open(GamePath.saves + "\\" + player.name + "\\" + "city_map.txt", 'w')
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            k = randint(0, len(images) - 1)
            tmp.append(images[k])
            m.write(str(k))
        map_Obj.append(tmp)
        m.write("\n")
    m.close()

    return map_Obj


def load_city_map(player_name):
    images = [pg.image.load(tile) for tile in GamePath.cityTiles]
    images = [pg.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]

    map_Obj = []
    m = open(GamePath.saves + "\\" + player_name + "\\" + "city_map.txt", 'r')
    lines = m.readlines()
    for i in range(SceneSettings.tileXnum):
        tmp = []
        for j in range(SceneSettings.tileYnum):
            k = lines[i][j]
            tmp.append(images[int(k)])
        map_Obj.append(tmp)
    m.close()

    return map_Obj


def gen_chests(player_name):
    chests = []
    if os.path.isfile(GamePath.saves + "\\" + player_name + "\\" + "chests.txt"):
        n = open(GamePath.saves + "\\" + player_name + "\\" + "chests.txt", 'r')
        lines = n.readlines()
        for line in lines:
            infor = line[:-1].split(',')
            index = infor[2]
            x = infor[0]
            y = infor[1]
            chest = Chest(int(index))
            chest.update_pos(int(x), int(y))
            chests.append(chest)
        n.close()
    else:
        n = open(GamePath.saves + "\\" + player_name + "\\" + "chests.txt", 'w')
        for i in range(1,21):
            lvl = (i + 1) // 2
            chest = Chest(i)
            chest.lvl = lvl
            x = randint(540 + chest.lvl * 300, 800 + chest.lvl * 300)
            y = randint(600, WindowSettings.height * WindowSettings.outdoorScale - 500)
            chest.update_pos(x, y)
            n.write(f"{chest.x},{chest.y},{chest.index}\n")
            chests.append(chest)
        n.close()
    return chests


def load_monsters(player_name):
    # 从存档中读取怪物位置
    m = open(GamePath.saves + "\\" + player_name + "\\" + "monsters.txt", 'r')
    lines = m.readlines()
    monsters = []
    for line in lines:
        x, y, lvl = map(int, line.split(','))
        monster = Monster(lvl, player_name)
        monster.x = x
        monster.rect.x = x
        monster.y = y
        monster.rect.y = y
        monsters.append(monster)
    m.close()
    return monsters
