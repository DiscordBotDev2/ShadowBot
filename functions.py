import replit
def db_clear():
  print("Test")
  keys = replit.db.keys()
  print(keys)
  for i in keys:
    del replit.db[i]
db_clear()