from flask import Flask, request, render_template,session
import random

app = Flask(__name__)
app.secret_key = "user"


turn = 1
heal_count = 2

@app.route("/")
def index():
  global monster
  monster = {}
  monster_name = ["スライム","ゾンビ","ゴースト","ドラゴン","デーモン"]
  li = ["HP","MP","ATK","DEF","SPD","MAG"] 

  for name_mon in monster_name: 
    state = {} 
    for stat_type in li:
      stat = random.randint(10,50)
      state[stat_type] = stat
    monster[name_mon] = state
  for i in monster:
    lv = 0
    for value in monster[i].values(): 
      lv += value
    lv //= 10
    monster[i]["LV"] = lv

  odds = []
  for x in monster:
    odd = (monster[x]["LV"],x)
    odds.append(odd)
  odds.sort(reverse=True)

  odds_rank = 2
  z = 0
  while z < len(odds):
    current_lv = odds[z][0] 
    same_lv = []

    j = z
    while j < len(odds) and odds[j][0] == current_lv:
      same_lv.append(odds[j][1])
      j += 1

    odds_avg = odds_rank + (len(same_lv) - 1) / 2

    if odds_avg == int(odds_avg): 
      odds_avg = int(odds_avg)
        
    for name_in_group in same_lv:
      monster[name_in_group]["odds"] = odds_avg

    odds_rank += len(same_lv)
    z = j

  # session["monster"] = monster

  return render_template("battlemon.html", monster = monster, names=monster_name)


@app.route("/action", methods = ["GET","POST"])
def action():
  global turn
  if turn == 1:
    if request.method == "POST":
        session["choise"] = request.form["choise"]
        session["bet"] = request.form["bet"]
    else:
        session["choise"] = request.args.get("choise")
        session["bet"] = request.args.get("bet")

  choise = session.get("choise")
  bet = session.get("bet")

  message = "次のターンへ"
  


  session['attacker'], session['defender'] = attack()
  attacker = session.get("attacker")
  defender = session.get("defender")
  session['damage'] = dam(attacker, defender)
  damage = session.get("damage")
  session['cri'] = persent()  # 会心フラグ
  cri = session.get("cri")
  session['critical_damage'] = critical_dmg(attacker)
  critical_damage = session.get("critical_damage")
  session['avoid1'] = avoid(defender)
  avoid1 = session.get("avoid1")

  actions = None
  move = None
  if choise == attacker:
    # action = command(attacker,chose_monster_HP, defender, dmg, av, c_dmg)
    actions = {1:"通常攻撃",2:f"HPを10回復(残り{heal_count}回)",3:"必殺技(ダメージが倍になるが1/2の確率で外れる)"}
  else:
    move = fainal(attacker, defender, avoid1, cri, damage, critical_damage)
  fin = finish()

  if fin == True:
     message = "今回の結果"
  turn += 1
  return render_template("battlemon.html",message=message,monster=monster,actions=actions,move=move,fin=fin,turn=turn,choise=choise,bet=bet)


@app.route('/move', methods = ["GET"])
def monster_action():
  com = int(request.args.get("mov", 0))
  choise = session.get("choise")
  attacker = session.get("attacker")
  defender = session.get("defender")
  damage = session.get("damage")
  critical_damage = session.get("critical_damage")
  avoid1 = session.get("avoid1")
  chose_monster_HP = monster[choise]["HP"]

  if com == 1:
    move = fainal(attacker,defender, avoid1, persent(), damage, critical_damage)
  elif com == 2:
    move = heal(attacker,chose_monster_HP,defender, damage, avoid1, critical_damage)
  elif com == 3:
    move = ult(attacker,defender, avoid1, damage,critical_damage)

  turn += 1

  return render_template("battlemon.html", move = move)


@app.route('/result', methods = ["GET","POST"])
def result():
  message = "result"
  success = None
  choise = session.get("choise")
  bet = session.get("bet")

  keys = list(monster.keys())

  if len(keys) != 1:
      print("モンスターが1体ではありません")
  else:
      winner = keys[0]
      if winner == choise:
          bet = int(bet)
          success = bet * monster[winner]["odds"]
  
  return render_template("battlemon.html",last_monster=monster,message=message,choise=choise,bet=bet,winner=winner,success=success)



# アタッカーディフェンダー
def attack():
    monster_name_list = list(monster.keys())
    a = random.choice(monster_name_list)
    monster_name_list.remove(a)
    b = random.choice(monster_name_list)
    return (a, b)


# ダメージ計算
def dam(x,y):
    attack_1 = monster[x]["ATK"]
    defense_1 = monster[y]["DEF"]
    D = int((attack_1 - defense_1 / 2) / 2)
    dmg = 0
    if D < 2:
      dmg = random.randint(0,1)
    elif 2 <= D < 9:
      dmg = random.randint(D - 2,D)
    elif 9 <= D:
      dmg = (D * 7) / 8 + ((D / 4 + 1) * random.randint(0,255) )/256
    return int(dmg)


# 会心ダメージ
def critical_dmg(y):
    atk = int(monster[y]["ATK"] * random.randint(55,65) / 64)
    return atk


# 会心率
def persent():
    if random.randint(1, 50) == 1:
       return True
    else:
       return False
    

# 回避
def avoid(a):
    pro = monster[a]["SPD"]
    if 45 <= pro and random.randint(1, 3) == 1:
       return True
    else:
       return False
    

#必殺
def ult(attacker,deff,avoi,dam,c_dam):
    # if "POWER_UP" in monster[attacker]:
    #   dam = int(dam * 1.5)
    #   c_dam = int(c_dam * 1.5)
    #   monster[attacker]["POWER_UP"] -= 1
    #   if monster[attacker]["POWER_UP"] == 0:
    #       del monster[attacker]["POWER_UP"]
    # if "眠り" not in monster[deff]["condition"]:
    if avoi == True:
      return f"{deff}が回避に成功しました"
      return
    if random.randint(1,2) == 1:
      return f"{deff}に{dam * 2}ダメージ入りました"
      monster[deff]["HP"] -= dam * 2
      # if "debuff" in monster[deff]:
      #   del monster[deff]["debuff"]
      # if "condition" in monster[attacker]:
      #   if "眠り" in monster[deff]["condition"]:
      #     monster[deff]["condition"].remove("眠り") 
      #     del monster[deff]["condition_count"]["眠り"]
      #     print(f"攻撃によって{deff}の目が覚めた")
    else:
       return "攻撃に失敗しました"


# 回復
def heal(att,chose_monster_HP,defender, damege, avoid1, critical_damege):
    global heal_count
    if heal_count > 0:
        c = 0
        while c < 10:
          if chose_monster_HP <= monster[att]["HP"]:
            break
          monster[att]["HP"] += 1
          c += 1
          
        heal_count -= 1
        return f"{att} はHPを10回復した。残り回復回数: {heal_count}"

    else:
        # print("回復はもうありません")
        # print()
        command(att, defender, damege, avoid1, critical_damege)

# 通常攻撃
def fainal(att,deff,avoi,per,dam,c_dam):
    if avoi == True:
      # print(deff,"が回避に成功しました")
      return f"{deff}が回避に成功しました"
    if per == True:
      # print(deff,f"に会心ダメージが{c_dam}ダメージ入りました")
      monster[deff]["HP"] -= c_dam
      return f"{att}が{deff}に会心ダメージを{c_dam}ダメージ入れました"
    elif per != True:
      # print(deff,f"に{dam}ダメージ入りました")
      monster[deff]["HP"] -= dam
      return f"{att}が{deff}に{dam}ダメージ入れました"


# コマンド
def command(attacker,chose_monster_HP, defender, damage, avoid1, critical_damage):
    # print("1:通常攻撃")
    # print(f"2:HPを10回復(残り{heal_count}回)")
    # print("3:必殺技(ダメージが倍になるが1/2の確率で外れる)")
    act = ["1:通常攻撃",f"2:HPを10回復(残り{heal_count}回)","3:必殺技(ダメージが倍になるが1/2の確率で外れる)"]

    # com = int(input("行動を選択してください:"))

    # if com == 1:
    #   fainal(attacker,defender, avoid1, persent(), damage, critical_damage)
    # elif com == 2:
    #   heal(attacker,chose_monster_HP,defender, damage, avoid1, critical_damage)
    # elif com == 3:
    #   ult(attacker,defender, avoid1, damage,critical_damage)

    return act


# 終了判定
def finish():
    defeated = []
    for name in list(monster.keys()): 
        if monster[name]["HP"] <= 0:
            defeated.append(name)
    for name in defeated:
        del monster[name]
        print(f"{name} が戦闘不能になりました")
    if len(monster) == 1:  
        return True
    return False



if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
