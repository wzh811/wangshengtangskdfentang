# -*- coding:utf-8 -*-

import pygame as pg
from Settings import *
from Monster import *
from DialogBox import DialogBox
import Scene
import ShoppingBox
from Enchantment import *
import pyautogui as ui


class SceneManager:
    def __init__(self, window, player):
        self.scene = Scene.MainMenu(window, player)
        self.window = window
        self.state = GameState.MAIN_MENU
        self.clock = pg.time.Clock()
        self.player = player

    def check_event_shopping(self, player, keys):
        for npc in self.scene.npcs.sprites():
            if self.scene.shoppingBox:
                self.scene.shoppingBox.render()
            elif pg.sprite.collide_rect(npc, player) and npc.talked:
                npc.talked = False
                npc.talking = True
                player.talking = True
                # 小米，消耗天赋点和资金增加属性
                if npc.id == 2:
                    self.scene.shoppingBox = ShoppingBox.ShoppingBox(self.window, GamePath.NPC[2], player,
                                                                     items={"攻击力+1": "资金-15",
                                                                            "防御力+1": "资金-15",
                                                                            "速度+0.5": "资金-15",
                                                                            "最大生命值+2": "资金-15",
                                                                            "EXIT": ""}, index=0)
                # 小花，消耗资金购买药水
                elif npc.id == 3:
                    self.scene.shoppingBox = ShoppingBox.ShoppingBox(self.window, GamePath.NPC[3], player,
                                                                     items={"力量药水": "资金-10",
                                                                            "生命恢复药水": "资金-10",
                                                                            "抗性提升药水": "资金-10",
                                                                            "速度药水": "资金-10",
                                                                            "EXIT": ""}, index=1)
                # 小白，消耗资金和经验值为装备附魔（集齐全套护甲才可进行附魔）
                elif npc.id == 4:
                    if 0 in (player.equipment['头盔'][0], player.equipment['胸甲'][0],
                             player.equipment['护腿'][0], player.equipment['靴子'][0]):
                        self.scene.shoppingBox = ShoppingBox.ShoppingBox(self.window, GamePath.NPC[4], player,
                                                                         items={"头盔（防御+7）": "资金-350",
                                                                                "胸甲（防御+10）": "资金-500",
                                                                                "护腿（防御+8）": "资金-400",
                                                                                "靴子（防御+5）": "资金-250",
                                                                                "EXIT": ""}, index=2)
                    else:
                        self.scene.shoppingBox = ShoppingBox.ShoppingBox(self.window, GamePath.NPC[4], player,
                                                                         items={"头盔附魔(祛魔)": "经验-20，资金-200",
                                                                                "胸甲附魔(祛魔)": "经验-20，资金-200",
                                                                                "护腿附魔(祛魔)": "经验-20，资金-200",
                                                                                "靴子附魔(祛魔)": "经验-20，资金-200",
                                                                                "EXIT": ""}, index=3)
                self.scene.shoppingBox.render()

    def check_event_talking(self, player, keys):
        if_talked = []
        voice = None
        dialogBoxTemp = None
        for npc in self.scene.npcs.sprites():
            if self.state == GameState.GAME_PLAY_CITY:
                p = npc.talked
                if_talked.append(p)
            if pg.sprite.collide_rect(player, npc) and keys[pg.K_f]:
                dialogBoxTemp = None
                if npc.id == 0 and player.talked < 2:
                    player.talking = True
                    npc.talking = True
                    dialogBoxTemp = DialogBox(self.window, GamePath.NPC, 0,
                                              [['主人，我是小彤。是你的马桶变的！',
                                                '主人天天往我肚子里放脏东西，人家实在是受不了啊！'],
                                               ["所以，对不起了主人！我要杀了你！！！",
                                                "接招吧，旋风水龙卷！"]])
                    voice = pg.mixer.Sound(GamePath.voice[0])

                elif npc.id == 1 and player.talked < 2:
                    player.talking = True
                    npc.talking = True
                    dialogBoxTemp = DialogBox(self.window, GamePath.NPC, 1,
                                              [['主人，我是小洁。是你的洗衣机变的！',
                                                '主人天天往我肚子里放脏衣服，人家实在是受不了啊！'],
                                               ["所以，对不起了主人！我要杀了你！！！",
                                                "接招吧，轰隆隆冲击波！！"]])
                    voice = pg.mixer.Sound(GamePath.voice[1])
                elif npc.id == 2 and not npc.talked:
                    player.talking = True
                    npc.talking = True
                    dialogBoxTemp = DialogBox(self.window, GamePath.NPC, 2,
                                              [['主人，我是小米。是你的手机变的！',
                                                '主人对我很好，我也很喜欢主人'],
                                               ["所以，我会帮主人战胜小彤和小洁她们两个叛徒！",
                                                "我这里有一些东西，希望能帮到主人。。。"]])
                    voice = pg.mixer.Sound(GamePath.voice[2])

                elif npc.id == 3 and not npc.talked:
                    player.talking = True
                    npc.talking = True
                    dialogBoxTemp = DialogBox(self.window, GamePath.NPC, 3,
                                              [['主人，我是小花。是你的电脑变的！',
                                                '主人对我很好，我也很喜欢主人'],
                                               ["我会尽我所能帮助主人，",
                                                "主人可以在我这里购买一次性道具哦~"]])
                    voice = pg.mixer.Sound(GamePath.voice[3])
                elif npc.id == 4 and not npc.talked:
                    player.talking = True
                    npc.talking = True
                    dialogBoxTemp = DialogBox(self.window, GamePath.NPC, 4,
                                              [['主人，我是小白。是你的平板变的！',
                                                '主人对我很好，我也很喜欢主人'],
                                               ["主人如果想要变得更强的话，",
                                                "我可以给主人提供附魔装备！"]])
                    voice = pg.mixer.Sound(GamePath.voice[4])
                if voice:
                    voice.play()
                if dialogBoxTemp:
                    dialogBoxTemp.render()
                    npc.talked = True
                    print('渲染对话框')
                    return dialogBoxTemp, voice
        if if_talked:
            if not (False in if_talked) and player.talked < 2:
                player.talking = True
                player.talked = 2
                dialogBoxTemp = DialogBox(self.window, GamePath.NPC, -1,
                                          [['我靠，太可怕了！',
                                            '我还是快点跑路吧。。。'],
                                           ["没想到我的马桶和洗衣机居然想杀我，",
                                            "我得离她们远点。。。"],
                                           ["我也不知道该怎么办了，",
                                            "不如就往那个传送门里面跑吧！"]])
                dialogBoxTemp.render()
                return dialogBoxTemp, voice
        return dialogBoxTemp, voice

    def continue_talking(self, player, keys, dialogBox, text_count):
        if text_count > len(dialogBox.texts):
            return -1
        else:
            dialogBox.cur_txt = text_count
            dialogBox.render()
            return text_count

    def check_event_boss(self, player, keys):
        if player.talked >= 2:
            for npc in self.scene.npcs.sprites():
                if pg.sprite.collide_rect(player, npc):
                    # 大语言模型对话
                    if npc.id == 0 and keys[pg.K_e]:
                        message = ui.prompt(text='你果然还是来了!还有什么遗言吗？', title='小彤')
                        player.talking = True
                        npc.talking = True
                        while message:
                            reply = chat(message)
                            message = ui.prompt(text=reply, title='小彤')
                        player.talking = False
                        npc.talking = False
                        return None
                    # 进入boss战
                    elif npc.id == 0 and keys[pg.K_f]:
                        boss = XiaoTong(player.name)
                    elif npc.id == 1 and keys[pg.K_f]:
                        boss = XiaoJie(player.name)
                    else:
                        boss = None
                    return boss

    def flush_scene(self, state, monster=None):
        pg.mixer.music.stop()
        match state:
            case GameState.GAME_PLAY_WILD:
                self.scene = Scene.WildScene(self.window, self.player)
                pg.mixer.music.load(GamePath.bgm[4])
                pg.mixer.music.play(-1)
            case GameState.GAME_PLAY_CITY:
                self.scene = Scene.CityScene(self.window, self.player)
                if self.player.talked >= 2:
                    pg.mixer.music.load(GamePath.bgm[3])
                    pg.mixer.music.play(-1)
                else:
                    pg.mixer.music.load(GamePath.bgm[2])
                    pg.mixer.music.play(-1)
            case GameState.GAME_BATTLE:
                self.scene = Scene.BattleScene(self.window, self.player, monster=monster)
                if monster.lvl < 11:
                    pg.mixer.music.load(GamePath.bgm[1])
                    pg.mixer.music.play(-1)
                else:
                    pg.mixer.music.load(GamePath.bgm[7])
                    pg.mixer.music.play(-1)
            case GameState.GAME_OVER:
                self.scene = Scene.OverScene(self.window, self.player)
                pg.mixer.stop()
                pg.mixer.music.load(GamePath.bgm[6])
                pg.mixer.music.play(-1)
            case GameState.GAME_WIN:
                self.scene = Scene.WinScene(self.window, self.player)
                pg.mixer.stop()
                pg.mixer.music.load(GamePath.bgm[5])
                pg.mixer.music.play(1)
            case GameState.GAME_PAUSE:
                self.scene = Scene.PauseScene(self.window, self.player)
            case GameState.MAIN_MENU:
                self.scene = Scene.MainMenu(self.window, self.player)
                pg.mixer.music.load(GamePath.bgm[0])
                pg.mixer.music.play(-1)
            case _:
                pass
        self.state = state

    def tick(self, fps):
        self.clock.tick(fps)

    def check_event_battle(self, player, keys):
        for monster in self.scene.monsters:
            if pg.sprite.collide_rect(player, monster):
                print(monster)
                return monster
        else:
            return False

    def render(self):
        self.scene.render()
