import sqlite3 

conn = sqlite3.connect("jarvis_memory.db")
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS memory (
    id INTEGER PRIMARY KEY,
    topic TEXT, 
    content TEXT
)''')

conn.commit()
print("JARVIS memory database created successfully.")

cursor.execute("INSERT INTO memory (topic, content) VALUES (?, ?)",
               ("user_name", "Sadaqat"))
conn.commit()   
print("Memory saved. ")

cursor.execute("SELECT * FROM memory")
rows = cursor.fetchall()
for row in rows:
    print(row)  
