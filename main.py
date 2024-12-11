import sys
import pygame
import random
'''
from characters import *
from enemies import *
from objects import *
'''

if __name__ == '__main__':
    pygame.init()  # 初始化pygame 虽然在这个简单的开关空白窗体看不出作用 但是默认把他写上是必要的 防止报错

    screen = pygame.display.set_mode((800, 450))  # 设置一个400x400的空白窗体
    screen.fill((0, 255, 255))  # 这里我们给空白窗体添加一个背景颜色
    pygame.display.set_caption("转生到异世界之我的马桶和洗衣机想杀我")
    font = pygame.font.Font('STXINGKA.TTF', 36)

    def display_text(text,x=400,y=225,color=(0,0,100)):
        text_suf = font.render(text, True, color)
        text_rect = text_suf.get_rect()
        text_rect.center = (x, y)
        screen.blit(text_suf, text_rect)
        pygame.display.flip()


# 构造一个精灵父类
class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.image = pygame.image.load(name)  # 加载图片
        self.rect = self.image.get_rect()  # 获取rect的位置


# 构造一个背景精灵类 继承的精灵父类
class BgSprite(BaseSprite):
    # 初始化函数 加入参数name(需要加载的背景名) top_left（背景从哪里开始加载)
    def __init__(self, name, location):
        # 有精灵父类 必须调用
        super().__init__(name)
        self.rect.topleft = location  # 设置位置

    # 定义一个更新函数
    def update(self):
        self.rect.top += 10  # 每次向上移动10个像素
        if self.rect.top >= 600:
            self.rect.top = -600


# 构造一个背景精灵的管理类
class BgManage:
    # 定义初始化函数 传入Manage类的实例 方便把背景添加到screen上
    def __init__(self, mg):
        self.mg = mg
        self.bg_group = pygame.sprite.Group()  # 添加一个背景精灵组
        self.bg_sprite1 = BgSprite("img/begin2.png", (0, 0))  # 实例化两个背景精灵加入背景精灵组
        self.bg_sprite1.add(self.bg_group)
        self.bg_sprite2 = BgSprite("img/begin2.png", (0, -600))
        self.bg_sprite2.add(self.bg_group)

    def update(self):
        self.bg_group.update()
        self.bg_group.draw(self.mg.screen)


class PlayerSprite(BaseSprite):
    # 初始化函数 加入参数name(需要加载的图片) location（玩家从哪里开始加载)
    def __init__(self, name, location):
        # 有精灵父类 必须调用
        super().__init__(name)
        self.rect.topleft = location  # 设置位置

    def update(self):
        # 获取键盘事件 玩家移动
        key_pressed = pygame.key.get_pressed()
        # 按下键盘←键 向左移动
        if key_pressed[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.left -= 8
        # 按下键盘→键 向右移动
        elif key_pressed[pygame.K_RIGHT] and self.rect.right < 400:
            self.rect.left += 8
        # 按下键盘↑键 向上移动
        elif key_pressed[pygame.K_UP] and self.rect.top > 0:
            self.rect.top -= 8
        # 按下键盘↓键 向下移动
        elif key_pressed[pygame.K_DOWN] and self.rect.bottom < 600:
            self.rect.top += 8


class PlayerManage:  # 构造玩家管理类
    def __init__(self, mg):
        self.mg = mg
        # 添加玩家精灵组
        self.player_group = pygame.sprite.Group()
        # 实例玩家精灵并加入到玩家精灵组
        self.player_sprite = PlayerSprite("img2/me1.png", (150, 400))
        self.player_sprite.add(self.player_group)

    def update(self):
        self.player_group.update()
        self.player_group.draw(self.mg.screen)


# 构造道具精灵类
class PropSprite(BaseSprite):
    # 初始化函数 加入参数name(需要加载的道具图片) center（道具加载的位置)
    def __init__(self, name, center):
        super().__init__(name)
        self.rect.center = center

    def update(self):
        self.rect.top += 10
        if self.rect.top >= 600:
            self.kill()


class PropManage:
    def __init__(self, mg):
        self.mg = mg
        self.prop_group = pygame.sprite.Group()
        self.time_count = 3  # 计时器

    def update(self):
        # 每过一段时间就会产生道具
        self.time_count -= 0.1
        if self.time_count <= 0:
            self.time_count = 3
            self.prop_sprite = PropSprite("prop.png", (random.randint(0, 370), 0))
            self.prop_sprite.add(self.prop_group)
        self.prop_group.update()
        self.prop_group.draw(self.mg.screen)


# 构造管理类管理精灵管理类
class Manage:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("会动的背景")
        # 实例化背景精灵管理类
        self.bg_manage = BgManage(self)
        # 实例化玩家管理
        self.player_manage = PlayerManage(self)
        # 实例化道具管理
        self.prop_manage = PropManage(self)

    def run(self):
        while True:
            self.clock.tick(25)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # 更新背景管理类中的内容
            self.bg_manage.update()
            self.player_manage.update()
            self.prop_manage.update()
            # 组与组之间的碰撞检测
            result = pygame.sprite.groupcollide(self.player_manage.player_group, self.prop_manage.prop_group, False,
                                                True)
            if result:
                print("吃到了道具")

            pygame.display.flip()

class Util:
    """
    工具类： 提供静态方法
    """

    @staticmethod
    def check_click(sprite):
        # 如果是鼠标的左键
        """
        精灵的点击检测
        """
        if pygame.mouse.get_pressed()[0]:
            if sprite.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False


# 创建ui精灵类 继承pygame精灵
class UISprite(pygame.sprite.Sprite):
    def __init__(self, name, center):
        super().__init__()
        self.image = pygame.image.load(name)
        self.rect = self.image.get_rect()
        self.rect.center = center


# 构造Ui精灵管理类
class UIManage:
    def __init__(self, gm):
        self.gm = gm
        self.foot = pygame.font.Font("font/font.ttf", 30)

        # 创建一个游戏前的精灵组
        self.ready_group = pygame.sprite.Group()
        self.begin_btn = UISprite("img/begin_btn.png", (200, 300))
        self.begin_btn.add(self.ready_group)

        # 游戏结束
        self.end_group = pygame.sprite.Group()
        self.gm_over_btn = UISprite("img/begin_btn.png", (200, 300))
        self.gm_over_btn.add(self.end_group)

    def update(self):
        # 游戏前有一个开始按钮
        if self.gm.state == "ready":
            self.ready_group.draw(self.gm.screen)
            # 把开始精灵传入工具类
            if Util.check_click(self.begin_btn):
                # 状态切换到游戏中
                self.gm.state = "gaming"
        elif self.gm.state == "gaming":
            # 游戏中会显示一个游戏分数的字体
            self.gm.screen.blit(self.score_surface, (0, 0))
        elif self.gm.state == "end":
            # 游戏结束会出现重新开始按钮 点击重新开始会再次切换到游戏中
            self.end_group.draw(self.gm.screen)
            if Util.check_click(self.gm_over_btn):
                self.gm.state = "gaming"


class GameManage:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        self.state = "ready"
        # 实例化UI精灵管理类
        self.ui_manage = UIManage(self)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                # 测试一键自杀 游戏结束
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_SPACE:
                        self.state = "end"
            self.screen.fill((0, 255, 255))
            self.ui_manage.update()
            pygame.display.flip()


gm = Manage()
gm.run()
