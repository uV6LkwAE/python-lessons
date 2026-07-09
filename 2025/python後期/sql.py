import pymysql

print("世界の皆さん、こんにちは")

connection = pymysql.connect(
host = "localhost",
database = "paiza",
user = "root",
password = "rootuser",
charset ="utf8",
cursorclass = pymysql.cursors.DictCursor
)

sql = "SELECT * FROM players"
cursor = connection.cursor()
cursor.execute(sql)
players = cursor.fetchall()

cursor.close()
connection.close()

for player in players:
  print(player["id"],player["name"],player["level"],player["job_id"])