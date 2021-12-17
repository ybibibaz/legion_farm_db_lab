import psycopg2


def game():
    games = ['dota', 'lol', 'starcraft']

    return games


con = psycopg2.connect(
  database="postgres",
  user="alexander",
  password="",
  host="127.0.0.1",
  port="5432"
)

cur = con.cursor()
games = game()
for play in games:
    cur.execute(
        "INSERT INTO game (name) VALUES (%s)", (play,)
    )
con.commit()
con.close()