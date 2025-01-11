# -*- coding:utf-8 -*-

from Settings import *
import sys


# 用于生成简单的动画
def fade_out(window, image, start_alpha, finish_alpha, interval):
    image = pg.transform.scale(image, (WindowSettings.width, WindowSettings.height))
    alpha = start_alpha
    while alpha > finish_alpha:
        window.fill((0, 0, 0))
        image.set_alpha(alpha)
        window.blit(image, (0, 0))
        alpha -= interval
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
    pg.time.wait(300)


def fade_in(window, image, start_alpha, finish_alpha, interval):
    image = pg.transform.scale(image, (WindowSettings.width, WindowSettings.height))
    alpha = start_alpha
    while alpha < finish_alpha:
        window.fill((0, 0, 0))
        image.set_alpha(alpha)
        window.blit(image, (0, 0))
        alpha += interval
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()
    pg.time.wait(300)


def fade_in_font(window, text, font, start_alpha, finish_alpha, interval):
    alpha = start_alpha
    t = font.render(text, True, (255, 255, 255))
    width, height = t.get_size()
    surface = pg.Surface((width, height), pg.SRCALPHA)
    while alpha < finish_alpha:
        window.fill((0, 0, 0))
        surface.set_alpha(alpha)
        surface.blit(t, (0, 0))
        window.blit(surface, ((WindowSettings.width - width) // 2, (WindowSettings.height - height) // 2))
        alpha += interval
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()


def fade_out_font(window, text, font, start_alpha, finish_alpha, interval):
    alpha = start_alpha
    t = font.render(text, True, (255, 255, 255))
    width, height = t.get_size()
    surface = pg.Surface((width, height), pg.SRCALPHA)
    while alpha > finish_alpha:
        window.fill((0, 0, 0))
        surface.set_alpha(alpha)
        surface.blit(t, (0, 0))
        window.blit(surface, ((WindowSettings.width - width) // 2, (WindowSettings.height - height) // 2))
        alpha -= interval
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
        pg.display.update()


def cutscene(window, player_name):
    window.fill((0, 0, 0))
    pg.display.update()
    texts = f'''
{player_name}感到眼前一黑，
一大段信息涌入脑海:
勇者，你是被神选中的人。
你肩负着击败两大魔王的使命。
魔王看守着价值连城的宝藏。
当你实力足够时，
可以去魔王的领地开启宝藏。
而现在，你将在这片土地上战斗。
你要变强，
直到你能轻易击败所有敌人。
那时，再次穿过传送门，
去直面魔王的恐怖吧。
'''
    font = pg.font.Font(GamePath.font, 60)
    for text in texts.split('\n'):
        fade_in_font(window, text, font, 0, 255, 1)
        pg.time.wait(1800)
        fade_out_font(window, text, font, 255, 0, 1)
        pg.time.wait(500)


def common_win(window, player_name):
    offset = 0
    texts = ['你成功战胜了你的马桶和洗衣机。',
             '虽然这看起来并不是什么值得骄傲的事。',
             f'但勇者{player_name},你赢了。',
             'END']
    for t in texts:
        t = pg.font.Font(GamePath.font, 50).render(t, True, (255, 0, 255))
        window.blit(t, (50, offset))
        offset += 100
    pg.display.flip()
    pg.time.wait(8000)
    bg_image = pg.image.load(GamePath.win).convert_alpha()
    fade_out(window, bg_image, 255, 0, 1)


def elite_win(window, player_name):
    texts = f'''
“嘻嘻，怎么样，{player_name}，
本堂主编的故事还不错吧？”
明媚的笑容浮现在眼前女孩的俏脸上.
你终于意识到，
自己被扔进了胡桃编的故事里当主角。
“很有趣。”你点头回应道。
“哼哼，下次也记得来捧场哦，
我还有好多故事等你来演呢！”
'''
    font = pg.font.Font(GamePath.font, 60)
    for text in texts.split('\n'):
        fade_in_font(window, text, font, 0, 255, 1)
        pg.time.wait(2400)
        fade_out_font(window, text, font, 255, 0, 1)
        pg.time.wait(500)
    hutao = pg.image.load(GamePath.hutao)
    fade_in(window, hutao, 0, 255, 1)
    pg.time.wait(2000)
    fade_out(window, hutao, 255, 0, 0.5)
