import sqlite3
from sqlite3 import Error


def openConnection(_dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Open database: ", _dbFile)

    conn = None
    try:
        conn = sqlite3.connect(_dbFile)
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

    return conn

def closeConnection(_conn, _dbFile):
    print("++++++++++++++++++++++++++++++++++")
    print("Close database: ", _dbFile)

    try:
        _conn.close()
        print("success")
    except Error as e:
        print(e)

    print("++++++++++++++++++++++++++++++++++")

def createTable(_conn):

    try:
        sql = ('''CREATE TABLE IF NOT EXISTS flashcard (
                    flashcard_id        INTEGER NOT NULL PRIMARY KEY,
                    front_id            INTEGER NOT NULL,
                    back_id             INTEGER NOT NULL,
                    correct_count       INTEGER NOT NULL,
                    incorrect_count     INTEGER NOT NULL);
                ''')

        sql1 = ('''CREATE TABLE IF NOT EXISTS deck (
            deck_id             INTEGER NOT NULL PRIMARY KEY,
            d_name              VARCHAR(55) NOT NULL,
            d_description       VARCHAR(75) NOT NULL,
            icon_path           VARCHAR(75));
        ''')

        sql2 = ('''CREATE TABLE IF NOT EXISTS user (
            user_id             INTEGER NOT NULL PRIMARY KEY,
            username            VARCHAR(25) NOT NULL,
            u_password          VARCHAR(25) NOT NULL);
        ''')

        sql3 = ('''CREATE TABLE IF NOT EXISTS u_session (
            user_id             INTEGER NOT NULL PRIMARY KEY,
            username            VARCHAR(25) NOT NULL,
            u_password          VARCHAR(25) NOT NULL);
        ''')

        sql4 = ('''CREATE TABLE IF NOT EXISTS spacing (
            spacing_id          INTEGER NOT NULL PRIMARY KEY,
            card_id             INTEGER NOT NULL,
            s_interval          datetime DEFAULT(getdate()),
            ef                  INTEGER NOT NULL);
        ''')

        sql5 = ('''CREATE TABLE IF NOT EXISTS categories (
            category_id         INTEGER NOT NULL PRIMARY KEY,
            c_name              VARCHAR(20) NOT NULL);
        ''')

        sql6 = ('''CREATE TABLE IF NOT EXISTS side (
            side_id             INTEGER NOT NULL PRIMARY KEY,
            s_header            VARCHAR(30) NOT NULL,
            s_body              VARCHAR(100) NOT NULL,
            img_path            VARCHAR(30));
        ''')

        _conn.execute(sql)
        _conn.execute(sql1)
        _conn.execute(sql2)
        _conn.execute(sql3)
        _conn.execute(sql4)
        _conn.execute(sql5)
        _conn.execute(sql6)

        _conn.commit()

    except Error as e:
        _conn.rollback()
        print(e)

def dropTable(_conn, var):

    if var == 'flashcard':
            try:
                sql = ('''drop table if exists flashcard''')
                _conn.execute(sql)

                _conn.commit()
                print("Table", var, "droppec")

            except Error as e:
                _conn.rollback()
                print(e)
    elif var == 'deck':
            try:
                sql = ('''drop table if exists deck''')
                _conn.execute(sql)

                _conn.commit()
                print("Table", var, "droppec")

            except Error as e:
                _conn.rollback()
                print(e)
    elif var == 'user':
            try:
                sql = ('''drop table if exists user''')
                _conn.execute(sql)

                _conn.commit()
                print("Table", var, "droppec")

            except Error as e:
                _conn.rollback()
                print(e)
    elif var == 'side':
            try:
                sql = ('''drop table if exists side''')
                _conn.execute(sql)

                _conn.commit()
                print("Table", var, "droppec")

            except Error as e:
                _conn.rollback()
                print(e)
    if var == 'spacing':
            try:
                sql = ('''drop table if exists spacing''')
                _conn.execute(sql)

                _conn.commit()
                print("Table", var, "droppec")

            except Error as e:
                _conn.rollback()
                print(e)
    if var == 'categories':
            try:
                sql = ('''drop table if exists categories''')
                _conn.execute(sql)

                _conn.commit()
                print("Table", var, "droppec")

            except Error as e:
                _conn.rollback()
                print(e)
    if var == 'u_session':
            try:
                sql = ('''drop table if exists u_session''')
                _conn.execute(sql)

                _conn.commit()
                print("Table", var, "droppec")

            except Error as e:
                _conn.rollback()
                print(e)

def createDeck(_conn, id, name, desc, img):
    
    try:

        print("Enter Info")

        deck_info = [id, name, desc, img]

        sql = ("INSERT INTO deck VALUES(?, ?, ?, ?)")
        _conn.execute(sql, deck_info)

        _conn.commit()

    except Error as e:
        _conn.rollback()
        print(e)

def main():
    database = r"flashcard.db"

    # create a database connection
    conn = openConnection(database)
    with conn:

        createTable(conn)

        #print("Tables Created Succesfully")
        #print("++++++++++++++++++++++++++++++++++")

        x = input("Drop Tables, y/n: ")
        if (x == "y"):
            dropTable(conn, input())
        
        #demo samples - create a deck
        y = input("Create Deck, y/n: ")
        if (y == "y"):
            id = int(input(""))
            name = input("Deck name: ")
            desc = input("Deck description: ")
            img = input("Image location path:")

            createDeck(conn, id, name, desc, img)

        z = input("Update deck, y/n: ")
        if (z == "z"):
            tablename = input("Set table")
            


    closeConnection(conn, database)


if __name__ == '__main__':
    main()
