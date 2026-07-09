import card
class Bakara:
  def __init__(self, card_deck):
    self.card_deck = card_deck
    self.player_hands = []
    self.banker_hands = []
    self.player_drawn_card = None
    self.chose = int(input("どちらに賭けますか？ 1.player / 2.banker / 3.draw :"))
    self.betto = int(input("いくら賭けますか？:"))

  def start(self):
    self.card_deck = card.Card()
    self.player_hands = []
    self.banker_hands = []
    
    for _ in range(2):
      self.player_hands.append(self.card_deck.draw())
      self.banker_hands.append(self.card_deck.draw())
    self.player_sum = sum(self.get_value(c) for c in self.player_hands) % 10
    self.banker_sum = sum(self.get_value(c) for c in self.banker_hands) % 10
    # self.player_sum = 6
    # self.banker_sum = 6
    return self.player_hands, self.banker_hands, self.player_sum,self.banker_sum
  
  @staticmethod
  def get_value(card_str):
    num = int(card_str[1:])
    if num >= 10:
      return 10
    return num

  def open(self):
    if self.chose == 1 or self.chose == 3:
      print("--プレイヤー側の手札--")
      for i in self.player_hands:
        print(i)
        input()
      print("player_hands:",self.player_hands,"total:",self.player_sum) 
      print()
      print("--バンカー側の手札--")
      print(self.banker_hands[0])
      input()
      print(self.banker_hands[1])
      print()
      print("banker_hands:",self.banker_hands,"total:",self.banker_sum) 
      print()

    elif self.chose == 2:
      print("--バンカー側の手札--")
      for j in self.banker_hands:
        print(j)
        input()
      print("banker_hands:",self.banker_hands,"total:",self.banker_sum) 
      print()
      print("--プレイヤー側の手札--")
      print(self.player_hands[0])
      input()
      print(self.player_hands[1])
      print()
      print("player_hands:",self.player_hands,"total:",self.player_sum) 
      print()

  def open_hands(self):
    input("-player-")
    print("player_hands:",self.player_hands,"total:",self.player_sum) 
    input("-banker-")
    print("banker_hands:",self.banker_hands,"total:",self.banker_sum) 
    print()

  def third_card_rule(self):
    self.player_drawn_card = None
    if self.player_sum <= 5 and self.banker_sum <= 7:
      self.player_drawn_card = self.card_deck.draw()

      if self.banker_sum <= 2:
        input("プレイヤー,バンカー共に3枚目を開きます ")
        self.player_hands.append(self.player_drawn_card)
        # self.player_hands.append(self.card_deck.draw())
        self.banker_hands.append(self.card_deck.draw())

      elif self.banker_sum < 7:
        input("プレイヤーの3枚目を開きます ")
        self.player_hands.append(self.player_drawn_card)
        self.p_val = self.get_value(self.player_drawn_card)
        b_sum = self.banker_sum
        # ルール表に基づく条件分岐
        if b_sum <= 2:
            self.open_hands()
            input("バンカーの3枚目を開きます ")
            self.banker_hands.append(self.card_deck.draw())
        elif b_sum == 3 and self.p_val not in (8,):
            self.open_hands()
            input("バンカーの3枚目を開きます ")
            self.banker_hands.append(self.card_deck.draw())
        elif b_sum == 4 and self.p_val in (2, 3, 4, 5, 6, 7):
            self.open_hands()
            input("バンカーの3枚目を開きます ")
            self.banker_hands.append(self.card_deck.draw())
        elif b_sum == 5 and self.p_val in (4, 5, 6, 7):
            self.open_hands()
            input("バンカーの3枚目を開きます ")
            self.banker_hands.append(self.card_deck.draw())
        elif b_sum == 6 and self.p_val in (6, 7):
            self.open_hands()
            input("バンカーの3枚目を開きます ")
            self.banker_hands.append(self.card_deck.draw())

      elif self.banker_sum == 7:
        input("プレイヤーの3枚目を開きます ")
        self.player_hands.append(self.card_deck.draw())

    elif self.player_sum <= 7 and self.banker_sum <= 5:
      input("バンカーの3枚目を開きます")
      self.banker_hands.append(self.card_deck.draw())

    else:
      input("何も開きません")
    self.player_sum = sum(self.get_value(c) for c in self.player_hands) % 10
    self.banker_sum = sum(self.get_value(c) for c in self.banker_hands) % 10
    
    self.open_hands()

    self.judge1 = self.judge()
    if self.judge1 == "lose":
      print(self.betto, "チップ失いました")
    elif self.judge1 == "tie":
      print("引き分けなので掛け金はそのままです")

    print()
    input("次のゲームを開始[Enter]")
    print()
      
  def judge(self):
      if self.player_sum == self.banker_sum:
          print("引き分けです")
          if self.chose == 3:
              print(self.betto * 9, "チップ返ってきました")
              return "win"
          return "tie"
      elif self.player_sum < self.banker_sum:
          print("bankerの勝利です")
          if self.chose == 2:
              print(self.betto * 1.95, "チップ返ってきました")
              return "win"
          return "lose"
      else:
          print("playerの勝利です")
          if self.chose == 1:
              print(self.betto * 2, "チップ返ってきました")
              return "win"
          return "lose"


while True:
  card = card.Card()
  print(card.cards)
  play = Bakara(card)

  # drawn_card = play.start()
  # player_hands, banker_hands, player_sum, banker_sum  = drawn_card

  play.start()
  play.open()
  play.third_card_rule()