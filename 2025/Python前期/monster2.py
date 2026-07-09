import random
monster_name = ["スライム","ゾンビ","ゴースト","ドラゴン","デーモン"]
monster = {}
monster_HP = {}
heal_count = 2
poison_count = 2

# アタッカーディフェンダー
def attack():
    monster_name_list = list(monster.keys())
    a = random.choice(monster_name_list)
    monster_name_list.remove(a)
    b = random.choice(monster_name_list)
    return (a, b)

# ダメージ計算
def dam(x,y):
    base_DEF = monster[y]["DEF"]
    if "debuff" in monster[y]:
      for _ in range(monster[y]["debuff"]):
        monster[y]["DEF"] = int(monster[y]["DEF"] * 0.8)
      print(y,"の防御力 : ",monster[y]["DEF"])
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
    monster[y]["DEF"] = base_DEF
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

# 魔法ダメージ
def mag_dam(x,y):
    base_DEF = monster[y]["DEF"]
    if "debuff" in monster[y]:
      for _ in range(monster[y]["debuff"]):
        monster[y]["DEF"] = int(monster[y]["DEF"] * 0.8)
    attack_1 = monster[x]["MAG"]
    defense_1 = monster[y]["DEF"]
    D = int((attack_1 - defense_1 / 3) / 2)
    dmg = 0
    if D < 2:
      dmg = random.randint(2,3)
    elif 2 <= D < 9:
      dmg = random.randint(D,D + 2)
    elif 9 <= D:
      dmg = (D * 7) / 8 + ((D / 4 + 1) * random.randint(0,255) )/256
    monster[y]["DEF"] = base_DEF
    return int(dmg)

# 回避
def avoid(a):
    pro = monster[a]["SPD"]
    if 45 <= pro and random.randint(1, 3) == 1:
       return True
    else:
       return False

# モンスター生成
def mons(): 
    li = ["HP","MP","ATK","DEF","SPD","MAG"] 

    for name_mon in monster_name: 
      state = {} 
      for stat_type in li:
        stat = random.randint(10,50)
        state[stat_type] = stat
      monster[name_mon] = state
      # monster_HP[name_mon] = monster[name_mon]["HP"]

    return 

# レベル計算
def level():
    for i in monster:
      lv = 0
      for value in monster[i].values(): 
        lv += value
      lv //= 10
      monster[i]["LV"] = lv
    return

# オッズ計算
def od():
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
    return

# 通常攻撃
def fainal(attacker,deff,avoi,per,dam,c_dam):
    # if "condition" in monster[attacker]:
    #   if monster[attacker]["condition"] == "眠り":
    #     print(f"{attacker}は眠っている")
    #     return
    # if "POWER_UP" in monster[attacker]:
    #   dam = int(dam * 1.5)
    #   c_dam = int(c_dam * 1.5)
    #   monster[attacker]["POWER_UP"] -= 1
    #   if monster[attacker]["POWER_UP"] == 0:
    #       del monster[attacker]["POWER_UP"]
    # if "眠り" not in monster[deff]["condition"]:
    #   if avoi == True:
    #     print(deff,"が回避に成功しました")
    #     return
    if per == True:
      print(deff,f"に会心ダメージが{c_dam}ダメージ入りました")
      monster[deff]["HP"] -= c_dam
      # if "debuff" in monster[deff]:
      #   del monster[deff]["debuff"]
      # if "condition" in monster[attacker]:
      #   if "眠り" in monster[deff]["condition"]:
      #     monster[deff]["condition"].remove("眠り") 
      #     del monster[deff]["condition_count"]["眠り"]
      #     print(f"攻撃によって{deff}の目が覚めた")
      # return
    elif per != True:
      print(deff,f"に{dam}ダメージ入りました")
      monster[deff]["HP"] -= dam
      # if "debuff" in monster[deff]:
      #   del monster[deff]["debuff"]
      # if "condition" in monster[attacker]:
      #   if "眠り" in monster[deff]["condition"]:
      #     monster[deff]["condition"].remove("眠り") 
      #     del monster[deff]["condition_count"]["眠り"]
      #     print(f"攻撃によって{deff}の目が覚めた")
      # return

# 必殺
def ult(attacker,deff,avoi,dam,c_dam):
    if "POWER_UP" in monster[attacker]:
      dam = int(dam * 1.5)
      c_dam = int(c_dam * 1.5)
      monster[attacker]["POWER_UP"] -= 1
      if monster[attacker]["POWER_UP"] == 0:
          del monster[attacker]["POWER_UP"]
    if "眠り" not in monster[deff]["condition"]:
      if avoi == True:
        print(deff,"が回避に成功しました")
        return
    if random.randint(1,2) == 1:
      print(deff,f"に{dam * 2}ダメージ入りました")
      monster[deff]["HP"] -= dam * 2
      if "debuff" in monster[deff]:
        del monster[deff]["debuff"]
      if "condition" in monster[attacker]:
        if "眠り" in monster[deff]["condition"]:
          monster[deff]["condition"].remove("眠り") 
          del monster[deff]["condition_count"]["眠り"]
          print(f"攻撃によって{deff}の目が覚めた")
    else:
       print("攻撃に失敗しました")

# 魔法ダメージ判定
def fainal2(att,deff,avoi,mag):
    if monster[att]["MP"] < 10:
       print("マナが足りません")
       print()
       command(attacker, defender, damege, avoid1, critical_damege)
    if "眠り" not in monster[deff]["condition"]:
      if avoi == True:
        print(deff,"が回避に成功しました")
        return
    else:
      print(deff,f"に{mag}ダメージ入りました")
      monster[deff]["HP"] -= mag
      monster[att]["MP"] -= 10
      if "debuff" in monster[deff]:
        del monster[deff]["debuff"]
      if "condition" in monster[attacker]:
        if "眠り" in monster[deff]["condition"]:
          monster[deff]["condition"].remove("眠り") 
          del monster[deff]["condition_count"]["眠り"]
          print(f"攻撃によって{deff}の目が覚めた")

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

# コマンド
def command(attacker, defender, damage, avoid1, critical_damage):
    print("1:通常攻撃")
    print(f"2:HPを10回復(残り{heal_count}回)")
    print("3:必殺技(ダメージが倍になるが1/2の確率で外れる)")
    print("4:魔法の選択")
    print(f"5:毒攻撃(残り{poison_count}回)")
    com = int(input("行動を選択してください:"))
    # if com == "":
    #   command(attacker, defender, damage, avoid1, critical_damage)
    if com == 1:
      fainal(attacker,defender, avoid1, persent(), damage, critical_damage)
    elif com == 2:
      heal(attacker)
    elif com == 3:
      ult(attacker,defender, avoid1, damage,critical_damege)
    elif com == 4:
      chose_magic()
    elif com == 5:
      poison(defender)

# 回復
def heal(att):
    global heal_count
    if heal_count > 0:
        c = 0
        while c < 10:
          if chose_monster_HP <= monster[att]["HP"]:
            break
          monster[att]["HP"] += 1
          c += 1
          
        heal_count -= 1
        print(f"{att} はHPを10回復した。残り回復回数: {heal_count}")

    else:
        print("回復はもうありません")
        print()
        command(attacker, defender, damege, avoid1, critical_damege)

# 毒攻撃
def poison(deff):
    global poison_count
    if poison_count > 0:
      coin = random.random()
      if coin < 0.7:
        poison_count -= 1
        # monster[deff]["condition"] = []
        monster[deff]["condition"].append("毒")
        monster[deff]["condition_count"]["毒"] = 0
        print("毒状態にしました")
        print(f"残り回数: {poison_count}")
      else:
        poison_count -= 1
        print("毒状態にできませんでした")
        print(f"残り回数: {poison_count}")
      
    else:
        print("毒攻撃はもうできません")
        print()
        command(attacker, defender, damege, avoid1, critical_damege)

# 眠り攻撃
def sleep(att):
    if monster[att]["MP"] < 20:
      print("マナが足りません")
      print()
      command(attacker, defender, damege, avoid1, critical_damege)
    monster[att]["MP"] -= 20
    for i in monster:
       if i != att:
          coin = random.random()
          if coin < 0.4:
            # monster[i]["condition"] = []
            if "眠り" in monster[i]["condition"]:
              pass
            else:
              monster[i]["condition"].append("眠り")
            monster[i]["condition_count"]["眠り"] = 0
            print(f"{i}が眠り状態になった")

# 状態異常解除判定
def conditions(p):
    if "毒" in monster[p]["condition"]:
      monster[p]["condition_count"]["毒"] += 1
      q = monster[p]["condition_count"]["毒"]
      poison_dmg = int(monster_HP[p] * 0.1)
      monster[p]["HP"] -= poison_dmg
      print(f"{p} は毒のダメージを {poison_dmg} 受けた")
      coin = random.random()
      if q > 5:
        if coin < 0.5:
          print(f"{p} の毒が自然に解除された")
          del monster[p]["condition_count"]["毒"]
          monster[p]["condition"].remove("毒")
      elif coin < q * 0.1:
        print(f"{p} の毒が自然に解除された")
        del monster[p]["condition_count"]["毒"]
        monster[p]["condition"].remove("毒")
    if "眠り" in monster[p]["condition"]:
      monster[p]["condition_count"]["眠り"] += 1
      w = monster[p]["condition_count"]["眠り"]
      coin = random.random()
      if w > 3:
        if coin < 0.5:
          print(f"{p} の目が覚めた")
          del monster[p]["condition_count"]["眠り"]
          monster[p]["condition"].remove("眠り")
      elif coin < (w + 2) * 0.1:
        print(f"{p} の目が覚めた")
        del monster[p]["condition_count"]["眠り"]
        monster[p]["condition"].remove("眠り")

# # 眠り解除判定
# def sleeps():
#     a

# 魔法回復
def magic_heal(att,x,chose_monster_HP):
    if chose_monster_HP < monster[att]["HP"] + x:
      print("モンスターの最大HPを超えてしまうので実行できません")
      chose_magic()
      return
    else:
      monster[att]["HP"] += x
      monster[att]["MP"] -= x
      
# 攻撃力アップ
def power(att):
    if monster[att]["MP"] < 15:
        print("MPが足りません")
        chose_magic()
        return
    monster[att]["MP"] -= 15
    monster[att]["POWER_UP"] = 2
    print(f"{att} の次の2回分の攻撃が1.5倍")

# デバフ
def debuf(chose):
    if monster[chose]["MP"] < 15:
        print("MPが足りません")
        chose_magic()
        return
    monster[chose]["MP"] -= 15
    for i in monster:
        if i != chose:
            if "debuff" in monster[i]:
                if monster[i]["debuff"] < 2:
                    monster[i]["debuff"] += 1
            else:
                monster[i]["debuff"] = 1
    print("敵にデバフを付与しました（攻撃を受けると解除）")

# 魔法選択
def chose_magic():
    print()
    print("1:魔法攻撃(MPを10消費)")
    print("2:回復魔法(MP1消費につきHP1を回復)")
    print("3:自身が2回攻撃するまで攻撃力1.5倍(MPを15消費)")
    print("4:自分以外のモンスターの防御力ダウン(攻撃をくらったら解除)(MPを15消費)")
    print("5:眠り攻撃(MP20消費)")
    chose = int(input("→"))
    if chose == 1:
      fainal2(attacker,defender,avoid1,mag_damege)
    elif chose == 2:
      x = int(input("消費MPを入力してください"))
      magic_heal(attacker,x,chose_monster_HP)
    elif chose == 3:
      power(attacker)
    elif chose == 4:
      debuf(chose_monster)
    elif chose == 5:
      sleep(attacker)


mons()
level()
od()
for name, state in monster.items():
  monster[name]["condition"] = []
  monster[name]["condition_count"] = {}
  print(name,state)
print(monster_HP)
chose_monster = input("モンスター名を入力してください:")
betto = int(input("賭ける額を決めてください:"))
chose_monster_HP = monster[chose_monster]["HP"]
print()
while True:
  persent()

  for p in monster:
    if "condition" in monster[p]:
      if "毒" in monster[p]["condition"] or "眠り" in monster[p]["condition"]:  
        conditions(p)
  
  if finish():
    winner = list(monster.keys())[0] 
    print(f"{winner} が勝利しました！")
    if winner == chose_monster:
      print("賭けに成功しました！")
      print("賞金 : ",monster[winner]["odds"] * betto)
    else:
       print("賭けに失敗しました")
    break

  for name, state in monster.items():
    print(name,state)

  attacker,defender = attack()
  damege = dam(attacker,defender) # ダメージ
  critical_damege =critical_dmg(attacker) # クリティカルダメージ
  mag_damege = mag_dam(attacker,defender) # 魔法ダメージ

  print("attacker =",attacker,"defender =",defender)
  avoid1 = avoid(defender) 

  if attacker == chose_monster:
     command(attacker, defender, damege, avoid1, critical_damege)
  else:
    fainal(attacker,defender,avoid1,persent(),damege,critical_damege)

  if finish():
    winner = list(monster.keys())[0] 
    print(f"{winner} が勝利しました！")
    if winner == chose_monster:
      print("賭けに成功しました！")
      print("賞金 : ",monster[winner]["odds"] * betto)
    else:
       print("賭けに失敗しました")
    break
  else:
    play = input("もう一度プレイ(エンターを押してください)")
  print()