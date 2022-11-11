from flask import Flask, jsonify, request
from flask_cors import CORS

import sqlite3
from sqlite3 import Error

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def connection():
    conn = sqlite3.connect('card.db')
    return conn

def createTable():

    _conn = connection()

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

def insert_deck(deck):
    new_decks = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO deck(deck_id, d_name, d_description, icon_path) VALUES(?,?,?,?)", (deck['deck_id'], deck['d_name'], deck['d_description'], deck['icon_path']))
        conn.commit()

        new_decks = get_decks(cur.lastrowid)

    except Error as e:
        conn().rollback()
        print(e)
    
    return insert_deck

def get_decks():
    decks = []

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM deck")
        rows = cur.fetchall()

        for i in rows:
            deck = {}
            deck['deck_id'] = i['deck_id']
            deck['d_name'] = i['d_name']
            deck['d_description'] = i['d_description']
            deck['icon_path'] = i['icon_path']
            decks.append(deck)

    except Error as e:
        decks = []
    
    return decks

def get_decks_by_id(deck_id):
    deck = {}

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM deck WHERE deck_id = ?", (deck_id,))
        row = cur.fetchone()

        deck['deck_id'] = row['deck_id']
        deck['d_name'] = row['d_name']
        deck['d_description'] = row['d_description']
        deck['icon_path'] = row['icon_path']

    except Error as e:
        deck = {}
    
    return deck

def update_deck(deck):
    updated_deck = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("UPDATE deck SET d_name = ?, d_description = ?, icon_path = ? WHERE deck_id = ?", (deck['d_name'], deck['d_description'], deck['icon_path'],))

        conn.commit()

        #updated user
        updated_deck = get_decks_by_id(deck['deck_id'])

    except Error as e:
        conn.rollback()
        updated_deck = {}
        print(e)
    
    finally:
        conn.close

def delete_deck(deck_id):
    message = {}

    try:
        conn = connection()
        conn.execute("DELETE from deck WHERE deck_id = ?", (deck_id,))

        conn.commit()
        message['status'] = "Deck deleted succesfully"

    except:
        conn.rollback()
        message['status'] = "Cannot delete deck"
    finally:
        conn.close()

    return message

#------------------------------------------------------------------------#

def insert_user(user):
    new_users = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO user(user_id, username, u_password) VALUES(?,?,?)", (user['user_id'], user['username'], user['password']))
        conn.commit()

        new_users = get_users(cur.lastrowid)

    except Error as e:
        conn().rollback()
        print(e)
    
    return insert_user

def get_users():
    users = []

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user")
        rows = cur.fetchall()

        for i in rows:
            user = {}
            user['user_id'] = i['user_id']
            user['username'] = i['username']
            user['password'] = i['password']
            users.append(user)

    except Error as e:
        users = []
    
    return users

def get_users_by_id(user_id):
    user = {}

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        user['user_id'] = row['user_id']
        user['username'] = row['username']
        user['password'] = row['password']

    except Error as e:
        user = {}
    
    return user

def update_user(user):
    updated_user = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("UPDATE user SET username = ?, password = ? WHERE user_id = ?", (user['username'], user['password'],))

        conn.commit()

        #updated user
        updated_user = get_users_by_id(user['user_id'])

    except Error as e:
        conn.rollback()
        updated_user = {}
        print(e)
    
    finally:
        conn.close

def delete_user(user_id):
    message = {}

    try:
        conn = connection()
        conn.execute("DELETE from user WHERE user_id = ?", (user_id,))

        conn.commit()
        message['status'] = "Deck deleted succesfully"

    except:
        conn.rollback()
        message['status'] = "Cannot delete deck"
    finally:
        conn.close()

    return message

#------------------------------------------------------------------------#

def insert_side(side):
    new_sides = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO side(side_id, s_header, s_body, img_path) VALUES(?,?,?,?)", (side['side_id'], side['s_header'], side['s_body'], side['img_path']))
        conn.commit()

        new_sides = get_sides(cur.lastrowid)

    except Error as e:
        conn().rollback()
        print(e)
    
    return insert_side

def get_sides():
    sides = []

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM side")
        rows = cur.fetchall()

        for i in rows:
            side = {}
            side['side_id'] = i['side_id']
            side['s_header'] = i['s_header']
            side['s_body'] = i['s_body']
            side['img_path'] = i['img_path']
            sides.append(side)

    except Error as e:
        sides = []
    
    return sides

def get_sides_by_id(side_id):
    side = {}

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM side WHERE side_id = ?", (side_id,))
        row = cur.fetchone()

        side['side_id'] = row['side_id']
        side['s_header'] = row['s_header']
        side['s_body'] = row['s_body']
        side['img_path'] = row['img_path']

    except Error as e:
        side = {}
    
    return side

def update_side(side):
    updated_side = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("UPDATE side SET s_header = ?, s_body = ?, img_path = ? WHERE side_id = ?", (side['s_header'], side['s_body'], side['img_path'],))

        conn.commit()

        #updated user
        updated_side = get_sides_by_id(side['side_id'])

    except Error as e:
        conn.rollback()
        updated_side = {}
        print(e)
    
    finally:
        conn.close

def delete_side(side_id):
    message = {}

    try:
        conn = connection()
        conn.execute("DELETE from side WHERE side_id = ?", (side_id,))

        conn.commit()
        message['status'] = "Deck deleted succesfully"

    except:
        conn.rollback()
        message['status'] = "Cannot delete deck"
    finally:
        conn.close()

    return message



#-------------Complex-------------#
def categories_to_deck(categories_list, deck_id):
	message = {}

	try:
		conn = connection()
		# find cards from each category
		cards = []
		for category in categories_list:
			conn.execute("""
				SELECT card_category.card_id
				FROM categories
					INNER JOIN card_category ON categories.category_id = card_category.category_id
				WHERE categories.c_name LIKE "%?%"
			""", category)
			cards += conn.fetchall()
		# insert into the deck
		for card in cards:
			conn.execute("INSERT INTO card_in_deck VALUES (?)", (deck_id, card["card_id"]))

	except:
		conn.rollback()
		message['status'] = "Making deck from provided categories failed"

	finally:
		conn.close()

	return message





#-------------DECKS-------------#
@app.route('/api/decks', methods=['GET'])
def api_get_decks():
    return jsonify(get_decks())

@app.route('/api/decks/<deck_id>', methods=['GET'])
def api_get_deck(deck_id):
    return jsonify(get_decks_by_id(deck_id))

@app.route('/api/decks/add', methods=['GET'])
def api_add_deck():
    deck = request.get_json()
    return jsonify(insert_deck(deck))

@app.route('/api/decks/update', methods=['PUT'])
def api_update_deck():
    deck = request.get_json()
    return jsonify(update_deck(deck))

@app.route('/api/decks/delete/<deck_id>', methods=['DELETE'])
def api_delete_deck(deck_id):
    return jsonify(delete_deck(deck_id))

#-----------USERS----------#
@app.route('/api/users', methods=['GET'])
def api_get_users():
    return jsonify(get_users())

@app.route('/api/users/add', methods=['GET'])
def api_add_user():
    user = request.get_json()
    return jsonify(insert_user(user))

@app.route('/api/users/<user_id>', methods=['GET'])
def api_get_user(user_id):
    return jsonify(get_users_by_id(user_id))

@app.route('/api/users/update', methods=['PUT'])
def api_update_user():
    user = request.get_json()
    return jsonify(update_user(user))

@app.route('/api/users/delete/<user_id>', methods=['DELETE'])
def api_delete_user(user_id):
    return jsonify(delete_user(user_id))

#-----------SIDES------------#
@app.route('/api/sides', methods=['GET'])
def api_get_sides():
    return jsonify(get_sides())

@app.route('/api/sides/<side_id>', methods=['GET'])
def api_get_deck(side_id):
    return jsonify(get_sides_by_id(side_id))

@app.route('/api/sides/add', methods=['GET'])
def api_add_deck():
    side = request.get_json()
    return jsonify(insert_side(side))

@app.route('/api/sides/update', methods=['PUT'])
def api_update_side():
    side = request.get_json()
    return jsonify(update_side(side))

@app.route('/api/sides/delete/<side_id>', methods=['DELETE'])
def api_delete_side(side_id):
    return jsonify(delete_side(side_id))

if __name__ == '__main__':
    app.run(debug=True)