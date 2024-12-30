# -*- coding:utf-8 -*-

from Monster import Monster, XiaoTong, XiaoJie
import sys
from Bullet import *
import time
from random import randint
from Settings import *
import pygame as pg


def battle(player, monster, window, scene_manager, fps, dfc=1.0):
    print('battle')
    level = monster.lvl
    # 用于处理玩家死亡后停止脚步声
    step_sound = None

    sprites = pg.sprite.Group()
    sprites.add(player)
    # 重新生成战斗状态的怪物
    monster.kill()
    if monster.lvl == 11:
        pg.mixer.Sound(GamePath.sound['boss_enter']).play()
        monster.rect.x = 1000
        monster.rect.y = 800
        monster = XiaoTong(player_name=player.name)
    elif monster.lvl == 12:
        pg.mixer.Sound(GamePath.sound['boss_enter']).play()
        monster.rect.x = 1000
        monster.rect.y = 800
        monster = XiaoJie(player_name=player.name)
    else:
        monster = Monster(lvl=level, player_name=player.name, battle=True)
    # 根据难度调整怪物属性
    monster.HP *= dfc * 3 - 1
    monster.attack *= dfc
    monster.defence *= dfc
    monster.speed *= 0.875 + dfc * 0.125
    if dfc > 1.8:
        monster.attack *= 1.2
        monster.speed *= 1.1

    # 生成怪物
    sprites.add(monster)
    # 设置玩家位置
    player.rect.x = 200
    player.rect.y = 200
    scene_manager.scene.cameraX = 0
    scene_manager.scene.cameraY = 0
    # 子弹管理
    bullets1 = []
    bullets2 = []
    bullets3 = []
    boss_bullets1 = []
    boss_bullets2 = []
    bomb_circles = []
    bomb_circle_count = 0
    kill_bomb_circle = 0
    cd = 5 if player.lvl < 4 else 4

    while True:
        scene_manager.tick(fps)
        scene_manager.render()
        keys = pg.key.get_pressed()
        m_x, m_y = pg.mouse.get_pos()
        # 重置瞬移CD
        try:
            start += 0
        except:
            start = 0
        # 玩家被击杀判定
        if player.HP <= 0:
            if step_sound:
                step_sound.stop()
            monster.kill()
            return 1
        # 击杀怪物判定
        if monster.HP <= 0:
            if step_sound:
                step_sound.stop()
            monster.kill()
            return 0
        # 怪物发射子弹
        bullet3 = monster.battle_update(player)
        if monster.lvl > 10:
            if monster.bullet_list1:
                for i in monster.bullet_list1:
                    boss_bullets1.append(i)
                    sprites.add(i)
                monster.bullet_list1 = None
            if monster.bullet_list2:
                for i in monster.bullet_list2:
                    boss_bullets2.append(i)
                    sprites.add(i)
                monster.bullet_list2 = None

        if bullet3 is not None:
            bullets3.append(bullet3)
            sprites.add(bullet3)
        # 更新怪物子弹
        for b in bullets3:
            b.update()
            if b.rect.x < 0 or b.rect.x > WindowSettings.width or b.rect.y < 0 or b.rect.y > WindowSettings.height:
                bullets3.remove(b)
                b.kill()
            elif pg.sprite.collide_rect(b, player):
                if player.damage:
                    # 考虑防御和坚韧附魔的效果
                    player.HP -= b.atk * 80 / (80 + player.defence) * (1 - player.enchantment[1])
                    pg.mixer.Sound(GamePath.sound['player_be_hit']).play()
                bullets3.remove(b)
                b.kill()
        # 更新boss子弹
        for b in boss_bullets1:
            b.update()
            if b.rect.x < 0 or b.rect.x > WindowSettings.width or b.rect.y < 0 or b.rect.y > WindowSettings.height:
                boss_bullets1.remove(b)
                b.kill()
            elif pg.sprite.collide_rect(b, player):
                if player.damage:
                    player.HP -= b.atk * 80 / (80 + player.defence) * (1 - player.enchantment[1])
                    pg.mixer.Sound(GamePath.sound['player_be_hit']).play()
                boss_bullets1.remove(b)
                b.kill()
        for b in boss_bullets2:
            # 小洁的回旋镖需要小洁的坐标来更新
            if monster.lvl == 12:
                b.update(monster.rect.centerx, monster.rect.centery)
                if pg.sprite.collide_rect(b, player):
                    if player.damage:
                        player.HP -= b.atk * 80 / (80 + player.defence) * (1 - player.enchantment[1])
                        pg.mixer.Sound(GamePath.sound['player_be_hit']).play()
            else:
                b.update()
                if b.rect.x < 0 or b.rect.x > WindowSettings.width or b.rect.y < 0 or b.rect.y > WindowSettings.height:
                    boss_bullets2.remove(b)
                    b.kill()
                if pg.sprite.collide_rect(b, player):
                    if player.damage:
                        player.HP -= b.atk * 80 / (80 + player.defence) * (1 - player.enchantment[1])
                        pg.mixer.Sound(GamePath.sound['player_be_hit']).play()
                    boss_bullets2.remove(b)
                    b.kill()

        # 显示玩家+怪物信息
        offset = 0
        for t in player.text:
            window.blit(t, (1075, 20 + offset))
            offset += 20
        # 怪物血条
        if monster.lvl < 11 and monster.HP > 0:
            monster_HP_image = pg.image.load(GamePath.HPline[2])
            monster_HP_image = pg.transform.scale(monster_HP_image, (500 * monster.HP /
                                                                     MonsterSettings.monsterHP[monster.lvl] /
                                                                     (dfc * 3 - 1), 20))
            window.blit(monster_HP_image, (400, 20))
        elif monster.HP > 0:
            monster_HP_image = pg.image.load(GamePath.HPline[3])
            monster_HP_image = pg.transform.scale(monster_HP_image, (500 * monster.HP /
                                                                     MonsterSettings.monsterHP[monster.lvl] /
                                                                     (dfc * 3 - 1), 20))
            window.blit(monster_HP_image, (400, 20))
        window.blit(monster.HP_text, (1075, 20 + offset))  # 以文本方式显示怪物血条

        # 玩家血条
        if player.HP / player.maxHP < 0.3 and player.HP > 0:
            player_HP_image = pg.image.load(GamePath.HPline[0])
            player_HP_image = pg.transform.scale(player_HP_image, (300 * player.HP / player.maxHP, 20))
            window.blit(player_HP_image, (500, 675))
        elif player.HP > 0:
            player_HP_image = pg.image.load(GamePath.HPline[1])
            player_HP_image = pg.transform.scale(player_HP_image, (300 * player.HP / player.maxHP, 20))
            window.blit(player_HP_image, (500, 675))
        # 显示玩家背包中的药水
        for t in player.bag_text:
            window.blit(t, (45 + offset, 700))
            offset += 200

        # 处理游戏事件
        for event in pg.event.get():
            # 退出游戏
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                # 左键发射子弹
                if event.button == 1:
                    bullet1 = Bullet(player.rect.centerx, player.rect.centery, 0, m_x, m_y,
                                     atk=player.attack // 2)
                    bullets1.append(bullet1)
                    sprites.add(bullet1)
                    # 7级后获得三发弹
                    if player.lvl >= 7:
                        bullet2 = Bullet(player.rect.midtop[0], player.rect.midtop[1],
                                         0, m_x, m_y, atk=player.attack // 4)
                        bullet2.direction_x = bullet1.direction_x
                        bullet2.direction_y = bullet1.direction_y
                        bullet3 = Bullet(player.rect.midbottom[0], player.rect.midbottom[1],
                                         0, m_x, m_y, atk=player.attack // 4)
                        bullet3.direction_x = bullet1.direction_x
                        bullet3.direction_y = bullet1.direction_y
                        bullets1.append(bullet2)
                        bullets1.append(bullet3)
                        sprites.add(bullet2)
                        sprites.add(bullet3)
                # 右键安放炸弹
                if event.button == 3:
                    bullet2 = Bomb(player.rect.x, player.rect.y, 1, m_x, m_y,
                                   atk=player.attack)
                    bullets2.append(bullet2)
                    sprites.add(bullet2)
            if event.type == pg.KEYDOWN:
                # 玩家无敌
                if event.key == pg.K_j:
                    player.damage = False
                # CTRL或SHIFT键加速(战斗中的加速效果比平时低，但所加的速度受到敏捷附魔的影响)
                if event.key == pg.K_LCTRL or event.key == pg.K_LSHIFT:
                    add_speed = 5 + player.enchantment[5]
                    if not player.speed_up and player.stamina > add_speed:
                        player.speed += add_speed
                        player.speed_up = True
                        print('加速')
                    elif player.speed_up:
                        player.speed -= add_speed
                        player.speed_up = False
                        print('减速')
                    else:
                        print('体力不足')
                # 空格键瞬移
                if event.key == pg.K_SPACE and time.time() - start > cd:
                    if WindowSettings.width / 16 < m_x < WindowSettings.width / 16 * 15:
                        m_x = m_x
                    elif m_x <= WindowSettings.width / 16:
                        m_x = WindowSettings.width / 16
                    else:
                        m_x = WindowSettings.width / 16 * 15
                    if WindowSettings.height / 16 < m_y < WindowSettings.height / 16 * 15:
                        m_y = m_y
                    elif m_y <= WindowSettings.height / 16:
                        m_y = WindowSettings.height / 16
                    else:
                        m_y = WindowSettings.height / 16 * 15
                    player.rect.center = (m_x, m_y)
                    start = time.time()

                # 喝药
                if event.key == pg.K_1 and player.bag["力量药水"][0] > 0 and player.bag["力量药水"][1] < 2:
                    player.attack += 5
                    if player.lvl == 10:
                        player.attack += 4
                    player.bag["力量药水"][1] += 1
                    player.bag_update("力量药水", -1)
                    if player.bag["力量药水"][1] == 1:
                        pg.time.set_timer(BattleEvent.Strength_time_over, 10000, loops=1)
                    else:
                        pg.time.set_timer(BattleEvent.Strength_time_over1, 10000, loops=1)
                if event.key == pg.K_2 and player.bag["生命恢复药水"][0] > 0 and player.bag["生命恢复药水"][1] < 11:
                    player.HP += 5
                    if player.lvl == 10:
                        player.HP += 4
                    if player.HP > player.maxHP:
                        player.HP = player.maxHP
                    player.bag["生命恢复药水"][1] += 10
                    player.bag_update("生命恢复药水", -1)
                    if player.bag["生命恢复药水"][1] == 10:
                        pg.time.set_timer(BattleEvent.Life_add, 500, loops=10)
                    else:
                        pg.time.set_timer(BattleEvent.Life_add1, 500, loops=10)
                if event.key == pg.K_3 and player.bag["速度药水"][0] > 0 and player.bag["速度药水"][1] < 2:
                    player.speed += 5
                    if player.lvl == 10:
                        player.speed += 3
                    player.bag["速度药水"][1] += 1
                    player.bag_update("速度药水", -1)
                    if player.bag["速度药水"][1] == 1:
                        pg.time.set_timer(BattleEvent.Speed_time_over, 7000, loops=1)
                    else:
                        pg.time.set_timer(BattleEvent.Speed_time_over1, 7000, loops=1)
                if event.key == pg.K_4 and player.bag["抗性提升药水"][0] > 0 and player.bag["抗性提升药水"][1] < 2:
                    player.defence += 7
                    if player.lvl == 10:
                        player.defence += 5
                    player.bag["抗性提升药水"][1] += 1
                    player.bag_update("抗性提升药水", -1)
                    if player.bag["抗性提升药水"][1] == 1:
                        pg.time.set_timer(BattleEvent.Defence_time_over, 10000, loops=1)
                    else:
                        pg.time.set_timer(BattleEvent.Defence_time_over1, 10000, loops=1)
            # 清除爆炸动画
            if 0 < event.type <= kill_bomb_circle:
                for i in bomb_circles:
                    print(i.index, kill_bomb_circle)
                    if i.index <= kill_bomb_circle:
                        bomb_circles.remove(i)
                        i.kill()
            # buff结束
            if event.type == BattleEvent.Strength_time_over:
                player.attack -= 5
                player.bag["力量药水"][1] -= 1
                player.bag_update('力量药水', 0)
                print('力量恢复')
            if event.type == BattleEvent.Strength_time_over1:
                player.attack -= 5
                player.bag["力量药水"][1] -= 1
                player.bag_update('力量药水', 0)
                print('力量恢复1')
            if event.type == BattleEvent.Life_add:
                player.HP += 1
                if player.lvl == 10:
                    player.HP += 0.5
                if player.HP > player.maxHP:
                    player.HP = player.maxHP
                player.bag["生命恢复药水"][1] -= 1
                player.bag_update('生命恢复药水', 0)
                print('生命恢复')
            if event.type == BattleEvent.Life_add1:
                player.HP += 1
                if player.HP > player.maxHP:
                    player.HP = player.maxHP
                player.bag["生命恢复药水"][1] -= 1
                player.bag_update('生命恢复药水', 0)
                print('生命恢复1')
            if event.type == BattleEvent.Defence_time_over:
                player.defence -= 7
                player.bag["抗性提升药水"][1] -= 1
                player.bag_update('抗性提升药水', 0)
                print('防御恢复')
            if event.type == BattleEvent.Defence_time_over1:
                player.defence -= 7
                player.bag["抗性提升药水"][1] -= 1
                player.bag_update('抗性提升药水', 0)
                print('防御恢复1')
            if event.type == BattleEvent.Speed_time_over:
                player.speed -= 5
                player.bag["速度药水"][1] -= 1
                player.bag_update('速度药水', 0)
                print('速度恢复')
            if event.type == BattleEvent.Speed_time_over1:
                player.speed -= 5
                player.bag["速度药水"][1] -= 1
                player.bag_update('速度药水', 0)
                print('速度恢复1')

        # 生机附魔的效果
        player.HP += player.enchantment[4] / fps
        if player.HP > player.maxHP:
            player.HP = player.maxHP
        # 更新玩家状态
        step = player.update(keys, scene_manager.scene)
        if step:
            step_sound = step
        # 更新玩家子弹
        if bullets1:
            for i in bullets1:
                i.update()
                if pg.sprite.collide_rect(i, monster):
                    i.delete = True
                    pg.mixer.Sound(GamePath.sound['monster_be_hit']).play()
                    # 暴击判定，同时考虑会心附魔提供的暴击率、狂暴附魔提供的爆伤和穿刺附魔提供的增伤(初始爆伤为50%，暴击率为5%)
                    critical_hit = randint(1, 100) <= 5 + 100 * player.enchantment[2]
                    if critical_hit:
                        monster.HP -= (i.atk * 80 / (80 + monster.defence)
                                       * (1 + player.enchantment[0]) * (1.5 + player.enchantment[3]))
                    else:
                        monster.HP -= i.atk * 80 / (80 + monster.defence) * (1 + player.enchantment[0])
                if i.delete:
                    bullets1.remove(i)
                    i.kill()
        # 更新玩家炸弹
        if bullets2:
            for i in bullets2:
                i.update()
                if i.delete:
                    bomb_circle_count += 1
                    bomb_circle = Bomb(i.rect.x, i.rect.y, 3, index=bomb_circle_count)
                    print(bomb_circle.index, 'bomb_circle_index')
                    sprites.add(bomb_circle)
                    bomb_circles.append(bomb_circle)
                    pg.time.set_timer(bomb_circle.index, 200, loops=1)
                    kill_bomb_circle = bomb_circle.index
                    if pg.sprite.collide_rect(bomb_circle, monster):
                        pg.mixer.Sound(GamePath.sound['monster_be_hit']).play()
                        # 暴击判定，同时考虑会心附魔提供的暴击率、狂暴附魔提供的爆伤和穿刺附魔提供的增伤(初始爆伤为50%，暴击率为5%)
                        critical_hit = randint(1, 100) <= 5 + 100 * player.enchantment[2]
                        if critical_hit:
                            monster.HP -= (i.atk * 80 / (80 + monster.defence)
                                           * (1 + player.enchantment[0]) * (1.5 + player.enchantment[3]))
                        else:
                            monster.HP -= i.atk * 80 / (80 + monster.defence) * (1 + player.enchantment[0])
                    i.kill()
                    bullets2.remove(i)

        sprites.draw(window)
        player.draw(window)
        pg.display.flip()
