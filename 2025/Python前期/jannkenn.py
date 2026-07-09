c = 0
p = 0
while True :
  player = input("じゃんけんの手入力してね→")
  print("あなたの手➡︎"+player)

  import random
  computer = random.randint(1,3)

  if computer == 1:
    print("コンピューターの手➡︎グー")
    computer = "グー"

  elif computer == 2:
    print("コンピューターの手➡︎チョキ")
    computer = "チョキ"

  elif computer == 3:
    print("コンピューターの手➡︎パー")
    computer = "パー"

  # ↑じゃんけんの手の設定
    
  if computer == player:
    print("あいこ")
    continue
    
  elif computer == "グー" and player== "パー" or computer == "チョキ" and player== "グー" or computer == "パー" and player== "チョキ":
    print("じゃんけん：勝ち")
    p1 = "win"

  elif computer == "チョキ" and player== "パー" or computer == "パー" and player== "グー" or computer == "グー" and player== "チョキ":
    print("じゃんけん：負け")
    p1 = "rose"

  else:
    print("カタカナで入力してください")
    continue

  computer_n = random.randint(1,4)

  if computer_n == 1:
    computer_n = "上"

  elif computer_n == 2:
    computer_n = "右"

  elif computer_n == 3:
    computer_n = "下"

  elif computer_n == 4:
    computer_n = "左"

  # ↑あっち向いてホイの設定

  if p1 == "win":
    player_p = input("あっち向いてほいを漢字で入力してください→")
    print("あなたの手➡︎"+player_p)
    print("コンピューターの向き➡︎", computer_n)
    if player_p == computer_n:
      print("あなたの勝ちです")
      p += 1
    
    elif player_p != computer_n:
      continue

  if p1 == "rose":
    player_c = input("あっち向いてほいを漢字で入力してください→")
    print("あなたの手➡︎"+player_c)
    print("コンピューターの向き➡︎", computer_n)
    if player_c == computer_n:
      print("コンピューターの勝ちです")
      c += 1

    elif player_c != computer_n:
      continue

  if c == 3:
    print("先に3勝されたのであなたの負けです")

  if p == 3:
    print("先に3勝したのであなたの勝ちです")