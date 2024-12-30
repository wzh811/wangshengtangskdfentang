# -*- coding:utf-8 -*-

from Settings import *
import pygame as pg


class Portal(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pg.image.load(GamePath.portal)
        self.image = pg.transform.scale(self.image, (PortalSettings.portalWidth, PortalSettings.portalHeight))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.CD = 150

    def draw(self, window):
        window.blit(self.image, self.rect)

    def update(self, dx, dy):
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy
        if self.CD > 0:
            self.CD -= 1

    def reset(self):
        self.CD = 300
