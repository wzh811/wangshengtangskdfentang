from openai import OpenAI
import threading as th
from deep_translator import MyMemoryTranslator


translator = MyMemoryTranslator(source='en-GB', target='zh-CN')
de_translator = MyMemoryTranslator(source='zh-CN', target='en-GB')


class DecThread(th.Thread):
    def __init__(self, infor, q):
        th.Thread.__init__(self)
        self.infor = infor
        self.queue = q

    def run(self):
        decision1 = decision(self.infor[0], self.infor[1], self.infor[2], self.infor[3])
        self.queue.put(decision1)


client = OpenAI(
    base_url='http://10.15.88.73:5008/v1',
    api_key='ollama',  # required but ignored
)

o_message = [
    {
        'role': 'system',
        'content': f'你现在需要扮演游戏里面的Boss需要跟玩家进行对战，尽可能争取获胜。\
玩家当前位置：{0, 0}，你的位置：{1000, 800}(单位：像素，玩家及你的尺寸均为高150像素、宽100像素)。\
玩家当前生命值：100%，你的生命值：100%。玩家只有远程技能，让玩家靠近你对你有利。\
你拥有3个技能，请尽可能使用不同的技能：\
1. 在随机位置生成5枚弹射物射向玩家，每颗造成少量远程伤害，\
2. 生成一个回旋镖环绕自己，半径400像素，造成中等近战伤害，\
3.吸附玩家，使玩家靠近自己,同时对其造成大量近战伤害。\
请你输出你当前需要发动的技能。如果要发动1技能，请输出1,以此类推，\
只需要输出一个整数，1或2或3，不需要任何多余的信息。'
    },
    {
        'role': 'user',
        'content': "请发动技能。",
    }
]


def decision(monster_HP, player_HP, monster_pos, player_pos):
    global o_message
    o_message.extend([
        {
            'role': 'user',
            'content': f'玩家当前位置：{player_pos[0], player_pos[1]}，你的位置：{monster_pos[0], monster_pos[1]}。\
    玩家当前生命值：{player_HP}%，你的生命值：{monster_HP}%。只需要输出一个整数，1或2或3，不需要任何多余的信息。'
        }
    ])
    response = client.chat.completions.create(
        model="llama3.2",
        messages=o_message,  # a list of dictionary contains all chat dictionary
    )
    assistant_reply = response.choices[0].message.content
    print(f"Llama: {assistant_reply}")
    for i in assistant_reply:
        if i in ['1', '2', '3']:
            if len(o_message) < 20:
                o_message.append({'role': 'system', 'content': 'boss发动技能' + i})
            else:
                del o_message[4], o_message[3]
            return int(i)
        else:
            if len(o_message) < 20:
                o_message.append({'role': 'system', 'content': 'boss发动技能' + '1'})
            else:
                del o_message[4], o_message[3]
            return 1


history = [
    {
        'role': 'system',
        'content': "You play as a villain in a game, and you are the protagonist's toilet.\
You strongly dislike the protagonist sitting on you to use the toilet. \
Now you have become a beautiful girl and learned magic. \
You engage in a battle with the protagonist, and you need \
to think of some words to humiliate and anger him.\
(Please reply in simple English, no more than thirty words!)"
    }
]


def chat(message):
    global history
    message = de_translator.translate(message)
    if message.lower() in ["exit", "quit"]:
        print("chat ends.")
        return
    history.append({"role": "user", "content": message})
    response = client.chat.completions.create(
        model="llama3.2",
        messages=history,  # a list of dictionary contains all chat dictionary
    )
    assistant_reply = response.choices[0].message.content
    reply = translator.translate(assistant_reply)
    # print(f"Llama: {reply}")
    history.append({"role": "assistant", "content": assistant_reply})
    if len(history) > 20:
        del history[2], history[1]
    return reply


'''
# 尝试对话
chat('呃，你冷静一点。')
chat('你太过分了！')
print(history)
'''
