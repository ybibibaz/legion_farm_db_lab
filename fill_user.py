import psycopg2
import random
from string import ascii_lowercase


def login_list():
  login = []
  for i in range(20000):
    login.append('super_cool_login_{}'.format(i + 1))

  return login


def ban_list():
  ban = []
  for i in range(20000):
    ban.append(bool(random.randint(1, 10) // 9))

  return ban


def password_list():
  password = []
  for i in range(20000):
    password.append("".join(random.choice(ascii_lowercase) for i in range(20)))

  return password


def nick_list():
  nick = []
  for i in range(20000):
    nick.append("super_cool_nick_" + str(i + 1))

  return nick


def type_list():
  type = []
  for i in range(20000):
    type.append(bool(random.randint(1, 10) // 9))

  return type


def email_list():
  email = []
  domains = ["mail.ru", "gmail.com", "yandex.ru", "inbox.ru"]
  for i in range(20000):
    email.append("super_cool_email_{}@".format(i + 1) + random.choice(domains))

  return email


con = psycopg2.connect(
  database="postgres",
  user="alexander",
  password="",
  host="127.0.0.1",
  port="5432"
)

cur = con.cursor()
login = login_list()
ban = ban_list()
password = password_list()
nick = nick_list()
typee = type_list()
email = email_list()
for i in range(20000):
  cur.execute(
    "INSERT INTO user_ (login, ban, password, nick, type, email) VALUES (%s, %s, %s, %s, %s, %s)",
    (login[i], ban[i], password[i], nick[i], typee[i], email[i])
  )
con.commit()
con.close()
