import random

n = int(input("何桁でプレイしますか→"))
 
li = []
i = 0
while i < n:
  a= random.randint(0,9)
  if a not in li:
    li.append(a)
    i += 1
print(li)

while True:
  p = list(map(int,input(f"{n}個の数字を半角スペースを入れて入力して下さい→").split()))

  hit = 0
  blow = 0
  hint = []
  for j in range(n):
    if p[j] == li[j]:
      hint.append("HIT")
    elif p[j] < li[j]:
      hint.append("HIGH")
    elif p[j] > li[j]:
      hint.append("LOW")
      

    if p[j] == li[j]:
      hit += 1
    elif p[j] in li :
      blow += 1

  print(f"{hit} HIT,{blow} BLOW")

  if hit == n:
    break

  hi = input("ヒントは要りますか？(yes or no)→")

  if hi == "yes":
    print(hint)


    # 入力り受け取り、じゃんけん、じゃんじ、引数、
    # 勝敗を戻り値
    