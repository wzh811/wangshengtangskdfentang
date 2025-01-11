# -*- coding:utf-8 -*-

import pygame as pg
from random import randint
from Settings import *
from Monster import Monster
import os


class Chest(pg.sprite.Sprite):
    def __init__(self, index):
        super().__init__()
        k = WindowSettings.outdoorScale
        self.x = randint(100, WindowSettings.width * k - 100)
        self.y = randint(100, WindowSettings.height * k - 100)
        self.image = pg.image.load(GamePath.chest)
        self.image = pg.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.index = index
        self.lvl = (index + 1) // 2

    def update_pos(self, x, y):
        self.x = x
        self.y = y
        self.rect.center = (x, y)

    def update(self, dx, dy):
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy


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
        for i in range(1, 21):
            lvl = (i + 1) // 2
            chest = Chest(i)
            chest.lvl = lvl
            x = (i - 1) // 2 * 360 + 240
            if i % 2 == 1:
                y = randint(760, 1140)
            else:
                y = randint(1640, 2000)
            chest.update_pos(x, y)
            n.write(f"{chest.x},{chest.y},{chest.index}\n")
            modify_city_map(player_name=player_name, chest_pos=(x, y))
            chests.append(chest)
        n.close()
    return chests


def modify_city_map(player_name, chest_pos):
    tileX = chest_pos[0] // 40
    tileY = chest_pos[1] // 40
    if tileY < 35:
        mod_tiles = [(tileX, Y) for Y in range(tileY + 1, 34)]
        mod_tiles.extend([(tileX + 1, Y) for Y in range(tileY + 1, 34)])
    else:
        mod_tiles = [(tileX, Y) for Y in range(37, tileY + 3)]
        mod_tiles.extend([(tileX + 1, Y) for Y in range(37, tileY + 3)])
    print(mod_tiles)
    m = open(GamePath.saves + "\\" + player_name + "\\" + "city_map.txt", 'r+')
    lines = m.readlines()
    tiles = [list(line.strip()) for line in lines]

    for i in range(SceneSettings.tileXnum):
        for j in range(SceneSettings.tileYnum):
            if (i, j) in mod_tiles:
                tiles[i][j] = '6'
    m.seek(0)
    m.writelines([''.join(line) + '\n' for line in tiles])
    m.truncate()
    m.close()


class Obstacle(pg.sprite.Sprite):
    def __init__(self, index, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pg.image.load(GamePath.obstacles[index])
        self.image = pg.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.index = index

    def update(self, dx, dy):
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy


def gen_barrier():
    tiles = [(x * 40, 0) for x in range(0, 96)]
    tiles.extend([(x * 40, 2120) for x in range(0, 96)])
    tiles.extend([(0, y * 40) for y in range(1, 53)])
    tiles.extend([(3800, y * 40) for y in range(1, 53)])
    tiles.extend([(x * 40, 720) for x in range(4, 53)])
    barriers = []
    for i in tiles:
        barrier = Obstacle(index=1, x=i[0], y=i[1])
        barriers.append(barrier)
    return barriers


def gen_wild_obstacle(player_name):
    obstacles = []
    tiles = []
    if os.path.isfile(GamePath.saves + "\\" + player_name + "\\" + "wild_obstacles.txt"):
        n = open(GamePath.saves + "\\" + player_name + "\\" + "wild_obstacles.txt", 'r')
        lines = n.readlines()
        for line in lines:
            infor = line[:-1].split(',')
            x = int(infor[0])
            y = int(infor[1])
            obstacle = Obstacle(index=0, x=x, y=y)
            obstacles.append(obstacle)
    else:
        m = open(GamePath.saves + "\\" + player_name + "\\" + "wild_map.txt", 'r+')
        n = open(GamePath.saves + "\\" + player_name + "\\" + "wild_obstacles.txt", 'w')
        lines = m.readlines()
        m.close()
        for x in range(1, len(lines)):
            line = lines[x].strip()
            for y in range(1, len(line)):
                if line[y] == '6' and line[y + 1] != '6' and line[y + 1] != '0':
                    tiles.append((x * 40, y * 40 + 40))
                if line[y] == '6' and line[y - 1] != '6' and line[y - 1] != '0':
                    tiles.append((x * 40, y * 40 - 40))
                if line[y] == '6' and lines[x + 1][y] != '6' and lines[x + 1][y] != '0':
                    tiles.append((x * 40 + 40, y * 40))
                if line[y] == '6' and lines[x - 1][y] != '6' and lines[x - 1][y] != '0':
                    tiles.append((x * 40 - 40, y * 40))
        tiles = tuple(set(tiles))
        for i in tiles:
            if i[1] <= 720:
                continue
            obstacle = Obstacle(index=0, x=i[0], y=i[1])
            n.write(str(i[0]) + ',' + str(i[1]) + '\n')
            obstacles.append(obstacle)
        n.close()
    return obstacles


def gen_city_obstacle(player_name):
    obstacles = []
    tiles = []
    if os.path.isfile(GamePath.saves + "\\" + player_name + "\\" + "city_obstacles.txt"):
        n = open(GamePath.saves + "\\" + player_name + "\\" + "city_obstacles.txt", 'r')
        lines = n.readlines()
        for line in lines:
            infor = line[:-1].split(',')
            x = int(infor[0])
            y = int(infor[1])
            obstacle = Obstacle(index=0, x=x, y=y)
            obstacles.append(obstacle)
    else:
        m = open(GamePath.saves + "\\" + player_name + "\\" + "city_map.txt", 'r+')
        n = open(GamePath.saves + "\\" + player_name + "\\" + "city_obstacles.txt", 'w')
        lines = m.readlines()
        m.close()
        for x in range(1, len(lines)):
            line = lines[x].strip()
            for y in range(1, len(line)):
                if line[y] == '6' and line[y + 1] != '6' and line[y + 1] != '0':
                    tiles.append((x * 40, y * 40 + 40))
                if line[y] == '6' and line[y - 1] != '6' and line[y - 1] != '0':
                    tiles.append((x * 40, y * 40 - 40))
                if line[y] == '6' and lines[x + 1][y] != '6' and lines[x + 1][y] != '0':
                    tiles.append((x * 40 + 40, y * 40))
                if line[y] == '6' and lines[x - 1][y] != '6' and lines[x - 1][y] != '0':
                    tiles.append((x * 40 - 40, y * 40))
        tiles = tuple(set(tiles))
        for i in tiles:
            if i[1] <= 720:
                continue
            obstacle = Obstacle(index=0, x=i[0], y=i[1])
            n.write(str(i[0]) + ',' + str(i[1]) + '\n')
            obstacles.append(obstacle)
        n.close()
    return obstacles
