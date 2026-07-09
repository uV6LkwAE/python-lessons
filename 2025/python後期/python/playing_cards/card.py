import random
class Card:
  mark = ["♢","♡","♧","♤"]

  def __init__(self):
    self.cards = []
    self.make_card()
  
  def make_card(self):
    for i in Card.mark:
      for j in range(1,14):
        self.cards.append(f"{i}{j}")

  def draw(self):
    if not self.cards:
      print("カードがなくなりました。")
      return "No card"
    pick = random.choice(self.cards)
    self.cards.remove(pick)
    return pick