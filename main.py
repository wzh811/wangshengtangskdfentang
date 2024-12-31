# -*- coding:utf-8 -*-

from SceneManager import SceneManager
from Player import Player
from DialogBox import DialogBox
import os
from BattleBox import battle
from Animation import *

# 读取游戏难度
if os.path.isfile('dfc.txt'):
    dfc = float(open('dfc.txt', 'r').read())
else:
    dfc = 1.0
with open('dfc.txt', 'w') as f:
    f.write(str(dfc))


# 游戏主进程
def run_game(player_name_input):
    global fps, dfc
    pg.init()

    # 初始化背景音乐
    pg.mixer.init()
    if os.path.isfile('settings.txt'):
        with open('settings.txt', 'r') as v:
            volume = float(v.read())
    else:
        volume = 0.5
    pg.mixer.music.set_volume(volume)
    # 创建游戏窗口
    window = pg.display.set_mode((WindowSettings.width, WindowSettings.height))
    pg.display.set_caption(WindowSettings.name)
    # 更改游戏图标
    icon = pg.image.load(r'.\assets\icon\icon.png')
    pg.display.set_icon(icon)

    # 开场动画
    pg.mixer.Sound(GamePath.sound['game_enter']).play()
    window.fill((0, 0, 0))
    pg.time.wait(300)
    bg_image = pg.image.load(GamePath.game_enter).convert_alpha()
    fade_out(window, bg_image,255, 0, 0.5)

    # 创建玩家
    sprites = pg.sprite.Group()
    player = Player(WindowSettings.width // 2, WindowSettings.height // 2, name=player_name_input)
    sprites.add(player)

    # 清空buff槽
    player.bag["力量药水"][1] = 0
    player.bag["生命恢复药水"][1] = 0
    player.bag["速度药水"][1] = 0
    player.bag["抗性提升药水"][1] = 0
    player.bag_update('力量药水', 0)
    # 用于打开选项菜单及回到游戏
    paused = False
    # 用于中断配音
    voice = None
    # 用于渲染场景
    sceneManager = SceneManager(window, player)
    # 用于多段对话
    text_count = -2

    # 播放背景音乐
    pg.mixer.music.load(GamePath.bgm[0])
    pg.mixer.music.play(-1)

    # 游戏主循环
    while True:
        esc_sgn = False
        sceneManager.tick(fps)
        keys = pg.key.get_pressed()
        m_x, m_y = pg.mouse.get_pos()
        # 对话时停止刷新背景
        if not player.talking:
            sceneManager.render()
            # 退出对话时中断配音
            if voice:
                voice.stop()
                voice = None
        x = 0
        y = 0
        # 循环处理事件
        for event in pg.event.get():
            match event.type:
                # 退出游戏
                case pg.QUIT:
                    pg.quit()
                    pg.mixer.quit()
                    sys.exit()

                # 传送
                case GameEvent.EVENT_SWITCH:
                    pg.mixer.Sound(GamePath.sound['flush_scene']).play()
                    # 过场动画
                    if player.talked == 2:
                        cutscene(window, player.name)
                        player.talked = 3
                        player.update(sceneManager.scene, keys)

                    if sceneManager.state == GameState.GAME_PLAY_CITY:
                        sceneManager.flush_scene(GameState.GAME_PLAY_WILD)
                    else:
                        sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                    with open(GamePath.saves + "\\" + player.name + "\\" + "position.txt", 'w') as file:
                        file.write(str(sceneManager.state))

                case pg.MOUSEBUTTONDOWN:
                    # 测试用，打印鼠标坐标
                    if event.button == 1:
                        x, y = event.pos
                        print(x, y)
                case pg.KEYDOWN:
                    # 暂停游戏
                    if event.key == pg.K_ESCAPE and not player.talking:
                        esc_sgn = True
                    # 作弊键
                    if event.key == pg.K_m:
                        player.attr_update(addCoins=5000)
                    if event.key == pg.K_n:
                        player.xp += 500
                    # 更新对话
                    if event.key == pg.K_SPACE:
                        if sceneManager.state == GameState.GAME_PLAY_WILD:
                            if player.talking and sceneManager.scene.shoppingBox is None:
                                text_count += 1
                        elif player.talking:
                            text_count += 1
                        # print(text_count)
                    # 更新商店
                    if sceneManager.state == GameState.GAME_PLAY_WILD:
                        if sceneManager.scene.shoppingBox is not None:
                            for npc in sceneManager.scene.npcs.sprites():
                                if npc.talking:
                                    if event.key == pg.K_w:
                                        sceneManager.scene.shoppingBox.sID = max(0,
                                                                                 sceneManager.scene.shoppingBox.sID - 1)
                                    elif event.key == pg.K_s:
                                        sceneManager.scene.shoppingBox.sID = min(4,
                                                                                 sceneManager.scene.shoppingBox.sID + 1)
                                    elif event.key == pg.K_RETURN:
                                        if sceneManager.scene.shoppingBox.sID == 4:
                                            npc.talking = False
                                            npc.reset_talk_cd()
                                            player.talking = False
                                            sceneManager.scene.shoppingBox = None
                                        else:
                                            sceneManager.scene.shoppingBox.buy()
                    # CTRL或SHIFT键加速
                    if event.key == pg.K_LCTRL or event.key == pg.K_LSHIFT:
                        if not player.speed_up and player.stamina > 10:
                            player.speed += 10
                            player.speed_up = True
                            print('加速')
                        elif player.speed_up:
                            player.speed -= 10
                            player.speed_up = False
                            print('减速')
                        else:
                            print('体力不足')

        match sceneManager.state:
            # 大地图界面
            case GameState.GAME_PLAY_WILD | GameState.GAME_PLAY_CITY:
                # 显示玩家信息
                if not player.talking:
                    offset = 0
                    for t in player.text:
                        window.blit(t, (1075, 20 + offset))
                        offset += 20
                    offset = 0
                    for t in player.bag_text:
                        window.blit(t, (45 + offset, 700))
                        offset += 200
                if player.information:
                    window.blit(player.information[0], (0, 0))
                    player.information[1] -= 1
                    if player.information[1] <= 0:
                        player.information = []
                # 调整游戏选项（暂停游戏）
                if esc_sgn:
                    (c_x, c_y) = (sceneManager.scene.cameraX, sceneManager.scene.cameraY)
                    sceneManager.flush_scene(GameState.GAME_PAUSE)
                    sceneManager.render()
                    paused = True
                    esc_sgn = False
                # 城市场景
                if sceneManager.state == GameState.GAME_PLAY_CITY and not player.talking:
                    if text_count == -2 and player.talked == 0:
                        player.talking = True
                        text_count = 1
                        dialogBox = DialogBox(window, GamePath.NPC, -1,
                                              [[f'如你所见，我叫{player.name}，',
                                                '是一名普通的大学生。'],
                                               ["今天，当我从睡梦中醒来准备赶早八的时候，",
                                                "忽然发现自己转生到了异世界！(这小机器人是我吗？！)"],
                                               ['而且一看就是在二次元！',
                                                "（毕竟自己都已经变成纸片人了嘛）"],
                                               ['不远处好像有两个漂亮妹子，一看就很好说话（？）',
                                                '去找她们问问情况吧。']])
                        dialogBox.render()
                        player.talked = 1
                        player.update(keys, sceneManager.scene)
                        continue
                    player.update(keys, sceneManager.scene)
                    player.draw(window)
                    sceneManager.scene.update_camera(player)
                    # 进入boss战
                    boss = sceneManager.check_event_boss(player, keys)
                    if boss is not None:
                        sceneManager.flush_scene(GameState.GAME_BATTLE, boss)
                        player.battle = True
                        if player.speed_up:
                            player.speed -= 10
                            player.speed_up = False
                        b = battle(player, boss, window, sceneManager, fps, dfc)
                        if b == 1:
                            # 玩家被击败
                            player.kill()
                            sceneManager.flush_scene(GameState.GAME_OVER)
                            sceneManager.render()
                        else:
                            # 怪物被击败
                            # boss小彤
                            if boss.lvl == 11:
                                with open(GamePath.saves + "\\" + player_name + "\\" + "NPCs.txt", 'r+') as n:
                                    lines = n.readlines()
                                    n.seek(0)
                                    lines[0] = f'0,2\n'
                                    n.writelines(lines)
                                    n.truncate()
                                    if lines[1] == '1,2\n':
                                        # 游戏胜利
                                        if dfc < 1.5:
                                            sceneManager.flush_scene(GameState.GAME_WIN)
                                            sceneManager.render()
                                            common_win(window, player.name)
                                        else:
                                            sceneManager.flush_scene(GameState.GAME_WIN)
                                            sceneManager.render()
                                            elite_win(window, player.name)
                            # boss小洁
                            elif boss.lvl == 12:
                                with open(GamePath.saves + "\\" + player_name + "\\" + "NPCs.txt", 'r+') as n:
                                    lines = n.readlines()
                                    n.seek(0)
                                    lines[1] = f'1,2\n'
                                    n.writelines(lines)
                                    n.truncate()
                                    if lines[0] == '0,2\n':
                                        # 游戏胜利
                                        if dfc < 1.5:
                                            sceneManager.flush_scene(GameState.GAME_WIN)
                                            sceneManager.render()
                                            common_win(window, player.name)
                                        else:
                                            sceneManager.flush_scene(GameState.GAME_WIN)
                                            sceneManager.render()
                                            elite_win(window, player.name)
                            player.kill()
                            sprites.empty()
                            del sceneManager
                            # 重新创建玩家
                            player = Player(WindowSettings.width // 2, WindowSettings.height // 2,
                                            name=player_name_input)
                            sprites.add(player)
                            # 恢复玩家信息
                            with open(GamePath.saves + "\\" + player.name + "\\" + "player.txt", 'r') as p:
                                lines = p.readlines()
                                player.lvl = int(lines[0][3:-1])
                                player.speed = float(lines[1][3:-1])
                                player.attack = int(lines[2][3:-1])
                                player.defence = int(lines[3][3:-1])
                                player.HP = float(lines[4][3:-1].split(' / ')[0])
                                player.maxHP = int(lines[4][3:-1].split(' / ')[1])
                                player.money = int(lines[5][3:-1])
                                player.xp = int(lines[6][3:-1].split(' / ')[0])
                                player.gift_point = int(lines[7][3:-1])
                                player.talked = int(lines[8][:])
                            # 恢复玩家背包
                            with open(GamePath.saves + "\\" + player.name + "\\" + "bag.txt", 'r') as q:
                                lines = q.readlines()
                                player.bag = eval(lines[0][:-1])
                                player.equipment = eval(lines[1][:-1])
                            # 清空buff槽
                            player.bag["力量药水"][1] = 0
                            player.bag["生命恢复药水"][1] = 0
                            player.bag["速度药水"][1] = 0
                            player.bag["抗性提升药水"][1] = 0
                            player.bag_update('力量药水', 0)
                            # 获得战胜奖励
                            player.money += boss.lvl * 100
                            player.xp += boss.lvl * 20
                            # 重新设置游戏场景
                            sceneManager = SceneManager(window, player)
                            sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                            sceneManager.render()
                            player.update(keys, sceneManager.scene)
                            sprites.draw(window)
                            player.draw(window)
                    # 进入对话
                    dialogBox, voice1 = sceneManager.check_event_talking(player, keys)
                    if voice1:
                        voice = voice1
                    if dialogBox is not None:
                        text_count = 1

                # 继续对话
                elif sceneManager.state == GameState.GAME_PLAY_CITY and player.talking:
                    sceneManager.render()
                    cur_text = sceneManager.continue_talking(player, keys, dialogBox, text_count)
                    text_count = cur_text
                    # 结束对话
                    if text_count == -1:
                        for npc in sceneManager.scene.npcs.sprites():
                            if npc.talking:
                                npc.talking = False
                                player.talking = False
                                npc.reset_talk_cd()
                                print("退出对话")
                                dialogBox = None
                                text_count = 0
                                break
                        else:
                            player.talking = False
                            dialogBox = None
                            text_count = 0

                # 野外场景
                elif sceneManager.state == GameState.GAME_PLAY_WILD and not player.talking:
                    player.update(keys, sceneManager.scene)
                    player.draw(window)
                    sceneManager.scene.update_camera(player)
                    # 事件模块
                    sceneManager.check_event_shopping(player, keys)

                    # 战斗模块
                    m = sceneManager.check_event_battle(player, keys)
                    if m:
                        # 进入战斗
                        if player.speed_up:
                            player.speed -= 10
                            player.speed_up = False
                        sceneManager.flush_scene(GameState.GAME_BATTLE, m)
                        player.battle = True
                        b = battle(player, m, window, sceneManager, fps, dfc)
                        # 玩家被击败
                        if b == 1:
                            player.update(keys, sceneManager.scene)
                            player.kill()
                            sceneManager.flush_scene(GameState.GAME_OVER)
                            sceneManager.render()
                        else:
                            # 怪物被击败
                            player.kill()
                            sprites.empty()
                            del sceneManager
                            # 重新创建玩家
                            player = Player(WindowSettings.width // 2, WindowSettings.height // 2,
                                            name=player_name_input)
                            sprites.add(player)
                            # 恢复玩家信息
                            with open(GamePath.saves + "\\" + player.name + "\\" + "player.txt", 'r') as p:
                                lines = p.readlines()
                                player.lvl = int(lines[0][3:-1])
                                player.speed = float(lines[1][3:-1])
                                player.attack = int(lines[2][3:-1])
                                player.defence = int(lines[3][3:-1])
                                player.HP = float(lines[4][3:-1].split(' / ')[0])
                                player.maxHP = int(lines[4][3:-1].split(' / ')[1])
                                player.money = int(lines[5][3:-1])
                                player.xp = int(lines[6][3:-1].split(' / ')[0])
                                player.gift_point = int(lines[7][3:-1])
                                player.talked = int(lines[8][:])
                            # 恢复玩家背包
                            with open(GamePath.saves + "\\" + player.name + "\\" + "bag.txt", 'r') as q:
                                lines = q.readlines()
                                player.bag = eval(lines[0][:-1])
                                player.equipment = eval(lines[1][:-1])
                            # 清空buff槽
                            player.bag["力量药水"][1] = 0
                            player.bag["生命恢复药水"][1] = 0
                            player.bag["速度药水"][1] = 0
                            player.bag["抗性提升药水"][1] = 0
                            # 获得战胜奖励
                            player.money += m.lvl ** 2 * 5
                            player.xp += m.lvl * 10
                            # 重新设置游戏场景
                            sceneManager = SceneManager(window, player)
                            sceneManager.flush_scene(GameState.GAME_PLAY_WILD)
                            sceneManager.render()
                            player.update(keys, sceneManager.scene)
                            sprites.draw(window)
                            player.draw(window)
                    # 进入对话
                    dialogBox, voice1 = sceneManager.check_event_talking(player, keys)
                    if voice1:
                        voice = voice1
                    if dialogBox is not None:
                        text_count = 1

                # 继续对话/继续购物
                elif sceneManager.state == GameState.GAME_PLAY_WILD and player.talking:
                    sceneManager.render()
                    if sceneManager.scene.shoppingBox is not None:
                        sceneManager.check_event_shopping(player, keys)
                    if dialogBox is not None:
                        cur_text = sceneManager.continue_talking(player, keys, dialogBox, text_count)
                        text_count = cur_text
                        # 结束对话
                        if text_count == -1:
                            for npc in sceneManager.scene.npcs.sprites():
                                if npc.talking:
                                    npc.talking = False
                                    npc.talked = True
                                    player.talking = False
                                    if npc.id == 0 or npc.id == 1:
                                        npc.reset_talk_cd()
                                    print("退出对话")
                                    dialogBox = None
                                    text_count = 0
                                    break
                            else:
                                player.talking = False
                                dialogBox = None
                                text_count = 0
            # 主菜单
            case GameState.MAIN_MENU:
                if esc_sgn:
                    pg.quit()
                    sys.exit()
                # 选中按钮
                if 485 <= m_x <= 857 and 184 <= m_y <= 301:
                    sceneManager.scene.change_bg(1)
                elif 590 <= m_x <= 752 and 368 <= m_y <= 474:
                    sceneManager.scene.change_bg(2)
                else:
                    sceneManager.scene.change_bg(0)
                # 点击按钮
                if sceneManager.state == GameState.MAIN_MENU:
                    if 485 <= x <= 857 and 184 <= y <= 301:
                        if os.path.isfile(GamePath.saves + "\\" + player.name + "\\" + "position.txt"):
                            with open(GamePath.saves + "\\" + player.name + "\\" + "position.txt", 'r') as f0:
                                sceneManager.state = eval(f0.read())
                                if sceneManager.state == GameState.GAME_PLAY_WILD:
                                    sceneManager.flush_scene(GameState.GAME_PLAY_WILD)
                                elif sceneManager.state == GameState.GAME_PLAY_CITY:
                                    sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                        else:
                            sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                    elif 590 <= x <= 752 and 368 <= y <= 474:
                        sceneManager.flush_scene(GameState.GAME_PAUSE)
            # 选项菜单
            case GameState.GAME_PAUSE:
                sceneManager.scene.buttons.draw(window)
                # 拖动按钮
                if pg.mouse.get_pressed()[0] == 1:
                    for i in sceneManager.scene.buttons:
                        if i.choosed:
                            i.move(m_x)
                            if i.index == 1:
                                volume = round(((i.rect.center[0] - 493) / 427), 3)
                                pg.mixer.music.set_volume(volume)
                                with open("settings.txt", "w") as f1:
                                    f1.write(str(volume))
                            elif i.index == 2:
                                with open('dfc.txt', 'w') as f1:
                                    dfc_chr = round(((i.rect.center[0] - 493) / 427), 3) + 1
                                    f1.write(str(dfc_chr))
                                    dfc = dfc_chr
                                    print(dfc)
                            break
                        if i.get_choosed(x, y):
                            i.move(m_x)
                            if i.index == 1:
                                volume = round(((i.rect.center[0] - 493) / 427), 3)
                                pg.mixer.music.set_volume(volume)
                                with open("settings.txt", "w") as f1:
                                    f1.write(str(volume))
                            elif i.index == 2:
                                with open('dfc.txt', 'w') as f1:
                                    dfc_chr = round(((i.rect.center[0] - 493) / 427), 3) + 1
                                    f1.write(str(dfc_chr))
                                    dfc = dfc_chr
                                    print(dfc)
                            break

                else:
                    for i in sceneManager.scene.buttons:
                        i.choosed = False
                # 回到主菜单
                if esc_sgn and not paused:
                    sceneManager.flush_scene(GameState.MAIN_MENU)
                    esc_sgn = False
                # 取消暂停游戏
                elif esc_sgn and paused:
                    if os.path.isfile(GamePath.saves + "\\" + player.name + "\\" + "position.txt"):
                        with open(GamePath.saves + "\\" + player.name + "\\" + "position.txt", 'r') as f0:
                            sceneManager.state = eval(f0.read())
                            if sceneManager.state == GameState.GAME_PLAY_WILD:
                                sceneManager.flush_scene(GameState.GAME_PLAY_WILD)
                            elif sceneManager.state == GameState.GAME_PLAY_CITY:
                                sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                    else:
                        sceneManager.flush_scene(GameState.GAME_PLAY_CITY)
                    (sceneManager.scene.cameraX, sceneManager.scene.cameraY) = (c_x, c_y)
                    esc_sgn = False
                    paused = False

                pg.display.flip()
                continue
        # 更新屏幕
        pg.display.flip()


if __name__ == "__main__":
    ori_dir = os.getcwd()
    fps = 30
    # 登录
    import Account

    player_name = Account.account_manager()
    # player_name = 'player1'
    if player_name:
        # 开始游戏
        os.chdir(ori_dir)
        run_game(player_name)
