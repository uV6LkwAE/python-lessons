import random

bingo = []
num = []
for a in range(1,100):
    num.append(a)

for x in range(5):
    li = []
    i = 0
    while i < 5:
      if x == 2 and i == 2:
        li.append("x")
        i += 1
      a= random.randint(1,99)
      if a in num:
        li.append(a)
        num.remove(a)
        i += 1
    bingo.append(li)
      
    print(li)


pick = []
for a in range(1,100):
  pick.append(a)

while True:
  play = input("ボールを取って下さい(一度Enterを押して下さい)")
  pic = random.choice(pick)
  print("pic = "+str(pic))
  pick.remove(pic)

  for p in range(5):
    for q in range(5):
      if bingo[p][q] == pic:
        bingo[p][q] = "x"
    print(bingo[p])

  bingo_count = 0
  for line in range(5):
    if all(cell == "x" for cell in bingo[line]):
      print("BINGO")
      bingo_count += 1
    
  for index in range(5):
    if bingo[0][index] == bingo[1][index] == bingo[2][index] == bingo[3][index] == bingo[4][index]:
      print("BINGO")
      bingo_count += 1

  
  if all(bingo[i][i] == "x" for i in range(5)):
    print("BINGO")
    bingo_count += 1

  if all(bingo[i][4 - i] == "x" for i in range(5)):
    print("BINGO")
    bingo_count += 1  
  
  if bingo_count == 1:
    break