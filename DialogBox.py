# -*- coding:utf-8 -*-

from Settings import *
import pygame as pg


class DialogBox:
    def __init__(self, window, npcPath, npc_id, texts,
                 bgColor=(0, 0, 0, DialogSettings.boxAlpha),
                 fontSize=DialogSettings.fontSize,
                 fontColor=DialogSettings.fontColor,
                 w=DialogSettings.boxWidth,
                 h=DialogSettings.boxHeight):
        self.window = window
        self.texts = texts
        self.fontSize = fontSize
        self.fontColor = fontColor
        self.font = pg.font.Font(GamePath.font, self.fontSize)

        self.bg = pg.Surface((w, h), pg.SRCALPHA)
        self.bg.fill(bgColor)
        self.npc = pg.image.load(npcPath[npc_id])
        self.npc = pg.transform.scale(self.npc, (DialogSettings.npcWidth, DialogSettings.npcHeight))
        self.player = pg.image.load(GamePath.player[0])
        self.player = pg.transform.scale(self.player, (DialogSettings.npcWidth, DialogSettings.npcHeight))
        self.cur_txt = 1

    def render(self):
        self.window.blit(self.bg,
                         (DialogSettings.boxStartX, DialogSettings.boxStartY))
        self.window.blit(self.npc, (DialogSettings.npcCoordX, DialogSettings.npcCoordY))
        self.window.blit(self.player, (DialogSettings.playerCoordX, DialogSettings.playerCoordY))

        offset = 0
        for t in self.texts[self.cur_txt-1]:
            self.window.blit(self.font.render(t, True, self.fontColor),
                             (DialogSettings.textStartX, DialogSettings.textStartY + offset))
            offset += DialogSettings.textVerticalDist
