import requests
import sqlite3

url = "https://www.freetogame.com/api/games"
response = requests.get(url)
games = response.json()

conn = sqlite3.connect("games.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY,
        title TEXT,
        genre TEXT,
        developer TEXT,
        release_date TEXT
    )
''')

for game in games:
    cursor.execute('''
        INSERT OR IGNORE INTO games (id, title, genre, developer, release_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (
        game['id'],
        game['title'],
        game['genre'],
        game['developer'],
        game['release_date']
    ))

conn.commit()


print("1.จำนวนเกมในแต่ละแนว:")
cursor.execute('''
    SELECT genre, COUNT(*) as count
    FROM games
    GROUP BY genre
    ORDER BY count DESC
''')
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} เกม")

print("\n2.5 เกมที่เปิดตัวล่าสุด:")
cursor.execute('''
    SELECT title, release_date
    FROM games
    WHERE release_date IS NOT NULL
    ORDER BY release_date DESC
    LIMIT 5
''')
for row in cursor.fetchall():
    print(f"{row[0]} - เปิดตัวเมื่อ {row[1]}")

print("\n3.จำนวนเกมที่เปิดตัวในแต่ละปี:")
cursor.execute('''
    SELECT SUBSTR(release_date, 1, 4) AS year, COUNT(*) as count
    FROM games
    WHERE release_date IS NOT NULL
    GROUP BY year
    ORDER BY year DESC
''')
for row in cursor.fetchall():
    print(f"ปี {row[0]}: {row[1]} เกม")

print("\n4.5 อันดับผู้พัฒนาที่มีเกมมากที่สุด:")
cursor.execute('''
    SELECT developer, COUNT(*) as count
    FROM games
    GROUP BY developer
    ORDER BY count DESC
    LIMIT 5
''')
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]} เกม")

print("\n5.แนวเกมยอดนิยมที่สุด:")
cursor.execute('''
    SELECT genre, COUNT(*) as count
    FROM games
    GROUP BY genre
    ORDER BY count DESC
    LIMIT 1
''')
row = cursor.fetchone()
print(f"{row[0]}: {row[1]} เกม")

print("\n6.เกมที่เก่าที่สุด:")
cursor.execute('''
    SELECT title, release_date
    FROM games
    WHERE release_date IS NOT NULL
    ORDER BY release_date ASC
    LIMIT 1
''')
row = cursor.fetchone()
print(f"{row[0]} - เปิดตัวเมื่อ {row[1]}")

conn.close()
