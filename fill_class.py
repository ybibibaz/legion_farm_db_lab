import psycopg2
import random
import datetime


def random_duration():

    return random.choice([30, 45, 60, 90, 120])


def check_time(classes):
    ans = []
    for i in range(len(classes)):
        check_item = classes[i]
        flag = True
        for j in range(i + 1, len(classes)):
            compare_item = classes[j]
            if check_item[0] == compare_item[0]:
                if ((check_item[3] < compare_item[3] < check_item[3] + datetime.timedelta(minutes=check_item[4])) or
                    (compare_item[3] < check_item[3] < compare_item[3] + datetime.timedelta(minutes=compare_item[4]))):
                    flag = False
            elif check_item[1] == compare_item[1]:
                if ((check_item[3] < compare_item[3] < check_item[3] + datetime.timedelta(minutes=check_item[4])) or
                    (compare_item[3] < check_item[3] < compare_item[3] + datetime.timedelta(minutes=compare_item[4]))):
                    flag = False
            if not flag:
                break
        if flag:
            ans.append(check_item)

    return ans




def generate_class(requests, cur):
    ans = []
    for _ in range(2000):
        request = requests.pop(random.randrange(len(requests)))
        cur.execute(
            'SELECT game FROM user_ LEFT OUTER JOIN rank ON user_id = user_ WHERE user_id = %s', (request[0], )
        )
        games = cur.fetchall()
        gameid = random.choice(games)[0]
        user_type = request[1]
        if not user_type:
            cur.execute(
                'SELECT user_id FROM user_ LEFT OUTER JOIN rank ON user_id = user_ WHERE type = True AND game = %s', (gameid,)
            )
            trainers = cur.fetchall()
            trainer = random.choice(trainers)[0]
            request_date = request[2]
            random_time_int = random.randrange(7 * 24 * 60 * 60)
            delta = datetime.timedelta(days=random_time_int // (24 * 60 * 60),
                                    hours=random_time_int // (60 * 60) % 24,
                                    minutes=random_time_int // 60 % 60,
                                    seconds=random_time_int % 60)
            date = request_date + delta
            duration = random_duration()

            ans.append((request[0], trainer, gameid, date, duration))

        else:
            cur.execute(
                'SELECT user_id FROM user_ LEFT OUTER JOIN rank ON user_id = user_ WHERE type = False AND game = %s',
                (gameid,)
            )
            clients = cur.fetchall()
            client = random.choice(clients)[0]
            request_date = request[2]
            random_time_int = random.randrange(7 * 24 * 60 * 60)
            delta = datetime.timedelta(days=random_time_int // (24 * 60 * 60),
                                       hours=random_time_int // (60 * 60) % 24,
                                       minutes=random_time_int // 60 % 60,
                                       seconds=random_time_int % 60)
            date = request_date + delta
            duration = random_duration()

            ans.append((client, request[0], gameid, date, duration))

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
    'SELECT userid, type, date FROM request'
)
requests = cur.fetchall()
classes = generate_class(requests, cur)
classes = check_time(classes)
for item in classes:
  cur.execute(
    "INSERT INTO class (client, trainer, game, date, duration) VALUES (%s, %s, %s, %s, %s)",
    item
  )

con.commit()
con.close()
