import pyautogui as ui
import os
from shutil import rmtree


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
        with open('players.txt', 'w'):
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
                            for z in range(len(psw)):
                                if z // 2 == 0:
                                    z_psw = z_psw + psw[z]
                                else:
                                    z_psw = psw[z] + z_psw
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
    if os.path.isfile('auto_sgn.txt'):
        while not sgn_suc:
            with open('auto_sgn.txt', 'r+') as a:
                players = a.readlines()
                if not players:
                    break
                print(players)
                auto_sgn = players[-1][:-1]
                st = ui.confirm(text="欢迎"+auto_sgn+'！', title=title,
                                buttons=['启动游戏', '切换账号', '修改密码', '注销', '取消自动登录'])
                match st:
                    case '启动游戏':
                        sgn_suc = auto_sgn
                        return auto_sgn
                    case '切换账号':
                        print(players[:][:-1])
                        auto_sgns = ui.confirm(text='请选择您要登录的账号：', title=title,
                                               buttons=players[:][:-1]+['我要\n登录其他账号'])
                        if auto_sgns == '我要\n登录其他账号':
                            break
                        elif auto_sgns:
                            sgn_suc = auto_sgns
                            return auto_sgns
                    case '修改密码':
                        sgnin = auto_sgn
                        with open('players.txt', 'r') as f:
                            lines = f.readlines()
                            for j, i in enumerate(lines):
                                if i[:-1] == sgnin:
                                    psw = ui.password(text="请输入您的密码以验证身份：", title=title)
                                    if not psw:
                                        break
                                    with open('passwords.txt', 'r') as p:
                                        psws = p.readlines()
                                        line = psws[j]
                                        z_psw = ''
                                        for z in range(len(psw)):
                                            if z // 2 == 0:
                                                z_psw = z_psw + psw[z]
                                            else:
                                                z_psw = psw[j] + z_psw
                                        if line[:-1] == sgnin[0] + z_psw + sgnin[1:]:
                                            ui.alert(text="登录成功！", title=title)
                                            p = open("passwords.txt", 'r+')
                                            psws = p.readlines()
                                            n_psw = ui.prompt(text="欢迎" + sgnin + "!\n请输入您的新密码：", title=title)
                                            if n_psw:
                                                zip_psw = ''
                                                for z in range(len(n_psw)):
                                                    if z // 2 == 0:
                                                        zip_psw = zip_psw + n_psw[z]
                                                    else:
                                                        zip_psw = n_psw[z] + zip_psw
                                                zip_psw = sgnin[0] + zip_psw + sgnin[1:]
                                                psws[j] = zip_psw + '\n'
                                                p.seek(0)
                                                p.writelines(psws)
                                                p.truncate()
                                                ui.alert(text="修改成功！", title=title)
                                            p.close()
                                        else:
                                            ui.alert(text=" 修改密码：\n密码不正确！", title=title)
                                            break
                    case '注销':
                        sgnin = auto_sgn
                        with open('players.txt', 'r') as f:
                            lines = f.readlines()
                            for j, i in enumerate(lines):
                                if i[:-1] == sgnin:
                                    psw = ui.password(text="请输入您的密码以验证身份：", title=title)
                                    if not psw:
                                        break
                                    with open('passwords.txt', 'r') as p:
                                        psws = p.readlines()
                                        line = psws[j]
                                        z_psw = ''
                                        for z in range(len(psw)):
                                            if z // 2 == 0:
                                                z_psw = z_psw + psw[z]
                                            else:
                                                z_psw = psw[j] + z_psw
                                        if line[:-1] == sgnin[0] + z_psw + sgnin[1:]:
                                            p = open("passwords.txt", 'r+')
                                            psws = p.readlines()
                                            confirm = ui.confirm(
                                                text="欢迎" + sgnin + "!\n您确认要注销账号吗？\n（注销后游戏数据无法找回！）",
                                                title=title, buttons=['确定', '还是算了'])
                                            if confirm == '确定':
                                                p.writelines(psws[:j] + psws[j + 1:])
                                                p.truncate()
                                                f.seek(0)
                                                f.writelines(lines[:j] + lines[j + 1:])
                                                f.truncate()
                                                os.chmod(os.getcwd() + "\\" + sgnin, 0o777)
                                                rmtree(os.getcwd() + "\\" + sgnin)
                                                ui.alert(text="注销成功！", title=title)
                                            p.close()
                                        else:
                                            ui.alert(text=" 注销：\n密码不正确！", title=title)
                                            break
                    case '取消自动登录':
                        for j, i in enumerate(players):
                            if i[:-1] == auto_sgn:
                                a.seek(0)
                                a.writelines(players[:j] + players[j + 1:])
                                a.truncate()
                                ui.alert(text="已取消自动登录。下次登录此账号请输入用户名和密码！", title=title)
                                break
                    case _:
                        break

    else:
        with open('auto_sgn.txt', 'w') as a:
            pass
    while not sgn_suc:
        st = ui.confirm(text="请登录以开始游戏", title=title, buttons=["登录", "注册", "修改密码", "注销", "退出"])
        match st:
            case "登录":
                player_name = sgn_in()
                if player_name:
                    auto_sgn = ui.confirm(text="下次是否自动登录？", title=title, buttons=['是', '否'])
                    if auto_sgn == '是':
                        with open('auto_sgn.txt', 'r+') as a:
                            lines = a.readlines()
                            for j, i in enumerate(lines):
                                if i[:-1] == player_name:
                                    a.seek(0)
                                    a.writelines(lines[:j] + lines[j + 1:])
                            a.write(player_name + '\n')
                    elif auto_sgn == '否':
                        with open('auto_sgn.txt', 'r+') as a:
                            lines = a.readlines()
                            for j, i in enumerate(lines):
                                if i[:-1] == player_name:
                                    a.seek(0)
                                    a.writelines(lines[:j]+lines[j+1:])
                                    break
                    return player_name

            case "注册":
                rgt_suc = False
                while not rgt_suc:
                    rgt = ui.prompt(text="注册账号：\n请输入您的用户名：", title=title, default='player')
                    if rgt:
                        if os.path.isfile('players.txt'):
                            pass
                        else:
                            p = open('players.txt', 'w')
                            p.close()
                        with open('players.txt', 'r+') as f:
                            lines = f.readlines()
                            for i in lines:
                                if i[:-1] == rgt:
                                    ui.alert(text=" 注册账号：\n用户已存在！请换一个用户名。", title=title)
                                    break
                            else:
                                f.write(rgt + "\n")
                                psw = ui.prompt(text="注册账号：\n请设置您的密码：", title=title)
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
                                n_psw = ui.prompt(text="欢迎" + player_name + "!\n请输入您的新密码：", title=title)
                                if n_psw:
                                    zip_psw = ''
                                    for z in range(len(n_psw)):
                                        if z // 2 == 0:
                                            zip_psw = zip_psw + n_psw[z]
                                        else:
                                            zip_psw = n_psw[z] + zip_psw
                                    zip_psw = player_name[0] + zip_psw + player_name[1:]
                                    psws[j] = zip_psw + '\n'
                                    p.seek(0)
                                    p.writelines(psws)
                                    p.truncate()
                                    ui.alert(text="修改成功！", title=title)
                                p.close()
            case "注销":
                player_name = sgn_in()
                if player_name:
                    with open('players.txt', 'r') as f:
                        lines = f.readlines()
                        for j, i in enumerate(lines):
                            if i[:-1] == player_name:
                                p = open("passwords.txt", 'r+')
                                psws = p.readlines()
                                confirm = ui.confirm(
                                    text="欢迎" + player_name + "!\n您确认要注销账号吗？\n（注销后游戏数据无法找回！）",
                                    title=title, buttons=['确定', '还是算了'])
                                if confirm == '确定':
                                    p.writelines(psws[:j] + psws[j + 1:])
                                    p.truncate()
                                    f.seek(0)
                                    f.writelines(lines[:j] + lines[j + 1:])
                                    f.truncate()
                                    os.chmod(os.getcwd() + "\\" + player_name, 0o777)
                                    rmtree(os.getcwd() + "\\" + player_name)
                                    ui.alert(text="注销成功！", title=title)
                                p.close()

            case "退出" | _:
                break
