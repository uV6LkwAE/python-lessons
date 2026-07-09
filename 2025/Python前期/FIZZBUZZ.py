for i in range(1,101):
  if i % 3 == 0 and i % 5 == 0:
    i = "FIZZBUZZ"
  
  elif i % 3 == 0:
    i = "FIZZ"

  elif i % 5 == 0:
    i ="BUZZ"

  print(i)
