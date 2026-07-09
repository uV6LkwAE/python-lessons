import random
def attack():
    monster_name_list = list(monster.keys())
    a = random.choice(monster_name_list)
    monster_name_list.remove(a)
    b = random.choice(monster_name_list)
    return (a, b)

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
      
def critical_dmg(y):
    atk = int(monster[y]["ATK"] * random.randint(55,65) / 64)
    return atk

def avoid(a):
    pro = monster[a]["SPD"]
    print(a,"SPD = ",pro)
    if 45 <= pro:
       return True
    elif pro < 45:
       return False
    
while True:
  monster_name = ["a","b","c","d","e"]
  monster = {}
  li = ["HP","MP","ATK","DEF","SPD","MAG"]
  odds = []
  for x in range(len(monster_name)):
    state = {}
    
    for i in range(len(li)):
      s = random.randint(10,50)
      state[li[i]] = s

    lv = 0
    for value in state.values():
      lv += value
    lv //= 10
    state["lv"] = lv
    monster[monster_name[x]]= state


    odd = (lv,monster_name[x])
    odds.append(odd)
  odds.sort(reverse=True)
  print(odds)

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

  for name, state in monster.items():
    print(name,state)


  attacker,defender = attack()

  print("attacker =",attacker,"defender =",defender)
  print("damage =",dam(attacker,defender))
  print("critical_dmg =",critical_dmg(attacker))
  print(avoid(defender))
  break