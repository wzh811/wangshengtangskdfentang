import pyautogui as ui
import os

ui.PAUSE = 0.5
ui.FAILSAFE = True
title = "转生到异世界之我的马桶和洗衣机想杀我因为她们变成了美少女"
if not os.path.isdir(os.getcwd() + "\\saves"):
    os.mkdir(os.getcwd() + "\\saves")
directory = os.getcwd() + "\\saves"
os.chdir(directory)
sgn_suc = False


def sgn_in():
    global sgn_suc
    unexist = True
    if not os.path.isfile('players.txt'):
        with open('players.txt','w'):
            pass
    if not os.path.isfile('passwords.txt'):
        with open('passwords.txt', 'w'):
            pass
    while not sgn_suc:
        sgnin = ui.prompt(text="输入您的用户名以登录：", title=title)
        if sgnin:
            with open('players.txt', 'r') as f:
                lines = f.readlines()
                for j, i in enumerate(lines):
                    if i[:-1] == sgnin:
                        psw = ui.password(text="请输入您的密码：", title=title)
                        if not psw:
                            break
                        with open('passwords.txt', 'r') as p:
                            psws = p.readlines()
                            line = psws[j]
                            z_psw = ''
                            for j in range(len(psw)):
                                if j // 2 == 0:
                                    z_psw = z_psw + psw[j]
                                else:
                                    z_psw = psw[j] + z_psw
                            if line[:-1] == sgnin[0] + z_psw + sgnin[1:]:
                                ui.alert(text="登录成功！", title=title)
                                sgn_suc = True
                                unexist = False
                                return sgnin
                            else:
                                ui.alert(text=" 登录\n密码不正确！请重新输入。", title=title)
                                unexist = False
                                break
                else:
                    if unexist:
                        ui.alert(text=" 登录\n用户不存在！请先注册。", title=title)
                    continue
        else:
            break


def account_manager():
    global sgn_suc
    while not sgn_suc:
        st = ui.confirm(text="请登录以开始游戏", title=title, buttons=["登录", "注册", "修改密码", "退出"])
        match st:
            case "登录":
                player_name = sgn_in()
                if player_name:
                    return player_name

            case "注册":
                rgt_suc = False
                while not rgt_suc:
                    rgt = ui.prompt(text="注册账号\n请输入您的用户名：", title=title, default='player')
                    if rgt:
                        if os.path.isfile('players.txt'):
                            pass
                        else:
                            p = open('players.txt','w')
                            p.close()
                        with open('players.txt', 'r+') as f:
                            lines = f.readlines()
                            for i in lines:
                                if i[:-1] == rgt:
                                    ui.alert(text=" 注册账号\n用户已存在！请换一个用户名。", title=title)
                                    break
                            else:
                                f.write(rgt + "\n")
                                psw = ui.prompt(text="注册账号\n请设置您的密码：", title=title)
                                if os.path.isfile('passwords.txt'):
                                    pass
                                else:
                                    p = open('passwords.txt', 'w')
                                    p.close()
                                with open('passwords.txt', 'a+') as p:
                                    zip_psw = ''
                                    for i in range(len(psw)):
                                        if i // 2 == 0:
                                            zip_psw = zip_psw + psw[i]
                                        else:
                                            zip_psw = psw[i] + zip_psw
                                    zip_psw = rgt[0] + zip_psw + rgt[1:]
                                    p.write(zip_psw + "\n")
                                    rgt_suc = rgt
                    else:
                        break
                if rgt_suc:
                    ui.alert(text="注册成功！", title=title, button='OK')
                    os.mkdir(os.getcwd() + "\\" + rgt_suc)
                    m = open(os.getcwd() + "\\" + rgt_suc + "\\" + "NPCs.txt", 'w')
                    m.close()
                    n = open(os.getcwd() + "\\" + rgt_suc + "\\" + "monsters.txt", 'w')
                    n.close()
                    p = open(os.getcwd() + "\\" + rgt_suc + "\\" + "player.txt", 'w')
                    p.close()
                    continue
            case "修改密码":
                player_name = sgn_in()
                if player_name:
                    with open('players.txt', 'r') as f:
                        lines = f.readlines()
                        for j, i in enumerate(lines):
                            if i[:-1] == player_name:
                                p = open("passwords.txt", 'r+')
                                psws = p.readlines()
                                n_psw = ui.prompt(text="欢迎" + player_name + "!\n请输入您的新密码：", title=title,
                                                  default=psws[j][-1])
                                if n_psw:
                                    zip_psw = ''
                                    for i in range(len(n_psw)):
                                        if i // 2 == 0:
                                            zip_psw = zip_psw + n_psw[i]
                                        else:
                                            zip_psw = n_psw[i] + zip_psw
                                    zip_psw = player_name[0] + zip_psw + player_name[1:]
                                    psws[j] = zip_psw + '\n'
                                    p.seek(0)
                                    p.writelines(psws)
                                    p.truncate()
                                    ui.alert(text="修改成功！", title=title)
                                p.close()
            case "退出":
                break
