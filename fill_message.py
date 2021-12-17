import psycopg2
import random
import datetime


def gen_text(type):
    if type:

        return random.choice([['Привет, готов учиться', 'Привет! Давай через полчаса созвонимся #4313 в дискорде', 'Ок'],
                              ['Привет, хочу стать учеником, добавь #1123 в дискорде', 'хорошо'],
                              ['Привет, давай обсудим условия обучения в дискорде', 'https://discord.gg/8tbfBex8']])
    else:

        return random.choice(
            [['Привет, могу стать твоим тренером', 'Привет! Как можно с тобой пообщаться?', '#5643 в дискорде'],
             ['Привет, еще ищешь тренера? ', 'Да', 'Могу предложить свою кандидатуру, можно сейчас пообщаться',
              'Дискорд?', 'Да, добавь #1789', 'Ок'],
             ['Привет, давай обсудим условия обучения в дискорде', 'Привет, заходи https://discord.gg/88jjhhf3']])


def gen_message(rows):
    mes = []
    for items in rows:
        receiver = items[0]
        if items[1] != receiver:
            sender = items[1]
        else:
            sender = items[2]
        delta = items[5]
        days = random.choice(range(delta))
        delta = datetime.timedelta(days=days, hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
        date = items[3] + delta
        text = gen_text(items[6])
        for messages in text:
            mes.append((sender, receiver, messages, date))
            date += datetime.timedelta(seconds=random.randint(0, 59))
            sender, receiver = receiver, sender

    return mes


con = psycopg2.connect(
  database="postgres",
  user="alexander",
  password="",
  host="127.0.0.1",
  port="5432"
)

cur = con.cursor()
cur.execute(
        "SELECT userid, client, trainer, request.date, class.date, time_of_action, type FROM class LEFT OUTER JOIN request ON userid = client OR userid = trainer",
    )
rows = cur.fetchall()
new_rows = []
for i in range(len(rows)):
    temp_datetime = datetime.datetime(rows[i][4].year, rows[i][4].month, rows[i][4].day)
    diff = (temp_datetime - rows[i][3]).days
    if 0 <= diff <= 7:
        new_rows.append(rows[i])
del rows
rows = []
if new_rows[0][1] != new_rows[1][1] or new_rows[0][2] != new_rows[1][2]:
    rows.append(new_rows[0])
for i in range(len(new_rows) - 1):
    if new_rows[i][1] != new_rows[i + 1][1] or new_rows[i][2] != new_rows[i + 1][2]:
        rows.append(new_rows[i + 1])
messages = gen_message(rows)
for message in messages:
    cur.execute(
        "INSERT INTO message (sender, receiver, text, date) VALUES (%s, %s, %s, %s)",
        message
    )
con.commit()
con.close()
