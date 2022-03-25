import time
import random
import socket
import requests
import concurrent.futures

""" An attempt to prevent spam detection """
header = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36"

""" Load the `accounts.txt` file """
try:
  accounts = []
  with open("accounts.txt", "r") as file:
    for x in file.readlines():
      password = x.strip()
      accounts.append(password)
except Exception as error: accounts = []

incorrect, maximum = [], len(accounts)

def token(target):
    """ Separate the login data provided by a colon then log in to Chatango to retrieve the account token """
    accounts.remove(target)
    query = target.split(": ", 1)
    post = requests.post("https://chatango.com/login", data={"user_id": query[0], "password": query[1], "storecookie": "on", "checkerrors": "yes"}, headers={"User-Agent": header}).cookies.get("auth.chatango.com", False)
    if post: return [query[0], post]
    else:
      incorrect.append(query[0])
      return [query[0], False]

def connect(target):
    """ Log in to Chatango private messages with the token and then immediately log out """
    query = token(target)
    if query[1]:
      frame = bytes(f"tlogin:{query[1]}:2:{random.randint(1, 10 ** 16)}\x00", "utf-8")
      log = socket.socket()
      log.connect(("c1.chatango.com", 5222))
      log.send(frame)
      log.close()
      return f'[LOGIN] {query[0]}'
    else: return f'[INCORRECT] {query[0]}'

def process():
    """ Do the `connect(target)` function 100 times simultaneously, may or may not be CPU intensive """
    data = 100
    if len(accounts) < data: data = len(accounts)
    with concurrent.futures.ThreadPoolExecutor(max_workers=data) as action:
      for x in action.map(connect, accounts[0:data]): print(x)

print("Launching...")
run = time.time()

""" While the amount of accounts in `accounts.txt` is above 0, do the `process()` function """
while len(accounts) > 0:
  process()
  print(f'[STATUS] ({maximum - len(accounts)}/{maximum}) completed in {int(time.time() - run)} seconds')

input(f'[FINISH] {"Failed to login to " + ", ".join(incorrect) if incorrect else ""}')
