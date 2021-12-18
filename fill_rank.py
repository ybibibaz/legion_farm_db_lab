import psycopg2
import random


def choose(game, type):
  if game == 317 and type:
    return random.randint(6000, 10000)
  if game == 317 and not type:
    return random.randint(1, 5000)
  if game == 318 and type:
    return random.choice(['master', 'grandmaster'])
  if game == 318 and not type:
    return random.choice(['bronze', 'silver', 'gold', 'platinum', 'diamond'])
  if game == 319 and type:
    return random.choice(['master', 'grandmaster', 'challenger'])
  if game == 319 and not type:
    return random.choice(['iron', 'bronze', 'silver', 'gold', 'platinum', 'diamond'])
  if type:
    return random.choice([random.choice(['master', 'grandmaster']), random.randint(6000, 10000)])
  return random.choice([random.choice(['bronze', 'silver', 'gold', 'platinum', 'diamond']), random.randint(1, 5000)])

def choose_rank(games, users):
  ans = []
  for user in users:
    count = random.randint(1, 100)
    if count <= 35:
      count = 1
    elif count <= 70:
      count = 2
    if count <= 85:
      count = 3
    else:
      count = 4
    gamepool = [games[i][0] for i in range(len(games))]
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