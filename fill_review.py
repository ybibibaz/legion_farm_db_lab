import psycopg2
import random
import datetime


def generate_review_client():
    possibilities = [[1, 'Тренер не умеет играть'], [2, 'Плохо объясняет'],
                     [2, 'Не пытается ничему научить и издевается'], [3, 'Опоздал на занятие'],
                     [3, 'Хороший игрок, но плохой тренер'], [3, 'У тренера плохой микрофон'],
                     [4, 'Хорошо объясняет'], [4, 'Хороший, но не очень опытный тренер'],
                     [5, 'Стал играть лучше уже после первого занятия'], [5, 'Отличный тренер']]

    return random.choice(possibilities)


def generate_review_trainer():
    possibilities = [[1, 'Неадекватный'], [2, 'Считает себя лучшим, не понятно, зачем берет занятия'],
                     [3, 'Опоздал'], [4, 'Не всегда следует советам'], [4, 'Вежливый пользователь'],
                     [5, 'Старается, не опаздывает, вежливый']]

    return random.choice(possibilities)


def generate_timestamp(date):

    return datetime.datetime(date.year, date.month, date.day,
                             random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))


def client_review(clients):
    ans = []
    for client in clients:
        flag = random.choice([True, False])
        if flag:
            review = generate_review_client()
            date = generate_timestamp(client[2])
            ans.append((client[0], client[1], review[1], review[0], date))

    return ans


def trainer_review(trainers):
    ans = []
    for trainer in trainers:
        flag = random.choice([True, False])
        if flag:
            review = generate_review_trainer()
            date = generate_timestamp(trainer[2])
            ans.append((trainer[0], trainer[1], review[1], review[0], date))

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
    'SELECT class_id, client, date FROM class'
)
clients = cur.fetchall()
cur.execute(
    'SELECT class_id, trainer, date FROM class'
)
trainers = cur.fetchall()
client_reviews = client_review(clients)
trainer_reviews = trainer_review(trainers)
reviews = client_reviews.copy()
reviews.extend(trainer_reviews)
for item in reviews:
  cur.execute(
    "INSERT INTO review (class, user_, text, mark, date) VALUES (%s, %s, %s, %s, %s)",
    item
  )

con.commit()
con.close()
