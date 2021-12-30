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
def manipulate(file, mode, data):
  try:
    with open(file, mode) as f:
      if mode == "w":
        f.write(data)
        f.close()
      if mode == "r":
        read = f.readlines()
        f.close
        return read
  except:
    raise 

def transform(ls, rules):
  pass

