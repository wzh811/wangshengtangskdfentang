# -*- coding:utf-8 -*-

import pygame as pg
from Settings import *
from random import randint
from Bullet import Bullet, Circle
from Chat import *
import queue


class Monster(pg.sprite.Sprite):
    def __init__(self, lvl, player_name, battle=False, dfc=1.0):
        super().__init__()
        k = WindowSettings.outdoorScale
        self.image = pg.image.load(GamePath.monster[lvl])
        self.image = pg.transform.scale(self.image,
                                        (MonsterSettings.monsterWidth, MonsterSettings.monsterHeight))
        self.lvl = lvl
        self.HP = MonsterSettings.monsterHP[self.lvl]
        self.HP_text = pg.font.Font(GamePath.font, 18).render(f'敌人血量：{self.HP:.1f}', True, (255, 255, 0, 120))
        self.attack = MonsterSettings.monsterAttack[self.lvl]
        self.defence = MonsterSettings.monsterDefence[self.lvl]
        self.direction_x = 0
        self.direction_y = 0
        self.shoot_timer = 0
        self.atk_timer = 0
        self.speed = 0
        self.dfc = dfc

        self.battle = battle
        if not battle and lvl < 11:
            n = open(GamePath.saves + "\\" + player_name + "\\" + "monsters.txt", 'r+')
            n.seek(0)
            lines = n.readlines()
            if lines:
                for line in lines:
                    line = line[:-1].split(',')
                    if line[2] == str(self.lvl):
                        self.x = int(line[0])
                        self.y = int(line[1])
                        break
                else:
                    self.x = (self.lvl - 1) // 2 * 720 + 460
                    if self.lvl % 2 == 1:
                        self.y = randint(960, 1140)
                    else:
                        self.y = randint(1640, 2000)
                    n.write(f"{self.x},{self.y},{self.lvl}\n")
                    modify_wild_map(player_name=player_name, monster_pos=(self.lvl, self.y))
            else:
                self.x = (self.lvl - 1) // 2 * 720 + 460
                if self.lvl % 2 == 1:
                    self.y = randint(960, 1140)
                else:
                    self.y = randint(1640, 2000)
                n.write(f"{self.x},{self.y},{self.lvl}\n")
                modify_wild_map(player_name=player_name, monster_pos=(self.lvl, self.y))
            n.close()
        else:
            self.speed = MonsterSettings.monsterSpeed[self.lvl]
            self.x = 1000
            self.y = 800
        x = self.x
        y = self.y
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def battle_update(self, player):
        if self.battle:
            self.HP_text = pg.font.Font(GamePath.font, 18).render(f'敌人血量：{self.HP:.1f}', True, (255, 255, 0, 120))
            p_x = player.rect.x
            p_y = player.rect.y
            x = self.rect.x
            y = self.rect.y
            if p_x == x:
                if p_y > y:
                    self.direction_x = 0
                    self.direction_y = self.speed
                else:
                    self.direction_x = 0
                    self.direction_y = -self.speed
            else:
                d = ((p_y - y) ** 2 + (p_x - x) ** 2) ** 0.5
                self.direction_x = self.speed * ((p_x - x) / d)
                self.direction_y = self.speed * ((p_y - y) / d)
            self.rect.y += self.direction_y
            self.rect.x += self.direction_x
            self.shoot_timer -= 1
            self.atk_timer -= 1
            # 近战攻击
            if self.atk_timer <= 0:
                if pg.sprite.collide_rect(self, player):
                    self.atk_timer = 40 / self.dfc
                    if player.damage:
                        player.HP -= self.attack * 80 / (80 + player.defence) * (1 - player.enchantment[1])
                        pg.mixer.Sound(GamePath.sound['player_be_hit']).play()
            # 发射子弹
            if self.shoot_timer <= 0:
                bullet = Bullet(self.rect.x, self.rect.y, num=2,
                                m_x=player.rect.center[0], m_y=player.rect.center[1],
                                atk=self.attack / 2)
                self.shoot_timer = 30 / self.dfc
                return bullet

    def update(self, dx, dy):
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy


def modify_wild_map(player_name, monster_pos):
    tileX = (monster_pos[0] - 1) // 2 * 18 + 12
    tileY = monster_pos[1] // 40
    if tileY < 35:
        mod_tiles = [(tileX, Y) for Y in range(tileY + 1, 34)]
        mod_tiles.extend([(tileX + 1, Y) for Y in range(tileY + 1, 34)])
    else:
        mod_tiles = [(tileX, Y) for Y in range(37, tileY + 3)]
        mod_tiles.extend([(tileX + 1, Y) for Y in range(37, tileY + 3)])
    # print(mod_tiles)
    m = open(GamePath.saves + "\\" + player_name + "\\" + "wild_map.txt", 'r+')
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


'''
小彤：弹幕雨，圆圈式弹幕(可以使用e键与她聊天，基于大预言模型和MyMemory翻译) 
小洁：吸附玩家，涡轮绞杀(目前采用大预言模型进行出招)
(很难打！等装备好了再打！)
'''


class XiaoTong(Monster):
    def __init__(self, player_name, battle=True):
        super().__init__(11, player_name, battle)
        self.image = pg.image.load(GamePath.monster[11])
        self.image = pg.transform.scale(self.image,
                                        (NPCSettings.NPCWidth, NPCSettings.NPCHeight))
        self.HP = MonsterSettings.monsterHP[self.lvl]
        self.HP_text = pg.font.Font(GamePath.font, 18).render(f'BOSS血量：{self.HP:.1f}',
                                                              True, (255, 255, 0, 120))
        self.attack = MonsterSettings.monsterAttack[self.lvl]
        self.defence = MonsterSettings.monsterDefence[self.lvl]
        self.bullet_list1 = None
        self.bullet_list2 = None
        self.shoot_timer1 = 120
        self.shoot_timer2 = 60

    def battle_update(self, player):
        self.shoot_timer1 -= 1
        self.shoot_timer2 -= 1
        if self.bullet_list1 is None and self.shoot_timer1 <= 0:
            self.shoot_timer1 = 180
            pg.mixer.Sound(GamePath.sound['boss_shoot1']).play()
            x = [i * 0.125 * WindowSettings.width for i in range(9)]
            y = [i * 0.125 * WindowSettings.height for i in range(9)]
            self.bullet_list1 = [Bullet(x[i], 0, num=4,
                                        m_x=player.rect.center[0], m_y=player.rect.center[1],
                                        atk=self.attack // 2) for i in range(9)] + \
                                [Bullet(0, y[i], num=4,
                                        m_x=player.rect.center[0], m_y=player.rect.center[1],
                                        atk=self.attack // 2) for i in range(9)] + \
                                [Bullet(x[i], WindowSettings.height, num=4,
                                        m_x=player.rect.center[0], m_y=player.rect.center[1],
                                        atk=self.attack // 2) for i in range(9)] + \
                                [Bullet(WindowSettings.width, y[i], num=4,
                                        m_x=player.rect.center[0], m_y=player.rect.center[1],
                                        atk=self.attack // 2) for i in range(9)]
        if self.bullet_list2 is None and self.shoot_timer2 <= 0:
            self.shoot_timer2 = 200
            pg.mixer.Sound(GamePath.sound['boss_shoot2']).play()
            x = [i * 0.125 * WindowSettings.width for i in range(9)]
            y = [i * 0.125 * WindowSettings.height for i in range(9)]
            self.bullet_list2 = [Bullet(self.rect.center[0], self.rect.center[1], num=4,
                                        m_x=x[i], m_y=0,
                                        atk=self.attack // 2) for i in range(9)] + \
                                [Bullet(self.rect.center[0], self.rect.center[1], num=4,
                                        m_x=x[i], m_y=WindowSettings.height,
                                        atk=self.attack // 2) for i in range(9)] + \
                                [Bullet(self.rect.center[0], self.rect.center[1], num=4,
                                        m_x=0, m_y=y[i],
                                        atk=self.attack // 2) for i in range(9)] + \
                                [Bullet(self.rect.center[0], self.rect.center[1], num=4,
                                        m_x=WindowSettings.width, m_y=y[i],
                                        atk=self.attack // 2) for i in range(9)]
        return super().battle_update(player)


dec_queue = queue.Queue()


class XiaoJie(Monster):
    def __init__(self, player_name, battle=True):
        super().__init__(12, player_name, battle)
        self.image = pg.image.load(GamePath.monster[12])
        self.image = pg.transform.scale(self.image,
                                        (MonsterSettings.monsterWidth, MonsterSettings.monsterHeight))
        self.HP = MonsterSettings.monsterHP[self.lvl]
        self.HP_text = pg.font.Font(GamePath.font, 18).render(f'BOSS血量：{self.HP:.1f}', True, (255, 255, 0, 120))
        self.attack = MonsterSettings.monsterAttack[self.lvl]
        self.defence = MonsterSettings.monsterDefence[self.lvl]
        self.bullet_list1 = None
        self.bullet_list2 = None
        self.knife_timer = 60
        self.shoot_timer1 = 90
        self.absorb_timer = 120
        self.absorb_times = 0
        self.maxHP = 0

    # 无大语言模型版
    def battle_update(self, player, battle=True):
        self.shoot_timer1 -= 1
        self.absorb_timer -= 1
        self.knife_timer -= 1
        if self.bullet_list1 is None and self.shoot_timer1 <= 0:
            self.shoot_timer1 = 180
            pg.mixer.Sound(GamePath.sound['boss_shoot2']).play()
            x = [randint(0, WindowSettings.width) for i in range(3)]
            y = [randint(0, WindowSettings.height) for i in range(3)]
            self.bullet_list1 = [Bullet(x[i], y[i], num=4,
                                        m_x=player.rect.center[0], m_y=player.rect.center[1],
                                        atk=self.attack // 2) for i in range(3)]
        if self.knife_timer <= 0:
            pg.mixer.Sound(GamePath.sound['boss_shoot1']).play()
            self.knife_timer = 150
            self.bullet_list2 = [Circle(self.rect.centerx, self.rect.centery, num=5, atk=self.attack // 4)]

        if self.absorb_timer <= 0:
            if self.absorb_times < 2:
                m_x = player.rect.center[0]
                m_y = player.rect.center[1]
                speed = self.speed
                x = self.rect.centerx
                y = self.rect.centery
                if m_x == x:
                    if m_y > y:
                        direction_x = 0
                        direction_y = speed
                    else:
                        direction_x = 0
                        direction_y = -speed
                else:
                    d = ((m_y - y) ** 2 + (m_x - x) ** 2) ** 0.5
                    direction_x = speed * ((m_x - x) / d)
                    direction_y = speed * ((m_y - y) / d)
                player.rect.x -= direction_x
                player.rect.y -= direction_y
                self.absorb_times += 1
            else:
                self.absorb_timer = 210
                self.absorb_times = 0
        return super().battle_update(player)

    # 大语言模型版
    def ai_update(self, player):
        global dec
        self.knife_timer -= 1
        if self.knife_timer == 20:
            # 多线程获取出招
            deci = DecThread((self.HP / self.maxHP * 100, player.HP / player.maxHP * 100,
                              player.rect.center, self.rect.center), q=dec_queue)
            deci.start()
        if self.knife_timer <= 0:
            dec = dec_queue.get()
            self.knife_timer = 60
            if self.bullet_list1 is None and dec == 1:
                pg.mixer.Sound(GamePath.sound['boss_shoot2']).play()
                x = [randint(0, WindowSettings.width) for i in range(5)]
                y = [randint(0, WindowSettings.height) for i in range(5)]
                self.bullet_list1 = [Bullet(x[i], y[i], num=4,
                                            m_x=player.rect.center[0], m_y=player.rect.center[1],
                                            atk=self.attack // 2) for i in range(5)]
            elif dec == 2:
                pg.mixer.Sound(GamePath.sound['boss_shoot1']).play()
                self.bullet_list2 = [Circle(self.rect.centerx, self.rect.centery, num=5, atk=self.attack // 4)]

            elif dec == 3:
                pg.mixer.Sound(GamePath.sound['boss_shoot1']).play()
                m_x = player.rect.center[0]
                m_y = player.rect.center[1]
                speed = self.speed * 2
                x = self.rect.centerx
                y = self.rect.centery
                if m_x == x:
                    if m_y > y:
                        direction_x = 0
                        direction_y = speed
                    else:
                        direction_x = 0
                        direction_y = -speed
                else:
                    d = ((m_y - y) ** 2 + (m_x - x) ** 2) ** 0.5
                    direction_x = speed * ((m_x - x) / d)
                    direction_y = speed * ((m_y - y) / d)
                player.rect.x -= direction_x
                player.rect.y -= direction_y
        return super().battle_update(player)
