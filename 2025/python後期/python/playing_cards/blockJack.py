import card
import makeplayer
class Blackjack:
  def __init__(self):
    self.dealer_hands = []
    self.players = []
    self.dealer_score = 0

  def start(self):
    self.total_player = int(input("何人でプレイしますか？:"))
    for i in range(self.total_player):
      player = makeplayer.Player(i+1) 
      self.players.append(player)
      
  def play(self):
    self.card_deck = card.Card()
    for player in self.players:
      while True:
        try:
          bet = int(input(f"Player{player.id} の賭け金を入力してください: "))
          if bet > 0 and bet <= player.chip:
            break
          else:
            print("⚠️ 1以上の数字を入力してください")
        except ValueError:
          print("⚠️ 数字を入力してください")

      player.bet = bet
      player.chip -= bet
      player.player_hands = []  # 前ラウンドの手札をクリア
      for _ in range(2):
        player.player_hands.append(self.card_deck.draw())
      # player.player_hands = ["♢10","♡10"]
      player.score = self.calc_score(player.player_hands)
    self.dealer_hands = []
    self.dealer_hands.append(self.card_deck.draw())
    # self.dealer_hands = ["♢1"]
    self.calc_dealer_score()
    self.open()
    

  def open(self):
    print()
    input("手札をオープン[Enter]")
    print("dealer hands:",self.dealer_hands,",score:",self.dealer_score)
    for p in self.players:
      print("playerID:",p.id,",hands:",p.player_hands,",score:",p.score)
      if p.player_hands2:
        print("playerID:",p.id,",hands2:",p.player_hands2,",score2:",p.score_2)
    print()

  def special_rules(self, player):
    self.choices = []
    self.choices.append("1:Doubling Down")
    if len(player.player_hands) == 2 and self.get_value(player.player_hands[0]) == self.get_value(player.player_hands[1]):
      self.choices.append("2:Splitting Pairs")
    if self.get_value(self.dealer_hands[0]) == 11:
      self.choices.append("3:Insurance")
    if (len(player.player_hands) == 2 and player.score == 21) and self.get_value(self.dealer_hands[0]) == 11:
      self.choices.append("4:Even Money")
    self.choices.append("5:Surrender")
    self.choices.append("6:何もしない")
    self.special_rules2()

    valid_numbers = [int(choice.split(":")[0]) for choice in self.choices]

    while True:
      try:
        special = int(input(f"player{player.id}: 特殊ルールを実行しますか？{self.choices} > "))
        if special in valid_numbers:
          break
        else:
          print(f"⚠️ {valid_numbers} の中から選んでください")
      except ValueError:
          print("⚠️ 数字を入力してください")
    if special == 1:
      #ダブリングダウン
      #賭け金をオリジナルベットと同額まで上乗せして賭けることが出来ます。ただし、カードは1枚しか引けません。
      player.chip -= player.bet
      print(f"{player.bet}chipを上乗せして賭けました")
      player.bet *= 2
    elif special == 2:
      #スプリッティングペアー
      #最初の2枚のカードが同数の際、オリジナルベットと同額の賭け金を追加することで、2手に分けて勝負することが出来ます。”A”のスプリットのときは、追加カードは1枚のみとなります。
      li = player.player_hands.pop()
      player.player_hands2 = [li]
      player.bet2 = player.bet
      player.chip -= player.bet2
      player.score = self.calc_score(player.player_hands)
      player.score_2 = self.calc_score(player.player_hands2)
    if special == 3:
      #インシュアランス
      #	ディーラーのアップカード（見せ札）が”A”の時、ディーラーのブラックジャックに対して 保険をかけることが出来ます。保険金は掛け捨てで、元の賭け金の半額までを保険に充てられます。 ディーラーがブラックジャックだった場合は元の賭け金は回収されますが、保険金への配当は2 to 1（3倍）です。
      while True:
        player.insurance = int(input(f"保険をいくらかけますか？ (賭け金 {player.bet} の半額まで): "))
        if player.insurance * 2 > player.bet:
            print("保険額が大きすぎます。もう一度入力してください。")
            continue 
        else:
            # player.bet -= player.insurance
            player.chip -= player.insurance
            print(f"Player{player.id} は {player.insurance} チップを保険にかけました")
            break 
    elif special == 4:
      #イーブンマネー
      #	プレイヤーがブラックジャックで、ディーラーのアップカードが”A”だった場合、ディーラーのブラックジャックを確認する前に配当を先にもらえるルールです。この場合の配当は2.5倍ではなく、2倍の配当になります。
      win = player.bet
      player.chip += player.bet + win
      print(f"player {player.id}はEven Moneyで {win} チップ獲得しました")
      player.special.append("skip")
      player.special.append("pass")
    elif special == 5:
      #サレンダー
      #降参すること。始めの2枚のカードが配られた時点で、賭け金の半額を放棄し、残りの半額だけを返してもらい勝負を降りることができます。
      print(f"player {player.id}は {player.bet * 0.5}チップ失いました")
      player.chip += player.bet * 0.5
      player.special.append("skip")
      player.special.append("pass")
    elif special == 6:
      #特殊ルールを使用せずHITSTANDに行く
      pass
    
    return special

  def special_rules2(self):
    print()
    if "1:Doubling Down" in self.choices:
      print("1:Doubling Down/賭け金をオリジナルベットと同額まで上乗せして賭けることが出来ます。ただし、カードは1枚しか引けません。")
    if "2:Splitting Pairs" in self.choices:
      print("2:Splitting Pairs/オリジナルベットと同額の賭け金を追加することで、2手に分けて勝負することが出来ます。”A”のスプリットのときは、追加カードは1枚のみとなります。")
    if "3:Insurance" in self.choices:
      print("3:Insurance/ディーラーのブラックジャックに対して 保険をかけることが出来ます。保険金は掛け捨てで、元の賭け金の半額までを保険に充てられます。 ディーラーがブラックジャックだった場合は元の賭け金は回収されますが、保険金への配当は2 to 1（3倍）です。")
    if "4:Even Money" in self.choices:
      print("4:Even Money/ディーラーのブラックジャックを確認する前に配当を先にもらえるルールです。この場合の配当は1.5倍ではなく、1倍（イーブン）の配当になります。")
    if "5:Surrender" in self.choices:
      print("5:Surrender/降参すること。始めの2枚のカードが配られた時点で、賭け金の半額を放棄し、残りの半額だけを返してもらい勝負を降りることができます。")
    print()

  def operation(self, player):
    sp = self.special_rules(player)
    # print(sp)
    if "skip" in player.special:
      print(f"Player{player.id} は特殊ルールを選択したので通常の操作をスキップします")
      input("次の人に移ります[Enter]")
      print()
      return 
    
    elif sp == 1:
      print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
      input("一枚カードをめくります")
      player.player_hands.append(self.card_deck.draw())
      player.score = self.calc_score(player.player_hands)
      print()
      print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
      # print()
      if player.score > 21:
          # print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
          print("Bust!")
          player.score = 0
          input("次の人に移ります[Enter]")
          print()
          return
      input("Doubling Downを選択したので次に移ります[Enter]")
      print()
  
      
    elif sp == 2:
      if player.score == 11:
        print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
        input("一枚カードをめくります")
        player.player_hands.append(self.card_deck.draw())
        player.score = self.calc_score(player.player_hands)
        print()
        print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
        # print()
        if player.score > 21:
            # print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
            print("Bust!")
            player.score = 0
            input("次の人に移ります[Enter]")
            print()
            return
        input("Splitting PairsのカードがAだったので次に移ります[Enter]")
        print()

        print(f"Player{player.id} hands:",player.player_hands2,",score2:",player.score_2)
        input("一枚カードをめくります")
        player.player_hands2.append(self.card_deck.draw())
        player.score_2 = self.calc_score(player.player_hands2)
        print()
        print(f"Player{player.id} hands:",player.player_hands2,",score2:",player.score_2)
        # print()
        if player.score_2 > 21:
            # print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
            print("Bust!")
            player.score_2 = 0
            input("次の人に移ります[Enter]")
            print()
            return
        input("次の人に移ります[Enter]")
        print()
      
      elif player.score_2 != 0:
        while True:
          # print("A")
          print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
          while True:
            try:
                chose = int(input(f"Player{player.id} 1,HIT / 2,STAND : "))
                if chose in (1, 2):
                    break
                else:
                    print("⚠️ 1か2を入力してください")
            except ValueError:
                print("⚠️ 数字を入力してください")

          if chose == 1:
            player.player_hands.append(self.card_deck.draw())
            player.score = self.calc_score(player.player_hands)
            # print(f"hands:{player.player_hands} score:{player.score}")
            print()
            if player.score > 21:
              print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
              print("Bust!")
              player.score = 0
              input("次に移ります[Enter]")
              print()
              break
          else:
            input("次に移ります[Enter]")
            print()
            break
        
        while True:
          # print("A")
          print(f"Player{player.id} hands2:",player.player_hands2,",score:",player.score_2)
          while True:
            try:
                chose = int(input(f"Player{player.id} 1,HIT / 2,STAND : "))
                if chose in (1, 2):
                    break
                else:
                    print("⚠️ 1か2を入力してください")
            except ValueError:
                print("⚠️ 数字を入力してください")

          if chose == 1:
            player.player_hands2.append(self.card_deck.draw())
            player.score_2 = self.calc_score(player.player_hands2)
            # print(f"hands:{player.player_hands2} score:{player.score}")
            print()
            if player.score_2 > 21:
              print(f"Player{player.id} hands2:",player.player_hands2,",score2:",player.score_2)
              print("Bust!")
              player.score_2 = 0
              input("次の人に移ります[Enter]")
              print()
              break
          else:
            input("次の人に移ります[Enter]")
            print()
            break

    # 操作　ヒットスタンド
    else:
      while True:
        # print("A")
        print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
        while True:
          try:
              chose = int(input(f"Player{player.id} 1,HIT / 2,STAND : "))
              if chose in (1, 2):
                  break
              else:
                  print("⚠️ 1か2を入力してください")
          except ValueError:
              print("⚠️ 数字を入力してください")

        if chose == 1:
          player.player_hands.append(self.card_deck.draw())
          player.score = self.calc_score(player.player_hands)
          # print(f"hands:{player.player_hands} score:{player.score}")
          print()
          if player.score > 21:
            print(f"Player{player.id} hands:",player.player_hands,",score:",player.score)
            print("Bust!")
            player.score = 0
            input("次の人に移ります[Enter]")
            print()
            break
        else:
          input("次の人に移ります[Enter]")
          print()
          break

  def operation_d(self):
    input("ディーラーの行動[Enter]")
    input("一枚ドローします[Enter]")
    self.dealer_hands.append(self.card_deck.draw())
    # self.dealer_hands.append("♡10")
    self.calc_dealer_score()
    while True:
      if self.dealer_score < 17:
        print("hands:",self.dealer_hands,",score:",self.dealer_score)
        input("一枚ドローします[Enter]")
        self.dealer_hands.append(self.card_deck.draw())
        self.calc_dealer_score()
        print("hands:",self.dealer_hands,",score:",self.dealer_score)
        print()
        if self.dealer_score > 21:
          print("ディーラーはバーストしました。")
          self.dealer_score = 0
          break
      else:
        if len(self.dealer_hands) == 2:
          print("hands:",self.dealer_hands,",score:",self.dealer_score)
        print(f"ディーラーはスコア {self.dealer_score} でストップしました。")
        break

  def get_value(self, card):
    # print(card)
    num = int(card[1:])
    if num > 10:
      return 10
    elif num == 1:
      return 11
    return num

  def calc_score(self, hands):
    vals = [ self.get_value(c) for c in hands ] 
    total = sum(vals)
    aces = vals.count(11)  

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    return total

  def calc_dealer_score(self):
    vals = [ self.get_value(c) for c in self.dealer_hands ]
    total = sum(vals)
    aces = vals.count(11)

    while total > 21 and aces > 0:
        total -= 10
        aces -= 1

    self.dealer_score = total

  def last(self):
      print()
      self.open()
      print()

      input("=== 結果発表 ===")
      for p in self.players:
        # self.resolve_player(p)   # 個別に処理
        self.resolve_split(p)    # 個別に処理
        p.special = []  # 毎ラウンド終了時にリセット
      
      print()
      print("--現在のチップ数--")
      for p in self.players:
        print(f"player {p.id}の現在のチップ数: {p.chip}")
      input()

  def result(self, p):
      
      if "pass" in p.special:
        pass
      
      elif (len(p.player_hands) == 2 and p.score == 21) and self.dealer_score != 21:
        return "BJ"
      elif p.score > self.dealer_score:
        return "WIN"
      elif p.score == self.dealer_score:
        return "TIE"
      else:
        return "LOSE"
        
  def resolve_player(self, p):  # pを引数で受け取る
    resolve = self.result(p)

    if "pass" in p.special:
        return
    elif resolve == "BJ":
        win = p.bet * 1.5
        p.chip += p.bet + win
        print(f"player {p.id}はBJで勝ったので {win} チップ獲得しました")
    elif resolve == "WIN":
        win = p.bet
        p.chip += p.bet + win
        print(f"player {p.id}は勝ったので {win} チップ獲得しました")
    elif resolve == "TIE":
        p.chip += p.bet
        print(f"player {p.id}は引き分けでした")
    else:
        print(f"player {p.id}は負けたので {p.bet} チップ失いました")
    p.bet = 0

    # インシュアランス判定
    if p.insurance > 0 and (len(self.dealer_hands) == 2 and self.dealer_score == 21):
        print(f"ディーラーBJ! Player{p.id} は {p.insurance * 2} チップ獲得しました")
        p.chip += p.insurance * 3
    p.insurance = 0

    
  def resolve_split(self, p):  
    # 分割していなければ処理しない
    if not hasattr(p, "player_hands2") or not p.player_hands2:
        self.resolve_player(p)
        return  

    # 分割1（元の手）
    resolve1 = self.result(p)  # 元の手は既存の result をそのまま使う

    if resolve1 == "WIN":
        win = p.bet
        p.chip += p.bet + win
        print(f"player {p.id} のハンド1は勝ったので {win} チップ獲得しました")
    elif resolve1 == "TIE":
        p.chip += p.bet
        print(f"player {p.id} のハンド1は引き分けでした")
    else:
        print(f"player {p.id} のハンド1は負けたので {p.bet} チップ失いました")

    # 分割2
    if p.score_2 > self.dealer_score and p.score_2 <= 21:
        win = p.bet2
        p.chip += p.bet2 + win
        print(f"player {p.id} のハンド2は勝ったので {win} チップ獲得しました")
    elif p.score_2 == self.dealer_score:
        p.chip += p.bet2
        print(f"player {p.id} のハンド2は引き分けでした")
    else:
        print(f"player {p.id} のハンド2は負けたので {p.bet2} チップ失いました")

    # 分割終了後にベットをリセット
    p.bet = 0
    p.bet2 = 0



game = Blackjack()
game.start()
while True:
  
  game.play()

  for p in game.players:
      print("playerID:",p.id,",hands:",p.player_hands,",score:",p.score)
      game.operation(p)
  game.operation_d()
  # game.resolve_player()
  game.last()