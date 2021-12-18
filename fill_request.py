import psycopg2
import random
import datetime


def random_datetime():
  start = datetime.datetime(2020, 12, 17, 0, 0, 0)
  end = datetime.datetime(2021, 12, 17, 0, 0, 0)
  between = (end - start).days
  random_days = datetime.timedelta(days=random.randrange(between))
  random_time_int = random.randrange(24 * 60 * 60)
  delta = datetime.timedelta(hours=random_time_int // (60 * 60),
                             minutes=random_time_int // 60 % 60,
                             seconds=random_time_int % 60)
  random_date = start + random_days + delta

  return random_date


def random_text_couch():
  possible = ['Привет! Ищу ученика', 'Ищу клиента, опыт игры 10 лет', 'Лучший тренер Вселенной ищет учеников',
              'Возьму в ученики, подробности  в пм', 'Всем привет! Первая тренировка бесплатно',
              'Топ-2 ладдера научит играть как профи', 'Ищу ученика, от 10 тренировок скидка']

  return random.choice(possible)


def random_text_client():
  possible = ['Привет! Ищу тренера', 'Хочу стать сильнее', 'Мне кажется, мой аккаунт проклят, помогите!',
              'Возьму тренера на 30 занятий', 'Ищу опытного тренера',
              'Хочу научиться играть и поднимать ранг', 'Хочу стать самым сильным игроком в классе',
              '2 года сижу на одном месте, помогите поднять ранг',
              'Хочу стать киберспортсменом, ищу тренера для регулярных занятий']

  return random.choice(possible)


def generate_requests(users):
  ans = []
  for _ in range(100000):
    user = random.choice(users)
    typee = user[1]
    if typee:
      text = random_text_couch()
    else:
      text = random_text_client()
    userid = user[0]
    date = random_datetime()
    time_of_action = random.choice([1, 2, 3])
    ans.append((userid, text, date, time_of_action, typee))

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
    'SELECT user_id, type FROM user_'
)
rows = cur.fetchall()
items = generate_requests(rows)
for item in items:
  cur.execute(
    "INSERT INTO request (userid, text, date, time_of_action, type) VALUES (%s, %s, %s, %s, %s)",
    item
  )

con.commit()
con.close()
