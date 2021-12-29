import replit
def db_clear():
  print("Test")
  keys = replit.db.keys()
  print(keys)
  for i in keys:
    del replit.db[i]
def unbackslash(data):
  betterData = []
  for item in data:
    betterData.append(item.strip())
  return betterData