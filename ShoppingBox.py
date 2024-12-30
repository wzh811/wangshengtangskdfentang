# -*- coding:utf-8 -*-

from Enchantment import *
from Settings import *
import pygame as pg


class ShoppingBox:
    def __init__(self, window, npcPath, player, index, items,
                 fontSize: int = DialogSettings.fontSize,
                 fontColor=(255, 255, 255),
                 bgColor=(0, 0, 0, 100)):
        self.window = window
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pg.font.Font(GamePath.font, self.fontSize)

        self.bg = pg.Surface((ShopSettings.boxWidth, ShopSettings.boxHeight), pg.SRCALPHA)
        self.bg.fill(bgColor)

        self.npc = pg.image.load(npcPath)
        self.npc = pg.transform.scale(self.npc, (ShopSettings.npcWidth, ShopSettings.npcHeight))

        self.player = player
        self.id = index
        self.items = items
        self.sID = 0

    def buy(self):
        if self.id == 0:
            if self.sID == 0 and self.player.money >= 15 and self.player.gift_point > 0:
                self.player.attr_update(addCoins=-15, addAttack=1, addgift_point=-1)
            elif self.sID == 1 and self.player.money >= 15 and self.player.gift_point > 0:
                self.player.attr_update(addCoins=-15, addDefence=1, addgift_point=-1)
            elif self.sID == 2 and self.player.money >= 15 and self.player.gift_point > 0:
                self.player.attr_update(addCoins=-15, addSpeed=0.5, addgift_point=-1)
            elif self.sID == 3 and self.player.money >= 15 and self.player.gift_point > 0:
                self.player.attr_update(addCoins=-15, addmaxHP=2, addHP=2, addgift_point=-1)
        elif self.id == 1:
            if self.sID == 0 and self.player.money >= 10:
                self.player.attr_update(addCoins=-10)
                self.player.bag_update('力量药水', num=1)
            elif self.sID == 1 and self.player.money >= 10:
                self.player.attr_update(addCoins=-10)
                self.player.bag_update('生命恢复药水', num=1)
            elif self.sID == 2 and self.player.money >= 10:
                self.player.attr_update(addCoins=-10)
                self.player.bag_update('抗性提升药水', num=1)
            elif self.sID == 3 and self.player.money >= 10:
                self.player.attr_update(addCoins=-10)
                self.player.bag_update('速度药水', num=1)
        elif self.id == 2:
            if self.sID == 0 and self.player.money >= 350 and self.player.equipment['头盔'][0] == 0:
                self.player.attr_update(addCoins=-350, addDefence=7)
                self.player.bag_update('头盔', [1, 0, 0, 0, 0, 0, 0])
            elif self.sID == 1 and self.player.money >= 500 and self.player.equipment['胸甲'][0] == 0:
                self.player.attr_update(addCoins=-500, addDefence=10)
                self.player.bag_update('胸甲', [1, 0, 0, 0, 0, 0, 0])
            elif self.sID == 2 and self.player.money >= 400 and self.player.equipment['护腿'][0] == 0:
                self.player.attr_update(addCoins=-400, addDefence=8)
                self.player.bag_update('护腿', [1, 0, 0, 0, 0, 0, 0])
            elif self.sID == 3 and self.player.money >= 250 and self.player.equipment['靴子'][0] == 0:
                self.player.attr_update(addCoins=-250, addDefence=5)
                self.player.bag_update('靴子', [1, 0, 0, 0, 0, 0, 0])
        elif self.id == 3:
            if self.sID == 0 and self.player.money >= 200 and self.player.xp >= 20:
                self.player.xp -= 20
                self.player.attr_update(addCoins=-200)
                self.player.bag_update('头盔', enchant(self.player.equipment['头盔']))
            elif self.sID == 1 and self.player.money >= 200 and self.player.xp >= 20:
                self.player.xp -= 20
                self.player.attr_update(addCoins=-200)
                self.player.bag_update('胸甲', enchant(self.player.equipment['胸甲']))
            elif self.sID == 2 and self.player.money >= 200 and self.player.xp >= 20:
                self.player.xp -= 20
                self.player.attr_update(addCoins=-200)
                self.player.bag_update('护腿', enchant(self.player.equipment['护腿']))
            elif self.sID == 3 and self.player.money >= 200 and self.player.xp >= 20:
                self.player.xp -= 20
                self.player.attr_update(addCoins=-200)
                self.player.bag_update('靴子', enchant(self.player.equipment['靴子']))

    def render(self):
        self.window.blit(self.bg, (ShopSettings.boxStartX, ShopSettings.boxStartY))
        self.window.blit(self.npc, (DialogSettings.npcCoordX, DialogSettings.npcCoordY))
        offset = 0
        for index, item in enumerate(list(self.items.keys())):
            if index == self.sID:
                text = '-->' + item + ' ' + self.items[item]
            else:
                text = '      ' + item + ' ' + self.items[item]
            text = self.font.render(text, True, self.fontColor)
            self.window.blit(text, (ShopSettings.textStartX, ShopSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
        if self.id == 0:
            texts = ['资金:' + str(self.player.money),
                     '生命值:' + str(self.player.HP),
                     '攻击力:' + str(self.player.attack),
                     '防御力:' + str(self.player.defence),
                     '速度:' + str(self.player.speed),
                     '天赋点:' + str(self.player.gift_point),
                     '↑购买属性增益需要天赋点！',
                     '（w,s键切换商品，enter确认）']
        elif self.id == 1:
            texts = ['资金:' + str(self.player.money),
                     '力量药水:' + str(self.player.bag.get('力量药水')[0]),
                     '生命恢复药水:' + str(self.player.bag.get('生命恢复药水')[0]),
                     '抗性提升药水:' + str(self.player.bag.get('抗性提升药水')[0]),
                     '速度药水:' + str(self.player.bag.get('速度药水')[0])]
        elif self.id == 2:
            equipment_str = ''
            if self.player.equipment['头盔'][0] == 1:
                equipment_str = equipment_str + '头盔 '
            if self.player.equipment['胸甲'][0] == 1:
                equipment_str = equipment_str + '胸甲 '
            if self.player.equipment['护腿'][0] == 1:
                equipment_str = equipment_str + '护腿 '
            if self.player.equipment['靴子'][0] == 1:
                equipment_str = equipment_str + '靴子'

            texts = ['请选择要购买的装备。',
                     '在购买全套护甲后可以为装备附魔。',
                     '资金:' + str(self.player.money),
                     '当前拥有：',
                     equipment_str]
        elif self.id == 3:
            equipment_name = ''
            enchantment1 = ''
            enchantment2 = ''
            enchantment3 = ''
            if self.sID == 0:
                equipment_name = '头盔'
                enchantment1 = EnchantmentSort.name[self.player.equipment['头盔'][1]] + \
                               EnchantmentSort.lvl[self.player.equipment['头盔'][2]]
                enchantment2 = EnchantmentSort.name[self.player.equipment['头盔'][3]] + \
                               EnchantmentSort.lvl[self.player.equipment['头盔'][4]]
                enchantment3 = EnchantmentSort.name[self.player.equipment['头盔'][5]] + \
                               EnchantmentSort.lvl[self.player.equipment['头盔'][6]]
            elif self.sID == 1:
                equipment_name = '胸甲'
                enchantment1 = EnchantmentSort.name[self.player.equipment['胸甲'][1]] + \
                               EnchantmentSort.lvl[self.player.equipment['胸甲'][2]]
                enchantment2 = EnchantmentSort.name[self.player.equipment['胸甲'][3]] + \
                               EnchantmentSort.lvl[self.player.equipment['胸甲'][4]]
                enchantment3 = EnchantmentSort.name[self.player.equipment['胸甲'][5]] + \
                               EnchantmentSort.lvl[self.player.equipment['胸甲'][6]]
            elif self.sID == 2:
                equipment_name = '护腿'
                enchantment1 = EnchantmentSort.name[self.player.equipment['护腿'][1]] + \
                               EnchantmentSort.lvl[self.player.equipment['护腿'][2]]
                enchantment2 = EnchantmentSort.name[self.player.equipment['护腿'][3]] + \
                               EnchantmentSort.lvl[self.player.equipment['护腿'][4]]
                enchantment3 = EnchantmentSort.name[self.player.equipment['护腿'][5]] + \
                               EnchantmentSort.lvl[self.player.equipment['护腿'][6]]
            elif self.sID == 3:
                equipment_name = '靴子'
                enchantment1 = EnchantmentSort.name[self.player.equipment['靴子'][1]] + \
                               EnchantmentSort.lvl[self.player.equipment['靴子'][2]]
                enchantment2 = EnchantmentSort.name[self.player.equipment['靴子'][3]] + \
                               EnchantmentSort.lvl[self.player.equipment['靴子'][4]]
                enchantment3 = EnchantmentSort.name[self.player.equipment['靴子'][5]] + \
                               EnchantmentSort.lvl[self.player.equipment['靴子'][6]]

            texts = ['为道具附魔。附魔满三词条后,',
                     '再购买可以进行祛魔。',
                     '经验:' + str(self.player.xp) + ' 资金:' + str(self.player.money),
                     equipment_name,
                     enchantment1,
                     enchantment2,
                     enchantment3]
        else:
            texts = None

        offset = 0
        if texts:
            for text in texts:
                text = self.font.render(text, True, self.fontColor)
                self.window.blit(text, (
                    ShopSettings.textStartX + ShopSettings.boxWidth / 2, ShopSettings.textStartY + offset))
                offset += DialogSettings.textVerticalDist
