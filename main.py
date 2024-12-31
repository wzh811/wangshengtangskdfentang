# -*- coding:utf-8 -*-

import os
from Run import run_game
import pygame as pg

# 读取游戏难度
if os.path.isfile('dfc.txt'):
    dfc = float(open('dfc.txt', 'r').read())
else:
    dfc = 1.0
with open('dfc.txt', 'w') as f:
    f.write(str(dfc))


if __name__ == "__main__":
    ori_dir = os.getcwd()
    fps = 30
    # 登录
    import Account
    player_name = Account.account_manager()
    if player_name:
        # 初始化游戏
        os.chdir(ori_dir)
        pg.init()
        # 初始化背景音乐
        pg.mixer.init()
        if os.path.isfile('settings.txt'):
            with open('settings.txt', 'r') as v:
                volume = float(v.read())
        else:
            volume = 0.5
        pg.mixer.music.set_volume(volume)
        # 游戏主进程
        run_game(player_name.strip(), fps=fps, dfc=dfc, direc=ori_dir)
