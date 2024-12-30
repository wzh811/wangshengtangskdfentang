from enum import Enum
import pygame as pg


class WindowSettings:
    name = "转生到异世界之我的马桶和洗衣机想杀我因为她们变成了美少女"
    width, height = 1280, 720
    outdoorScale = 3


class PlayerSettings:
    playerWidth = 50
    playerHeight = 80
    playerHP = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 32]
    playerAttack = [5, 7, 9, 11, 13, 15, 18, 21, 24, 27, 30]
    playerDefence = [2, 4, 6, 8, 9, 10, 11, 12, 13, 14, 15]
    playerXP = [10, 20, 35, 55, 80, 110, 145, 180, 220, 270, 330, 'max']


class SceneSettings:
    tileXnum = 96
    tileYnum = 54
    tileWidth, tileHeight = 40, 40


class GamePath:
    game_enter = r'.\assets\menu\start.png'

    player = [r'.\assets\player\player1.png']

    saves = r'.\saves'

    bgm = [r'.\assets\music\main_menu.mp3',
           r'.\assets\music\battle_scene.mp3',
           r'.\assets\music\city_scene.mp3',
           r'.\assets\music\city_scene2.mp3',
           r'.\assets\music\wild_scene.mp3']

    sound = {
        'bomb': r'.\assets\sound\bomb.mp3',
        'boss_enter': r'.\assets\sound\boss_enter.mp3',
        'boss_shoot1': r'.\assets\sound\boss_shoot1.mp3',
        'boss_shoot2': r'.\assets\sound\boss_shoot2.mp3',
        'flush_scene': r'.\assets\sound\flush_scene.mp3',
        'game_enter': r'.\assets\sound\game_enter.mp3',
        'level_up': r'.\assets\sound\level_up.mp3',
        'monster_be_hit': r'.\assets\sound\monster_be_hit.mp3',
        'open_chest': r'.\assets\sound\open_chest.mp3',
        'over': r'.\assets\sound\over.mp3',
        'player_be_hit': r'.\assets\sound\player_be_hit.mp3',
        'purchase': r'.\assets\sound\purchase.mp3',
        'step': r'.\assets\sound\step.mp3'
    }

    voice = [
        r'.\assets\voice\xiaotong.mp3',
        r'.\assets\voice\xiaojie.mp3',
        r'.\assets\voice\xiaomi.mp3',
        r'.\assets\voice\xiaohua.mp3',
        r'.\assets\voice\xiaobai.mp3',
        r'.\assets\voice\player.mp3'
    ]

    NPC = [r'.\assets\npc\xiaotong.png',
           r'.\assets\npc\xiaojie.png',
           r'.\assets\npc\xiaomi.png',
           r'.\assets\npc\xiaohua.png',
           r'.\assets\npc\xiaobai.png',
           r'.\assets\npc\player.png']

    bullet = [r'.\assets\bullet\bullet1.png',
              r'.\assets\bullet\bullet2.png',
              r'.\assets\bullet\bullet3.png',
              r'.\assets\bullet\bomb_circle.png',
              r'.\assets\bullet\boss_bullet.png',
              r'.\assets\bullet\knife.png']

    monster = [
        r'.\assets\monster\monster.png',
        r'.\assets\monster\monster1.png',
        r'.\assets\monster\monster2.png',
        r'.\assets\monster\monster3.png',
        r'.\assets\monster\monster4.png',
        r'.\assets\monster\monster5.png',
        r'.\assets\monster\monster6.png',
        r'.\assets\monster\monster7.png',
        r'.\assets\monster\monster8.png',
        r'.\assets\monster\monster9.png',
        r'.\assets\monster\monster10.png',
        r'.\assets\monster\xiaotong.png',
        r'.\assets\monster\xiaojie.png'
    ]

    groundTiles = [
        r'.\assets\tiles\ground1.png',
        r'.\assets\tiles\ground2.png',
        r'.\assets\tiles\ground3.png',
        r'.\assets\tiles\ground4.png',
        r'.\assets\tiles\ground5.png',
        r'.\assets\tiles\ground6.png'
    ]

    cityTiles = [
        r'.\assets\tiles\city1.png',
        r'.\assets\tiles\city2.png',
        r'.\assets\tiles\city3.png',
        r'.\assets\tiles\city4.png',
        r'.\assets\tiles\city5.png',
        r'.\assets\tiles\city6.png'
    ]

    battle = r'.\assets\tiles\battle.png'

    portal = r'.\assets\portals\portal.png'

    chest = r'.\assets\obstacles\chest.png'

    menu = r'.\assets\menu\menu.png'
    menu_start = r'.\assets\menu\menu1.png'
    menu_settings = r'.\assets\menu\menu2.png'

    pause_menu = r'.\assets\menu\pause.png'
    win = r'.\assets\menu\win.png'
    over = r'.\assets\menu\over.png'

    font = r'.\assets\fonts\STXINGKA.TTF'

    button = r'.\assets\buttons\button1.png'

    HPline = [r'.\assets\HP\HPline1.png',
              r'.\assets\HP\HPline2.png',
              r'.\assets\HP\HPline3.png',
              r'.\assets\HP\HPline4.png']


class GameState(Enum):
    MAIN_MENU = 1
    GAME_LOADING = 2
    GAME_BATTLE = 3
    GAME_OVER = 4
    GAME_WIN = 5
    GAME_PAUSE = 6
    GAME_PLAY_WILD = 7
    GAME_PLAY_CITY = 8


class NPCSettings:
    NPCWidth = 120
    NPCHeight = 150


class BulletSettings:
    bulletWidth = [21, 30, 20, 400, 10, 40]
    bulletHeight = [7, 30, 20, 400, 6, 40]
    bulletSpeed = [12, 0, 6, 0, 8, 0]
    bombTimer = 50
    circleTimer = 90


o_monsterHP = [10, 40, 70, 100, 130, 180, 230, 280, 340, 400, 500, 1800, 2000]
o_monsterDefence = [2, 4, 6, 8, 10, 12, 15, 18, 22, 26, 30, 35, 40]
o_monsterSpeed = [4, 4, 4.4, 4.8, 5.2, 5.6, 6, 6.4, 6.8, 7.2, 7.8, 7, 8]
o_monsterAttack = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 20, 16, 20]


class MonsterSettings:
    monsterWidth = 110
    monsterHeight = 120
    monsterHP = [o_monsterHP[i] * 2 for i in range(len(o_monsterHP))]
    monsterAttack = [o_monsterAttack[i] * 0.5 for i in range(len(o_monsterAttack))]
    monsterDefence = [o_monsterDefence[i] * 2 for i in range(len(o_monsterDefence))]
    monsterSpeed = [o_monsterSpeed[i] for i in range(len(o_monsterSpeed))]


class PortalSettings:
    portalWidth = 80
    portalHeight = 80


class DialogSettings:
    boxAlpha = 150
    fontSize = 27
    fontColor = (255, 255, 255)
    boxWidth = 1200
    boxHeight = 400
    npcWidth = 240
    npcHeight = 300
    textVerticalDist = 40
    boxStartX = 100
    boxStartY = 350
    textStartX = 170
    textStartY = 410
    npcCoordX = 20
    npcCoordY = 20
    playerCoordX = 700
    playerCoordY = 20


class ShopSettings:
    boxWidth = 1000
    boxHeight = 350
    npcWidth = 160
    npcHeight = 200
    boxStartX = 160
    boxStartY = 200
    textStartX = 170
    textStartY = 210


class SceneType:
    CITY = 0
    WILD = 1
    BATTLE = 2
    MAIN_MENU = 3
    OVER = 4
    WIN = 5
    PAUSE = 6


class GameEvent:
    EVENT_SWITCH = 1


class ButtonSettings:
    buttonWidth = 20
    buttonHeight = 50


class BattleEvent:
    Strength_time_over = pg.USEREVENT
    Life_add = pg.USEREVENT + 1
    Defence_time_over = pg.USEREVENT + 2
    Speed_time_over = pg.USEREVENT + 3
    Strength_time_over1 = pg.USEREVENT + 4
    Life_add1 = pg.USEREVENT + 5
    Defence_time_over1 = pg.USEREVENT + 6
    Speed_time_over1 = pg.USEREVENT + 7
