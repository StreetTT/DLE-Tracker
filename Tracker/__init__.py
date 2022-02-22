import sqlite3 as sql

def SQLComand(comannd, variables=None):
    conn = sql.connect("DLE.db")
    c = conn.cursor()
    if variables == None:
        c.execute(comannd)
    else:
        c.execute(comannd, variables)
    output = c.fetchall()
    conn.commit()
    conn.close()
    if c == None:
        return
    else:
        return output

def innit():
    SQLComand("""CREATE TABLE IF NOT EXISTS Accounts (
      UserID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
      FName TEXT NOT NULL,
      Username TEXT NOT NULL,
      Pin TEXT NOT NULL,
      Phrase TEXT NOT NULL,
      LastLogin TEXT)""")
    SQLComand("""CREATE TABLE IF NOT EXISTS WordleWords
           (WordleID INTEGER NOT NULL PRIMARY KEY,
          Word TEXT NOT NULL)""")
    count = SQLComand("""SELECT COUNT(*)
              FROM WordleWords""")[0][0]
    if count < 2309:
        f = open("Tracker/WordleMasterList.txt","r")
        list = f.read()
        f.close
        list = list.split(",")
        for i in range (len(list)):
        	SQLComand("""INSERT INTO WordleWords
                       Values (:id,:word)""",{"id":i, "word":list[i]})
    SQLComand("""CREATE TABLE IF NOT EXISTS WordleData (
              WordleID INTEGER NOT NULL,
              UserID INTEGER NOT NULL,
              Guessed BOOLEAN NOT NULL,
              Guesses INTEGER,
              Row1 TEXT NOT NULL,
              Row2 TEXT,
              Row3 TEXT,
              Row4 TEXT,
              Row5 TEXT,
              Row6 TEXT,
              PRIMARY KEY (WordleID, UserID),
              FOREIGN KEY (WordleID) REFERENCES WordleWords(WordleID),
              FOREIGN KEY (UserID) REFERENCES Accounts(UserID))""")