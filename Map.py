# -*- coding:utf-8 -*-

from Objects import *


def gen_wild_map(player):
    images = [pg.image.load(tile) for tile in GamePath.groundTiles]
    images = [pg.transform.scale(image, (SceneSettings.tileWidth, SceneSettings.tileHeight)) for image in images]
    m = open(GamePath.saves + "\\" + player.name + "\\" + "wild_map.txt", 'w')
    map_Obj = []
    for i in range(SceneSettings.tileXnum):
        tmp = []
        if i == 0 or i == SceneSettings.tileXnum - 1:
            for j in range(SceneSettings.tileYnum):
                tmp.append(images[0])
                m.write('0')
        elif i == 1 or i == 2 or i == 3:
            for j in range(SceneSettings.tileYnum):
                if 9 < j < 38:
                    tmp.append(images[6])
                    m.write('6')
                elif j == 0 or j == SceneSettings.tileYnum - 1:
                    tmp.append(images[0])
                    m.write('0')
                else:
                    k = randint(1, len(images) - 2)
                    tmp.append(images[k])
                    m.write(str(k))
        else:
            for j in range(SceneSettings.tileYnum):
                if j == 0 or j == SceneSettings.tileYnum - 1:
                    tmp.append(images[0])
                    m.write('0')
                elif 33 < j < 38:
                    tmp.append(images[6])
                    m.write('6')
                else:
                    k = randint(1, len(images) - 2)
                    tmp.append(images[k])
                    m.write(str(k))
        m.write('\n')
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
        if i == 0 or i == SceneSettings.tileXnum - 1:
            for j in range(SceneSettings.tileYnum):
                tmp.append(images[0])
                m.write('0')
        elif i == 1 or i == 2 or i == 3:
            for j in range(SceneSettings.tileYnum):
                if 9 < j < 38:
                    tmp.append(images[6])
                    m.write('6')
                elif j == 0 or j == SceneSettings.tileYnum - 1:
                    tmp.append(images[0])
                    m.write('0')
                else:
                    k = randint(1, len(images) - 2)
                    tmp.append(images[k])
                    m.write(str(k))
        else:
            for j in range(SceneSettings.tileYnum):
                if j == 0 or j == SceneSettings.tileYnum - 1:
                    tmp.append(images[0])
                    m.write('0')
                elif 33 < j < 38:
                    tmp.append(images[6])
                    m.write('6')
                else:
                    k = randint(1, len(images) - 2)
                    tmp.append(images[k])
                    m.write(str(k))
        m.write('\n')
        map_Obj.append(tmp)
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
