import sqlite3

#connect to database
conn = sqlite3.connect('db.sqlite3')

# creating a cursor to intrect with database
cursor = conn.cursor()

# Creating a Table task 
cursor.execute("""
CREATE TABLE tasks(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               title VARCHAR(255) NOT NULL,
               description TEXT NOT NULL,
               due_date DATE NOT NULL,
               status VARCHAR(20) DEFAULT 'Pending'
               )

""")


# COmmiting my commands to db
conn.commit()

#closing the connection
conn.close()