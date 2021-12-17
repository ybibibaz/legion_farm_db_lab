import psycopg2
import random


def choose(game, type):
  if game == 151 and type:
    return random.randint(6000, 10000)
  if game == 151 and not type:
    return random.randint(1, 5000)
  if game == 152 and type:
    return random.choice(['master', 'grandmaster'])
  if game == 152 and not type:
    return random.choice(['bronze', 'silver', 'gold', 'platinum', 'diamond'])
  if game == 153 and type:
    return random.choice(['master', 'grandmaster', 'challenger'])
  if game == 153 and not type:
    return random.choice(['iron', 'bronze', 'silver', 'gold', 'platinum', 'diamond'])

def choose_rank(games, users):
  ans = []
  for user in users:
    count = random.randint(1, 100)
    if count <= 50:
      count = 1
    elif count <= 85:
      count = 2
    else:
      count = 3
    gamepool = [games[i][0] for i in range(3)]
    for _ in range(count):
      game = gamepool.pop(random.randint(0, len(gamepool) - 1))
      ans.append((user[0], game, choose(game, user[1])))

  return ans


con = psycopg2.connect(
  database="postgres",
  user="alexander",
  password="",
  host="127.0.0.1",
  port="5432"
)

cur = con.cursor()
cur.execute(
    'SELECT game_id, name FROM game'
)
rows = cur.fetchall()
cur.execute(
    'SELECT user_id, type FROM user_'
)
rows1 = cur.fetchall()
items = choose_rank(rows, rows1)
for item in items:
  cur.execute(
    "INSERT INTO rank (user_, game, rating) VALUES (%s, %s, %s)", item
  )

con.commit()
con.close()