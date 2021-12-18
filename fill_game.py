import psycopg2


def random_name_generator1():
    first = ['battle', 'conflict', 'world', 'clash', 'war', 'empire', 'alliance', 'shine', 'time', 'dawn']
    second = ['magic', 'ancients', 'orcs', 'crusaders', 'wizards', 'archers', 'interests', 'cats', 'r\'lyech',
              'azatot', 'nyarlathotep', 'insmut', 'shub-niggurath', 'yog-sothoth', 'yogg-saron', 'y\'saarj']
    ans = []
    for f in first:
        for s in second:
            ans.append(f + ' of ' + s)

    return ans

def game():
    games = ['dota', 'lol', 'starcraft']
    games.extend(random_name_generator1())

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
