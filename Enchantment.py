# -*- coding:utf-8 -*-

from Settings import *
import pygame as pg
import random as r
from enum import Enum

'''
随机从以下属性中选择：
穿刺1-5
（增伤15%/25%/35%/45%/55%）
坚韧1-3
（减伤10%/15%/20%）
会心1-5
（暴击率5%-25%）
狂暴1-5
（暴击伤害20%-100%）
生机1-3
（自动生命回复1/1.5/2点每秒）
敏捷1-3
（冲刺速度提升1.0/1.5/2.0，
体力消耗速度降低、回复速度提高10%/15%/20%）
'''


def enchant(enchant_object):
    if enchant_object[1] == 0:
        attr = r.randint(1, 6)
        if attr == 2 or attr == 5 or attr == 6:
            lvl = r.randint(1, 3)
        else:
            lvl = r.randint(1, 5)
        enchant_object[1] = attr
        enchant_object[2] = lvl
        return enchant_object
    elif enchant_object[3] == 0:
        attr = r.randint(1, 6)
        if attr == 2 or attr == 5 or attr == 6:
            lvl = r.randint(1, 3)
        else:
            lvl = r.randint(1, 5)
        enchant_object[3] = attr
        enchant_object[4] = lvl
        return enchant_object
    elif enchant_object[5] == 0:
        attr = r.randint(1, 6)
        if attr == 2 or attr == 5 or attr == 6:
            lvl = r.randint(1, 3)
        else:
            lvl = r.randint(1, 5)
        enchant_object[5] = attr
        enchant_object[6] = lvl
        return enchant_object
    else:
        return de_enchant(enchant_object)


def de_enchant(de_enchant_object):
    de_enchant_object = [1, 0, 0, 0, 0, 0, 0]
    return de_enchant_object


class EnchantmentSort:
    name = ('平凡', '穿刺', '坚韧', '会心', '狂暴', '生机', '敏捷')
    lvl = ('O', 'I', 'II', 'III', 'IV', 'V')


class EnchantmentEffect:
    pingfan = (0, 0, 0, 0, 0, 0, 0)
    chuanci = (0, 0.15, 0.25, 0.35, 0.45, 0.55)
    jianren = (0, 0.1, 0.15, 0.2)
    huixin = (0, 0.05, 0.1, 0.15, 0.2, 0.25)
    kuangbao = (0, 0.2, 0.4, 0.6, 0.8, 1.0)
    shengji = (0, 1.0, 1.5, 2.0)
    minjie = (0, 1.0, 1.5, 2.0)
    all = (pingfan, chuanci, jianren, huixin, kuangbao, shengji, minjie)
