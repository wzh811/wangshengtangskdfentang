队名：往生堂上科大分堂

队员：王梓衡2024533079

**[项目主页](https://github.com/wzh811/wangshengtangskdfentang/)**

**[exe版本](https://github.com/wzh811/wangshengtangskdfentang/releases)**

**Requirements(第三方库):openai(相信助教一定装好了),pyautogui,deep_translator**

**项目主页的根目录下有个requirements.bat，如果不介意自己电脑的python环境里多两个库就直接运行好了**

# 一个借鉴了元气骑士和MC和原神的小游戏，剧情非常简单

***重点在于打怪升级然后打boss...***

*关于分工：由于我们组就我一个人，所以所有的功劳都是我的啦，哈哈哈！！！*

关于操作：

空格键继续对话，f键交互，w、s键切换商品，enter购买，按住e键显示具体信息，对boss小彤按e键进行大语言模型对话，左ctrl或左shift疾跑，esc打开选项菜单

关于作弊（快速通关）：

在大地图场景中按下m键可获得5000资金，按下n键可获得500经验

在战斗场景中按下j键可以进入无敌状态，再次按下退出无敌状态

# 一些有意思的系统：

### 经验系统：打怪或者开宝箱获得经验来升级：

*除了一些基础属性的提升，还有：*

*升到3级时瞬移CD减少1秒；*

*升到7级时子弹变为三发弹（边上的子弹伤害为中间子弹的一半）；*

*升到10级时药水效果增强*

### 天赋点系统：初始拥有5天赋点，之后每升一级获得3天赋点，可以在NPC小米处进行天赋升级

*（建议优先升级速度，因为升级不加速度）*

### 药水商店：NPC小花售卖的便宜的药水能帮你获得短暂（其实不短了）的buff，最多叠加2层：

*前期比较有用，中期可以当糖豆吃，10级后又很有用*

### 装备与附魔系统：可以在NPC小白处购买护甲四件套，集齐四件后可以对它们进行附魔，

*附魔属性从中随机选取：穿刺（增伤），坚韧（减伤），会心（暴击率），狂暴（暴击伤害），生机（自动生命回复），敏捷（增强战斗中的冲刺速度，减少体力消耗，增加体力恢复速度），*

*穿刺，会心和狂暴的等级为1-5（I,II,III,IV,V），其余为1-3，*

*每件装备最多附魔三个词条，继续附魔可以去除所有词条重新附魔（这何尝不是一种刷圣遗物(其实更像是崩三的圣痕)），*

*但是前期还是别想着刷词条了，会消耗经验导致升级很慢*

## 战斗系统：

**有商店的地图上随机生成10只怪物，位置从左到右依次为lvl 1-10**

**小怪（头上顶着lvl 1-10的）拥有近战和远程两种攻击方式，近战伤害较高，千万记得不要离怪太近，如果难度较高容易被秒**

**Boss小彤有2个额外技能：1.从屏幕边缘向玩家发射一圈子弹；2.以自身为中心向边缘发射一圈子弹**

**Boss小洁有3个额外技能：1.生成一把快速环绕自己旋转的回旋镖；2.吸附玩家，使玩家靠近自己;3.在随机位置生成三枚子弹射向玩家**

**玩家初始有5%暴击率和50%暴击伤害**

**玩家的技能：**

*按左键朝鼠标方向发射子弹；*

*按右键在原地放置炸弹（范围较大，伤害较高）；*

*按空格瞬移到鼠标位置（有5秒CD）；*

*体力大于10%时，按左ctrl或左shift切换到冲刺模式，再按一下可以切换回普通移动，*

*冲刺时消耗体力，体力用完自动退出冲刺；*

*按1，2，3，4（不是小键盘上的）使用药水，获得攻击力/防御力/速度提升，或生命恢复效果*

# 其他特色功能：

**在boss所在地图中有20个宝箱，玩家每升一级可以开两个（与怪物生成方式类似），获得资金和少量经验值**

**难度和音量实时调节：**

*在主菜单点击选项按钮，或在大地图按esc打开选项界面，*

*拖动滑块调整音量和难度，其中，难度将很大程度影响游戏体验，*

*不建议尝试地狱难度，但如果非要尝试也未尝不可*

**玩家属性实时显示：**

**战斗属性实时显示：**

***玩家的药水数量和对应的buff层数显示在屏幕底部，***

***上面一丢丢显示的是玩家血条，血量过低时会变红，***

***怪物血条显示在屏幕顶部，boss血条颜色不一样，***

**账号管理：登录后才可进行游戏，每个玩家独立存档，保存玩家属性，背包，怪物位置，地图外观，宝箱开启情况**

**自动存档：玩家信息实时保存，但战斗中途退出游戏不会保存战斗进度（原神不就这样么）**

--

以下为更新日志，可以略过不看

--

v1.0-v1.0.1 更新内容:

*修复了中断对话后配音不停止的问题

*修复了玩家死亡后仍有脚步声的问题

*修复了可以重复购买护甲来提高防御力的问题

*修复了部分场景bgm异常中断的问题

*新增玩家升级额外增益（3、7、10级的额外强化）

*新增自动登录系统，支持多账号自动登录

*优化了账号管理系统的UI，增加注销账号功能

*修改了boss小洁回旋镖的伤害

*新增并修改了游戏图标

*新增游戏胜利界面

*优化了怪物生成位置

*修复了部分NPC图片两边有白边的问题

--

v1.0.2 更新内容：

*新增两种不同的胜利动画

*新增剧情过场动画

*新增胡桃图片

*修复了剧情对话时玩家脚步声未停止的问题

*修复了被小怪击败时站在传送门位置有概率被传入boss所在场景的问题

*修复了自动登录切换账号时用户名末尾\n未去除的问题

--

v1.1更新内容：

*全面优化信息显示的UI

*全面优化玩家行走动画

*全面优化地图路径和美观性

*重写怪物和宝箱的生成位置

*全面调整了游戏BGM和音效

*全面调整了npc和boss的贴图

*重写了障碍物的生成和碰撞判定

*重写了玩家信息显示方式

*修复了过场动画中仍有玩家脚步声的问题

*修复了在10级后药水buff未能正确消失的问题

*修复了玩家靠近边界时子弹发射失败的问题

*更改了玩家与NPC的交互方式，改为按f键

*新增了与boss小彤的大语言模型聊天功能

*boss小洁改为使用大语言模型出招

*修复了怪物等级信息会被障碍物遮挡的问题
