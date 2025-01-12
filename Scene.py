# -*- coding:utf-8 -*-

import Objects
import Map
from NPC import NPC
from Monster import Monster
from Objects import modify_city_map
from Portal import *
import os
from Settings import *


class Scene:
    def __init__(self, window, player):
        self.type = None
        self.player = player

        self.map = None
        self.chests = pg.sprite.Group()
        self.npcs = pg.sprite.Group()
        self.monsters = pg.sprite.Group()
        self.portals = pg.sprite.Group()
        self.obstacles = pg.sprite.Group()

        self.window = window
        self.width = WindowSettings.width
        self.height = WindowSettings.height
        self.cameraX = 0
        self.cameraY = 0

        self.ShoppingBox = None

    def update_camera(self, player):
        if player.rect.x > WindowSettings.width / 4 * 3:
            self.cameraX += player.speed
            if self.cameraX < self.get_width() - WindowSettings.width:
                player.fix_to_middle(player.speed, 0)
            else:
                self.cameraX = self.get_width() - WindowSettings.width
        elif player.rect.x < WindowSettings.width / 4:
            self.cameraX -= player.speed
            if self.cameraX > 0:
                player.fix_to_middle(-player.speed, 0)
            else:
                self.cameraX = 0

        if player.rect.y > WindowSettings.height / 4 * 3:
            self.cameraY += player.speed
            if self.cameraY < self.get_height() - WindowSettings.height:
                player.fix_to_middle(0, player.speed)
            else:
                self.cameraY = self.get_height() - WindowSettings.height
        elif player.rect.y < WindowSettings.height / 4:
            self.cameraY -= player.speed
            if self.cameraY > 0:
                player.fix_to_middle(0, -player.speed)
            else:
                self.cameraY = 0

    @staticmethod
    def get_width():
        return WindowSettings.width * WindowSettings.outdoorScale

    @staticmethod
    def get_height():
        return WindowSettings.height * WindowSettings.outdoorScale

    def render(self):
        for each in self.obstacles.sprites():
            each.update(self.cameraX, self.cameraY)
        for each in self.npcs.sprites():
            each.update(self.cameraX, self.cameraY)
        for each in self.chests.sprites():
            each.update(self.cameraX, self.cameraY)
        for each in self.monsters.sprites():
            each.update(self.cameraX, self.cameraY)
        for each in self.portals.sprites():
            each.update(self.cameraX, self.cameraY)
        if self.type == SceneType.WILD or self.type == SceneType.CITY:
            for i in range(SceneSettings.tileXnum):
                for j in range(SceneSettings.tileYnum):
                    self.window.blit(self.map[i][j],
                                     (SceneSettings.tileWidth * i - self.cameraX,
                                      SceneSettings.tileHeight * j - self.cameraY))
        elif self.type in [SceneType.BATTLE, SceneType.OVER, SceneType.WIN]:
            self.window.blit(self.map, (0, 0))

        self.chests.draw(self.window)
        self.npcs.draw(self.window)
        self.portals.draw(self.window)
        self.monsters.draw(self.window)
        self.obstacles.draw(self.window)


class CityScene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.type = SceneType.CITY
        if os.path.isfile(GamePath.saves + "\\" + player.name + "\\" + "city_map.txt"):
            self.map = Map.load_city_map(player.name)
        else:
            self.map = Map.gen_city_map(player)
        chests = Map.gen_chests(player.name)
        for i in chests:
            self.chests.add(i)
        self.map = Map.load_city_map(player.name)
        xiaotong = NPC(0, player.name)
        xiaojie = NPC(1, player.name)
        obstacles = [i for i in Map.gen_barrier()] + [i for i in Map.gen_city_obstacle(player_name=player.name)]
        for j in obstacles:
            self.obstacles.add(j)
        self.npcs.add(xiaotong)
        self.npcs.add(xiaojie)
        self.portals.add(Portal(self.width * 2 // 3, self.height * 2 // 3))


class WildScene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.type = SceneType.WILD
        if os.path.isfile(GamePath.saves + "\\" + player.name + "\\" + "wild_map.txt"):
            self.map = Map.load_wild_map(player.name)
        else:
            self.map = Map.gen_wild_map(player)
        self.portals.add(Portal(self.width * 2 // 3, self.height * 2 // 3))
        self.monsters = None
        self.monsters = pg.sprite.Group()
        if not os.path.isfile(GamePath.saves + "\\" + player.name + "\\" + "monsters.txt"):
            m = open(GamePath.saves + "\\" + player.name + "\\" + "monsters.txt", 'w')
            m.close()
        m = open(GamePath.saves + "\\" + player.name + "\\" + "monsters.txt")
        if m.readlines():
            monsters = Map.load_monsters(player_name=player.name)
            for i in monsters:
                self.monsters.add(i)
        else:
            for i in range(1, 11):
                monster = Monster(i, player.name)
                self.monsters.add(monster)
        m.close()
        self.map = Map.load_wild_map(player.name)
        obstacles = [i for i in Objects.gen_barrier()] + [i for i in Objects.gen_wild_obstacle(player_name=player.name)]
        for j in obstacles:
            self.obstacles.add(j)
        self.npcs.add(NPC(2, player.name))
        self.npcs.add(NPC(3, player.name))
        self.npcs.add(NPC(4, player.name))
        self.shoppingBox = None


class BattleScene(Scene):
    def __init__(self, window, player, monster):
        super().__init__(window, player)
        self.type = SceneType.BATTLE
        self.monsters.add(monster)
        image = pg.image.load(GamePath.battle)
        self.map = image


class OverScene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.type = SceneType.OVER
        image = pg.image.load(GamePath.over)
        image = pg.transform.scale(image, (WindowSettings.width, WindowSettings.height))
        self.map = image


class WinScene(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.type = SceneType.WIN
        image = pg.image.load(GamePath.win)
        image = pg.transform.scale(image, (WindowSettings.width, WindowSettings.height))
        self.map = image


class MainMenu(Scene):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.type = SceneType.MAIN_MENU
        self.bg = pg.image.load(GamePath.menu)
        self.bg = pg.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))

    def change_bg(self, index):
        if index == 1:
            self.bg = pg.image.load(GamePath.menu_start)
            self.bg = pg.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))
        elif index == 2:
            self.bg = pg.image.load(GamePath.menu_settings)
            self.bg = pg.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))
        else:
            self.bg = pg.image.load(GamePath.menu)
            self.bg = pg.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))

    def render(self):
        self.window.blit(self.bg, (0, 0))


class Button(pg.sprite.Sprite):
    def __init__(self, x, y, index):
        super().__init__()
        self.image = pg.image.load(GamePath.button)
        self.image = pg.transform.scale(self.image, (ButtonSettings.buttonWidth, ButtonSettings.buttonHeight))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.index = index
        self.choosed = False

    def draw(self, window):
        window.blit(self.image, self.rect)

    def move(self, x):
        if 493 < x < 920:
            self.rect.center = (x, self.rect.center[1])
        elif x <= 493:
            self.rect.center = (493, self.rect.center[1])
        elif x >= 920:
            self.rect.center = (920, self.rect.center[1])

    def get_choosed(self, m_x, m_y):
        if self.rect.collidepoint(m_x, m_y):
            self.choosed = True
            return True
        return False


class PauseScene(MainMenu):
    def __init__(self, window, player):
        super().__init__(window, player)
        self.type = SceneType.PAUSE
        self.bg = pg.image.load(GamePath.pause_menu)
        self.bg = pg.transform.scale(self.bg, (WindowSettings.width, WindowSettings.height))
        if os.path.isfile('settings.txt'):
            with open('settings.txt', 'r') as f2:
                volume = float(f2.read())
                pos1 = volume * 427 + 493
        else:
            pos1 = 706
        if os.path.isfile('dfc.txt'):
            with open('dfc.txt', 'r') as f3:
                dfc = float(f3.read())
                pos2 = (dfc - 1) * 427 + 493
        else:
            pos2 = 493
        button1 = Button(pos1, 244, 1)
        button2 = Button(pos2, 433, 2)
        self.buttons = pg.sprite.Group()
        self.buttons.add(button1)
        self.buttons.add(button2)

    def render(self):
        self.window.blit(self.bg, (0, 0))
