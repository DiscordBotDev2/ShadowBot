from flask import Flask
from threading import Thread
with open("id.txt", "r") as file:
  Id = file.readlines()
  print(int(Id[0]))
  file.close()
app = Flask('')

@app.route('/')
def home():
    return Id[0]

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
