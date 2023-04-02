import time
import asyncio
import websockets

# stalemate.py v3.1 by Vissle Drissle

""" Load the `accounts.txt` file """
try:
  accounts = []
  with open("accounts.txt", "r", encoding="latin-1") as file:
    for x in file.readlines():
      password = x.strip()
      accounts.append(password)
except Exception as error: accounts = []

detail = []

""" Log in to Chatango with the message catcher server and then immediately log out """
async def login(username, password):
  try:
    async with websockets.connect("wss://i0.chatango.com:8081/", origin="https://st.chatango.com", ping_interval=None, ping_timeout=None) as client:
      connected = True
      await client.send("version:4:1\r\n\x00")
      await client.send(f"login:{username}:{password}\r\n\x00")
      while connected:
        try:
          frame = await client.recv()
          clean = frame.replace("\r\n\x00", "")
          if "msgcount" in clean:
            unread = clean.split(":")[1]
            await client.close()
            return [True, username, unread]
          elif "DENIED" in clean:
            await client.close()
            return [False, username, False]
        except Exception as error:
          connected = False
          await client.close()
          return [False, username, False]
  except Exception as error:
    print(error)
    return [False, username, False]

""" Show results of logins """
async def launch():
  result = await asyncio.gather(*detail)
  fail = []
  total = []
  for x in result:
    if x[0]: total.append(f"{x[1]}: {x[2]} unread messages")
    else:
      fail.append(x[1])
      total.append(f"{x[1]}: [Incorrect password]")
  parse = "\n".join(total)
  print(f"Finished in {int(time.time() - run)} seconds.")
  if fail:
    with open("stalemate.txt", "w+") as file: file.write(parse)
    content = input(f'Logged ({len(accounts) - len(fail)}/{len(accounts)}) accounts, check "stalemate.txt" for more details.\nType "clean" to only show accounts that failed to log in. (Close "stalemate.txt" if open before typing)\n')
    if content == "clean":
      failed = "\n".join(fail)
      with open("stalemate.txt", "w+") as file: file.write(failed)
    else: input()
  else:
    with open("stalemate.txt", "w+") as file: file.write(parse)
    input('All accounts were logged, check "stalemate.txt" to see the amount of unread messages for each account.')

""" Login data separated by a colon (username: password) """
if len(accounts) > 0:
  fail = []
  for x in accounts:
    data = x.split(": ")
    if len(data) > 1:
      username = data[0]
      password = data[1]
      function = login(username, password)
      detail.append(function)
    else:
      fail.append(x)
      break

  if fail:
    input(f'Incorrect format was used, please check the line below in accounts.txt\n{fail}\nThe format is "username: password"')
  else:
    print("Launching...")
    run = time.time()
    script = launch()
    asyncio.run(script)
else: input('"accounts.txt" is empty.')
