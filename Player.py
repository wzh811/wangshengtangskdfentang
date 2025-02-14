# -*- coding:utf-8 -*-

import os
from Enchantment import *
from Settings import *
import pygame as pg
from random import randint
from itertools import cycle


class Player(pg.sprite.Sprite):
    def __init__(self, x, y, name):
        super().__init__()
        # 玩家名=用户名
        self.name = name
        # 用于行走动画
        self.indexes = None
        self.index = 1
        self.images = [pg.transform.scale(pg.image.load(img), (PlayerSettings.playerWidth, PlayerSettings.playerHeight))
                       for img in GamePath.player]
        self.image = self.images[self.index]
        self.walk_cd = 0
        self.direction = 2
        # 用于处理等级不足无法开箱子的消息显示
        self.information = None
        # 玩家位置
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # 用于处理玩家冲刺
        self.speed_up = False
        self.stamina = 100
        # 用于处理对话、购物
        self.talking = False
        # 开启玩家受伤
        self.damage = True
        # 用于处理玩家脚步声
        self.step = None
        # 用于处理战斗
        self.battle = False
        # 读取玩家信息，没有玩家信息则初始化
        if not os.path.isfile(GamePath.saves + "\\" + self.name + "\\" + "player.txt"):
            with open(GamePath.saves + "\\" + self.name + "\\" + "player.txt", 'w'):
                pass
        with open(GamePath.saves + "\\" + self.name + "\\" + "player.txt", 'r') as f:
            lines = f.readlines()
            if lines:
                self.lvl = int(lines[0][3:-1])
                self.speed = float(lines[1][3:-1])
                self.attack = int(lines[2][3:-1])
                self.defence = int(lines[3][3:-1])
                self.HP = float(lines[4][3:-1].split(' / ')[0])
                self.maxHP = int(lines[4][3:-1].split(' / ')[1])
                self.money = int(lines[5][3:-1])
                self.xp = int(lines[6][3:-1].split(' / ')[0])
                self.gift_point = int(lines[7][3:-1])
                self.talked = int(lines[8])
            else:
                self.lvl = 0
                self.speed = 5
                self.maxHP = PlayerSettings.playerHP[self.lvl]
                self.HP = self.maxHP
                self.attack = PlayerSettings.playerAttack[self.lvl]
                self.defence = PlayerSettings.playerDefence[self.lvl]
                self.money = 50
                self.xp = 0
                self.gift_point = 5
                self.talked = 0
        # 读取玩家背包内容（药水和护甲）
        if os.path.isfile(GamePath.saves + "\\" + self.name + "\\" + "bag.txt"):
            with open(GamePath.saves + "\\" + self.name + "\\" + "bag.txt", 'r') as f:
                lines = f.readlines()
                self.bag = eval(lines[0][:-1])
                self.equipment = eval(lines[1][:-1])
                self.enchantment = self.calc_enchantment()
                '''
                附魔属性：
                self.extra_damage = enchantment[0]
                self.resilience = enchantment[1]
                self.CRIT = enchantment[2]
                self.CHD = enchantment[3]
                self.HP_recover = enchantment[4]
                self.swiftness = enchantment[5]
                '''
        else:
            with open(GamePath.saves + "\\" + self.name + "\\" + "bag.txt", 'w') as f:
                self.bag = {'力量药水': [0, 0], '生命恢复药水': [0, 0], '速度药水': [0, 0], '抗性提升药水': [0, 0]}
                self.equipment = {'头盔': [0, 0, 0, 0, 0, 0, 0], '胸甲': [0, 0, 0, 0, 0, 0, 0],
                                  '护腿': [0, 0, 0, 0, 0, 0, 0], '靴子': [0, 0, 0, 0, 0, 0, 0]}
                f.write(str(self.bag) + "\n")
                f.write(str(self.equipment) + "\n")
                self.enchantment = (0, 0, 0, 0, 0, 0)

        text = [f'玩家名：{self.name}',
                f'等级：{self.lvl}',
                f'速度：{self.speed}',
                f'攻击力：{self.attack}',
                f'防御力：{self.defence}',
                f'生命值：{self.HP:.1f} / {self.maxHP}',
                f'资金：{self.money}',
                f'经验：{self.xp} / {PlayerSettings.playerXP[self.lvl + 1]}',
                f'天赋：{self.gift_point}',
                f'体力：{int(self.stamina)}%'
                ]
        self.text = [pg.font.Font(GamePath.font, 20).render(t, True,
                                                            (255, 255, 0, 120)) for t in text]
        self.bag_text = [pg.font.Font(GamePath.font, 25).render(f'{item}：{num}', True,
                                                                (255, 255, 0, 120)) for
                         item, num in self.bag.items()]

    # 整合装备提供的附魔属性，便于伤害计算
    def calc_enchantment(self):
        enchantment = [0, 0, 0, 0, 0, 0, 0]
        enchantment[self.equipment['头盔'][1]] += EnchantmentEffect.all[
            self.equipment['头盔'][1]][self.equipment['头盔'][2]]
        enchantment[self.equipment['头盔'][3]] += EnchantmentEffect.all[
            self.equipment['头盔'][3]][self.equipment['头盔'][4]]
        enchantment[self.equipment['头盔'][5]] += EnchantmentEffect.all[
            self.equipment['头盔'][5]][self.equipment['头盔'][6]]

        enchantment[self.equipment['胸甲'][1]] += EnchantmentEffect.all[
            self.equipment['胸甲'][1]][self.equipment['胸甲'][2]]
        enchantment[self.equipment['胸甲'][3]] += EnchantmentEffect.all[
            self.equipment['胸甲'][3]][self.equipment['胸甲'][4]]
        enchantment[self.equipment['胸甲'][5]] += EnchantmentEffect.all[
            self.equipment['胸甲'][5]][self.equipment['胸甲'][6]]

        enchantment[self.equipment['护腿'][1]] += EnchantmentEffect.all[
            self.equipment['护腿'][1]][self.equipment['护腿'][2]]
        enchantment[self.equipment['护腿'][3]] += EnchantmentEffect.all[
            self.equipment['护腿'][3]][self.equipment['护腿'][4]]
        enchantment[self.equipment['护腿'][5]] += EnchantmentEffect.all[
            self.equipment['护腿'][5]][self.equipment['护腿'][6]]

        enchantment[self.equipment['靴子'][1]] += EnchantmentEffect.all[
            self.equipment['靴子'][1]][self.equipment['靴子'][2]]
        enchantment[self.equipment['靴子'][3]] += EnchantmentEffect.all[
            self.equipment['靴子'][3]][self.equipment['靴子'][4]]
        enchantment[self.equipment['靴子'][5]] += EnchantmentEffect.all[
            self.equipment['靴子'][5]][self.equipment['靴子'][6]]
        return tuple(enchantment[1:])

    def bag_update(self, item, num):
        if item in self.bag:
            self.bag[item][0] += num
        else:
            self.equipment[item] = num
        # 更新背包并自动存档
        with open(GamePath.saves + "\\" + self.name + "\\" + "bag.txt", 'w') as p:
            p.write(str(self.bag) + "\n")
            p.write(str(self.equipment) + "\n")
            self.enchantment = self.calc_enchantment()

    def attr_update(self, addCoins=0, addHP=0, addmaxHP=0, addAttack=0, addDefence=0, addSpeed=0, addgift_point=0):
        if self.HP + addHP < 0:
            return
        self.money += addCoins
        # 购买音效
        if addCoins < 0:
            pg.mixer.Sound(GamePath.sound['purchase']).play()
        # 更新属性并自动保存
        self.HP += addHP
        self.attack += addAttack
        self.defence += addDefence
        self.speed += addSpeed
        self.maxHP += addmaxHP
        self.gift_point += addgift_point
        text = [f'玩家：{self.name}',
                f'等级：{self.lvl}',
                f'速度：{self.speed}',
                f'攻击：{self.attack}',
                f'防御：{self.defence}',
                f'生命：{self.HP:.1f} / {self.maxHP}',
                f'资金：{self.money}',
                f'经验：{self.xp} / {PlayerSettings.playerXP[self.lvl + 1]}',
                f'天赋：{self.gift_point}',
                f'体力：{int(self.stamina)}%']
        with open(GamePath.saves + "\\" + self.name + "\\" + "player.txt", 'w') as p:
            for i in range(1, len(text) - 1):
                if i == 2 and self.speed_up:
                    text[i] = text[i][0:3] + str(self.speed - 10)
                p.write(text[i] + "\n")
            p.write(str(self.talked))

    def update(self, keys, scene):
        # text为实时显示的玩家信息
        text = [f'玩家：{self.name}',
                f'等级：{self.lvl}',
                f'速度：{self.speed}',
                f'攻击：{self.attack}',
                f'防御：{self.defence}',
                f'生命：{self.HP:.1f} / {self.maxHP}',
                f'资金：{self.money}',
                f'经验：{self.xp} / {PlayerSettings.playerXP[self.lvl + 1]}',
                f'天赋：{self.gift_point}',
                f'体力：{int(self.stamina)}%']
        self.text = [pg.font.Font(GamePath.font, 18).render(t, True, (255, 255, 0, 120)) for t in text]
        # 战斗过程中不保存玩家属性变化，其他时候自动存档
        if not self.battle:
            self.bag_text = [pg.font.Font(GamePath.font, 18).render(f'{item}：{num[0]}', True, (255, 255, 0, 120)) for
                             item, num in self.bag.items()]
            with open(GamePath.saves + "\\" + self.name + "\\" + "player.txt", 'w') as p:
                for i in range(1, len(text) - 1):
                    if i == 2 and self.speed_up:
                        text[i] = text[i][0:3] + str(self.speed - 10)
                    p.write(text[i] + "\n")
                p.write(str(self.talked))
            # 加速状态消耗体力，不加速时以0.5倍速回复体力（敏捷附魔可以增加回复体力的速度，减缓消耗体力的速度）
            if self.speed_up:
                self.stamina -= 1 - self.enchantment[5] / 10
                if self.stamina <= 0:
                    self.speed_up = False
                    self.speed -= 10
            else:
                self.stamina += 0.5 * (1 + self.enchantment[5] / 10)
                if self.stamina > 100:
                    self.stamina = 100
        else:
            self.bag_text = [pg.font.Font(GamePath.font, 18).render(f'{item}：{num}', True,
                                                                    (255, 255, 0, 120)) for
                             item, num in self.bag.items()]
            if self.speed_up:
                self.stamina -= 1 - self.enchantment[5] / 10
                if self.stamina <= 0:
                    self.speed_up = False
                    self.speed -= 5 + self.enchantment[5]
            else:
                self.stamina += 0.5
                if self.stamina > 100:
                    self.stamina = 100
        if self.talking:
            self.index = 0
            self.image = self.images[self.index]
        else:
            # 控制玩家移动
            dx = 0
            dy = 0
            self.walk_cd -= 1
            if keys[pg.K_w] and self.rect.top > 0:
                dy -= self.speed
            if keys[pg.K_s] and self.rect.bottom < WindowSettings.height:
                dy += self.speed
            if keys[pg.K_a] and self.rect.left > 0:
                dx -= self.speed
            if keys[pg.K_d] and self.rect.right < WindowSettings.width:
                dx += self.speed

            # 碰撞检测，采用双方向分开检测，同时加入回弹防止卡住，比一般的取消移动更为流畅
            if dx != 0:
                self.rect = self.rect.move(dx, 0)
                if pg.sprite.spritecollide(self, scene.obstacles, False, pg.sprite.collide_mask):
                    ex_x = 1 if dx > 0 else -1
                    self.rect = self.rect.move(-dx - ex_x, 0)
                    dx = 0

            if dy != 0:
                self.rect = self.rect.move(0, dy)
                if pg.sprite.spritecollide(self, scene.obstacles, False, pg.sprite.collide_mask):
                    ex_y = 1 if dy > 0 else -1
                    self.rect = self.rect.move(0, -dy - ex_y)
                    dy = 0

            # 行走动画，变向检测采用循环迭代，斜向走时方向会来回切换
            if dx > 0:
                if self.direction != 1:
                    self.direction = 1
                    self.indexes = cycle([6, 7, 8])
            elif dx < 0:
                if self.direction != 2:
                    self.direction = 2
                    self.indexes = cycle([3, 4, 5])
            elif dy > 0:
                if self.direction != 3:
                    self.direction = 3
                    self.indexes = cycle([0, 1, 2])
            elif dy < 0:
                if self.direction != 4:
                    self.direction = 4
                    self.indexes = cycle([9, 10, 11])

            if dx == 0 and dy == 0:
                if self.direction == 1:
                    self.indexes = cycle([7])
                elif self.direction == 2:
                    self.indexes = cycle([4])
                elif self.direction == 3:
                    self.indexes = cycle([1])
                elif self.direction == 4:
                    self.indexes = cycle([10])
                self.direction = 0
                self.index = next(self.indexes)
                self.walk_cd = 0
                try:
                    self.step.stop()
                    self.step = None
                except:
                    pass
            elif self.step:
                if self.step.get_num_channels() == 0:
                    self.step.play()
                if self.walk_cd <= 0:
                    self.index = next(self.indexes)
                    self.walk_cd = 5/(self.speed//5)
            else:
                self.step = pg.mixer.Sound(GamePath.sound['step'])
                self.step.play()
                if self.walk_cd <= 0:
                    self.index = next(self.indexes)
                    self.walk_cd = 5/(self.speed//5)

            if scene.type == SceneType.CITY:
                # 开箱子
                for chest in scene.chests:
                    if pg.sprite.collide_rect(self, chest) and self.lvl >= chest.lvl:
                        pg.mixer.Sound(GamePath.sound['open_chest']).play()
                        self.rect = self.rect.move(-dx, -dy)
                        m = randint(10, 50) * chest.lvl
                        p = randint(5, 10) * chest.lvl
                        self.money += m
                        self.xp += p
                        self.information = [pg.font.Font(GamePath.font, 50).render(
                            f'经验增加{p}点！资金增加{m}！', True, (255, 0, 255)), 60]
                        # 删除开过的箱子
                        c = open(GamePath.saves + "\\" + self.name + "\\" + "chests.txt", 'r')
                        lines = c.readlines()
                        for line in lines:
                            if line[:-1].split(',')[2] == str(chest.index):
                                lines.remove(line)
                                break
                        c.close()
                        with open(GamePath.saves + "\\" + self.name + "\\" + "chests.txt", 'w') as c:
                            c.writelines(lines)
                        chest.kill()
                    elif pg.sprite.collide_rect(self, chest):
                        self.information = [pg.font.Font(GamePath.font, 50).render(
                            f'等级不足！需要{chest.lvl}级才能打开！', True, (255, 0, 255)), 60]

            # 传送门判定
            if pg.sprite.spritecollide(self, scene.portals, False, pg.sprite.collide_mask):
                for i in scene.portals:
                    if i.CD <= 0:
                        i.reset()
                        if self.step:
                            self.step.stop()
                            self.step = None
                        pg.event.post(pg.event.Event(GameEvent.EVENT_SWITCH))
                        self.rect.x, self.rect.y = WindowSettings.width // 2, WindowSettings.height // 2

            # 升级判定
            if self.lvl < 10:
                if self.xp >= PlayerSettings.playerXP[self.lvl + 1] and self.lvl < 10:
                    print("升级！")
                    pg.mixer.Sound(GamePath.sound['level_up']).play()
                    self.attack += PlayerSettings.playerAttack[self.lvl + 1] - PlayerSettings.playerAttack[self.lvl]
                    self.defence += PlayerSettings.playerDefence[self.lvl + 1] - PlayerSettings.playerDefence[self.lvl]
                    self.maxHP += PlayerSettings.playerHP[self.lvl + 1] - PlayerSettings.playerHP[self.lvl]
                    self.HP = self.maxHP
                    self.lvl += 1
                    self.xp = self.xp - PlayerSettings.playerXP[self.lvl]
                    self.gift_point += 3

            '''
            if any(keys):
                self.index = (self.index +1) % len(self.images)
                self.image = self.images[self.index]
            '''
        return self.step

    def draw(self, window):
        self.image = self.images[self.index]
        window.blit(self.image, self.rect)
        # 渲染玩家体力条
        stamina = pg.image.load(GamePath.stamina)
        size = (stamina.get_width() // 20, stamina.get_height() // 80)
        stamina_size = (int(stamina.get_width() * self.stamina / 100) // 20, stamina.get_height() // 80)
        if stamina_size[0] > 0:
            stamina = pg.transform.scale(stamina, stamina_size)
            window.blit(stamina, (self.rect.centerx - 40, self.rect.centery - 50))
        frame = pg.image.load(GamePath.frame)
        frame = pg.transform.scale(frame, (size[0] + 4, size[1] + 4))
        window.blit(frame, (self.rect.centerx - 42, self.rect.centery - 52))

    def fix_to_middle(self, dx, dy):
        self.rect.x -= dx
        self.rect.y -= dy
