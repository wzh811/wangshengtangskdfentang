# -*- coding:utf-8 -*-

from Settings import *


class NPC(pg.sprite.Sprite):
    def __init__(self, num, player_name):
        super().__init__()
        # 固定位置生成NPC
        self.x = NPCSettings.NPCx[num]
        self.y = NPCSettings.NPCy[num]
        self.image = pg.image.load(GamePath.NPC[num])
        self.image = pg.transform.scale(self.image, (NPCSettings.NPCWidth, NPCSettings.NPCHeight))
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)

        self.talking = False
        self.id = num
        self.talk_CD = 0
        self.talked = False

        # 储存NPC信息（其实发现没用，用作胜利结算了，应该命名为boss.txt但懒得改了）
        n = open(GamePath.saves + "\\" + player_name + "\\" + "NPCs.txt", 'a+')
        talking = 1 if self.talking else 0
        talked = 1 if self.talking else 0
        n.seek(0)
        if n.readlines:
            for line in n.readlines():
                if line.split(',')[0] == str(self.id):
                    break
            else:
                n.write(f'{self.id},{self.talk_CD},{talking},{talked}\n')
        n.close()

    def update(self, dx, dy):
        self.rect.x = self.x - dx
        self.rect.y = self.y - dy
        self.talk_CD -= 1
        if self.talk_CD < 0:
            self.talk_CD = 0

    def can_talk(self):
        if self.talk_CD > 0:
            return False
        else:
            return not self.talking

    # 改为f键互动之后也没用了，但还是留在这里，万一要改回去
    def reset_talk_cd(self):
        self.talk_CD = 150
