i=1

print("あ",end=" ")
print("い")

i = 1
while i <= 9:
  print("2 ×", i, "=", 2 * i, end=" ")
  i += 1

i = 1
while i <= 9:
  print(f"2 × {i} = {2 * i}", end=" ")
  i += 1

i = 1
j = 1
while i <= 9:
  i += 1
  print(f"{j} × {i} = {j * i}", end=" ")
  
  while i > 9:
    j += 1
    continue

i = 1
while i <= 9:
  j = 1
  while j <= 9:
    print(f"{i * j}",end=" ")
    j += 1
  print() 
    
  i += 1
  
a = set()
for i in range(1,10):
  for j in range(1,10):
    a.add(i * j)
print(len(a))

s = {i*l for i in range(1,10)for l in range(1,10)}
print(len(s))