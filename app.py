import os

from flask_cors import CORS

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

import sqlite3
from sqlite3 import Error

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
maindir = os.path.abspath(os.path.dirname(__file__))

# Database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(maindir, "card.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "thisissecret"

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    u_password = db.Column(db.String(32), nullable=False)

    def get_id(self):
        return self.user_id


class RegisterForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "u_password", validators=[InputRequired(), Length(min=4, max=15)]
    )

    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username already exists")


class LoginForm(FlaskForm):
    username = StringField(
        "username", validators=[InputRequired(), Length(min=4, max=15)]
    )
    password = PasswordField(
        "u_password", validators=[InputRequired(), Length(min=4, max=15)]
    )

    submit = SubmitField("Sign In")


@app.route("/")
def home():
    return redirect(url_for("login"))


# A function to store the logged in user
def logged_in_user_id(id=None):
    # If an id is passed to it
    if id:
        print("Set ID")
        # Store that
        logged_in_user_id.id = id
    else:
        try:
            # Otherwise, if there's a stored id, return that
            temp = logged_in_user_id.id
            print("Returning set ID")
            return temp
        except:
            print("Returning default ID")
            # Otherwise return 0, which doesn't map to any user since id's start at 1
            #TODO change it back to 0
            # return 10
            return 0


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.u_password, form.password.data):
                login_user(user)
                logged_in_user_id(user.user_id)
                return redirect(url_for("profile"))

    return render_template("login.html", form=form)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        new_user = User(username=form.username.data, u_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("signup.html", form=form)


@app.route("/profile", methods=["GET", "POST"])
def profile():
    return render_template("profile.html")


@app.route("/deck/<deck_id>", methods=["GET"])
def deck_display(deck_id):
    decks = get_decks(logged_in_user_id())
    print([d["deck_id"] for d in decks])
    if int(deck_id) in [d["deck_id"] for d in decks]:
        return render_template("deck.html") 
    return '<a href="http://127.0.0.1:5000">404 You don\'t have access to that deck</a>'
    # return render_template("deck.html") 

@app.route("/new_deck", methods=["GET", "POST"])
def new_deck():
    print(request.method)
    if request.method == "GET":
        return render_template("new_deck.html")
    else:
        deck = {}
        deck["d_name"] = request.form["deck-name"]
        deck["d_description"] = request.form["deck-description"]
        print(deck)
        deck_id = insert_deck(deck)
        return redirect(url_for("deck_display", deck_id=deck_id))

        
@app.route("/new_card/<deck_id>", methods=["GET", "POST"])
def new_card(deck_id):
    print(request.method)
    if request.method == "GET":
        return render_template("new_card.html", deck_id=deck_id)
    else:
        print("POSTING NEW CARD")
        # side["s_header"],
        #         side["s_body"],
        side1 = {}
        side1["s_header"] = request.form["card-back-title"]
        side1["s_body"] = request.form["card-back-text"]
        side2 = {}
        side2["s_header"] = request.form["card-front-title"]
        side2["s_body"] = request.form["card-front-text"]
        # print(card)
        card_id = insert_card(side1, side2, deck_id)
        return redirect(url_for("deck_display", deck_id=deck_id))


def connection():
    conn = sqlite3.connect(r"card.db")
    return conn


def createTable():

    _conn = connection()

    try:
        sql = """CREATE TABLE IF NOT EXISTS flashcard (
                    flashcard_id        INTEGER NOT NULL PRIMARY KEY,
                    front_id            INTEGER NOT NULL,
                    back_id             INTEGER NOT NULL,
                    correct_count       INTEGER NOT NULL,
                    incorrect_count     INTEGER NOT NULL);
                """

        sql1 = """CREATE TABLE IF NOT EXISTS deck (
            deck_id             INTEGER NOT NULL PRIMARY KEY,
            d_name              VARCHAR(55) NOT NULL,
            d_description       VARCHAR(75) NOT NULL,
        """

        sql2 = """CREATE TABLE IF NOT EXISTS user (
            user_id             INTEGER NOT NULL PRIMARY KEY,
            username            VARCHAR(25) NOT NULL,
            u_password          VARCHAR(25) NOT NULL);
        """

        sql3 = """CREATE TABLE IF NOT EXISTS u_session (
            user_id             INTEGER NOT NULL PRIMARY KEY,
            username            VARCHAR(25) NOT NULL,
            u_password          VARCHAR(25) NOT NULL);
        """

        sql4 = """CREATE TABLE IF NOT EXISTS spacing (
            spacing_id          INTEGER NOT NULL PRIMARY KEY,
            card_id             INTEGER NOT NULL,
            s_interval          datetime DEFAULT(getdate()),
            ef                  INTEGER NOT NULL);
        """

        sql5 = """CREATE TABLE IF NOT EXISTS categories (
            category_id         INTEGER NOT NULL PRIMARY KEY,
            c_name              VARCHAR(20) NOT NULL);
        """

        sql6 = """CREATE TABLE IF NOT EXISTS side (
            side_id             INTEGER NOT NULL PRIMARY KEY,
            s_header            VARCHAR(30) NOT NULL,
            s_body              VARCHAR(100) NOT NULL,
        """

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
        print("createTable", e)


def insert_deck(deck):
    try:
        conn = connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT deck_id FROM deck ORDER BY deck_id DESC LIMIT 1"
        )
        deck_id = int(cur.fetchone()[0]) + 1
        cur.execute(
            "INSERT INTO deck(deck_id, d_name, d_description) VALUES(?,?,?)",
            (deck_id, deck["d_name"], deck["d_description"],),
        )
        cur.execute("INSERT INTO user_decks(user_id, deck_id) VALUES(?, ?)", (logged_in_user_id(), deck_id,))
        conn.commit()

        return deck_id
    except Error as e:
        conn().rollback()
        print("insert_deck", e)

    # return insert_deck


def get_decks(user_id):
    decks = []

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        # print(type(user_id))
        # print(user_id)
        cur.execute(
            """SELECT deck.deck_id, d_name, d_description
                        FROM user_decks
                        INNER JOIN deck ON user_decks.deck_id = deck.deck_id
                        WHERE ? = user_decks.user_id
                        AND user_decks.deck_id = deck.deck_id""",
            (user_id,),
        )
        rows = cur.fetchall()

        for i in rows:
            deck = {}
            deck["deck_id"] = i["deck_id"]
            deck["d_name"] = i["d_name"]
            deck["d_description"] = i["d_description"]
            decks.append(deck)

    except Error as e:
        decks = []
        print("get_decks", e)

    return decks


def get_decks_by_id(deck_id):
    deck = {}

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM deck WHERE deck_id = ?", (deck_id,))
        row = cur.fetchone()

        deck["deck_id"] = row["deck_id"]
        deck["d_name"] = row["d_name"]
        deck["d_description"] = row["d_description"]

    except Error as e:
        deck = {}

    return deck


def update_deck(deck):
    updated_deck = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE deck SET d_name = ?, d_description = ? WHERE deck_id = ?",
            (
                deck["d_name"],
                deck["d_description"],
            ),
        )

        conn.commit()

        # updated user
        updated_deck = get_decks_by_id(deck["deck_id"])

    except Error as e:
        conn.rollback()
        updated_deck = {}
        print("get_decks_by_id", e)

    finally:
        conn.close


def delete_deck(deck_id):
    message = {}

    try:
        conn = connection()
        conn.execute("DELETE from deck WHERE deck_id = ?", (deck_id,))

        conn.commit()
        message["status"] = "Deck deleted succesfully"

    except:
        conn.rollback()
        message["status"] = "Cannot delete deck"
    finally:
        conn.close()

    return message


# ------------------------------------------------------------------------#

# def insert_user(user):
#     new_users = {}

#     try:
#         conn = connection()
#         cur = conn.cursor()
#         cur.execute("INSERT INTO user(user_id, username, u_password) VALUES(?,?,?)", (user['user_id'], user['username'], user['password']))
#         conn.commit()

#         new_users = get_users(cur.lastrowid)

#     except Error as e:
#         conn().rollback()
#         print(e)

#     return insert_user

# def get_users():
#     users = []

#     try:
#         conn = connection()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM user")
#         rows = cur.fetchall()

#         for i in rows:
#             user = {}
#             user['user_id'] = i['user_id']
#             user['username'] = i['username']
#             user['password'] = i['password']
#             users.append(user)

#     except Error as e:
#         users = []

#     return users

# def get_users_by_id(user_id):
#     user = {}

#     try:
#         conn = connection()
#         conn.row_factory = sqlite3.Row
#         cur = conn.cursor()
#         cur.execute("SELECT * FROM user WHERE user_id = ?", (user_id,))
#         row = cur.fetchone()

#         user['user_id'] = row['user_id']
#         user['username'] = row['username']
#         user['password'] = row['password']

#     except Error as e:
#         user = {}

#     return user

# def update_user(user):
#     updated_user = {}

#     try:
#         conn = connection()
#         cur = conn.cursor()
#         cur.execute("UPDATE user SET username = ?, password = ? WHERE user_id = ?", (user['username'], user['password'],))

#         conn.commit()

#         #updated user
#         updated_user = get_users_by_id(user['user_id'])

#     except Error as e:
#         conn.rollback()
#         updated_user = {}
#         print(e)

#     finally:
#         conn.close

# def delete_user(user_id):
#     message = {}

#     try:
#         conn = connection()
#         conn.execute("DELETE from user WHERE user_id = ?", (user_id,))

#         conn.commit()
#         message['status'] = "Deck deleted succesfully"

#     except:
#         conn.rollback()
#         message['status'] = "Cannot delete deck"
#     finally:
#         conn.close()

#     return message

# ------------------------------------------------------------------------#


def insert_card(side1, side2, deck_id):
    try:
        conn = connection()
        cur = conn.cursor()

        cur.execute("SELECT side_id FROM side ORDER BY side_id DESC LIMIT 1")
        last_side_id = int(cur.fetchone()[0])
        side1["side_id"] = last_side_id + 1
        side2["side_id"] = last_side_id + 2

        insert_side(side1)
        insert_side(side2)

        cur.execute(
            "SELECT flashcard_id FROM flashcard ORDER BY flashcard_id DESC LIMIT 1"
        )

        card_id = int(cur.fetchone()[0]) + 1
        cur.execute(
            "INSERT INTO flashcard(flashcard_id, front_id, back_id, correct_count, incorrect_count) VALUES(?, ?, ?, ?, ?)",
            (
                card_id,
                last_side_id + 1,
                last_side_id + 2,
                0,
                0,
            ),
        )

        cur.execute("INSERT INTO card_in_deck(deck_id, card_id) VALUES(?, ?)", (deck_id, card_id))
        conn.commit()
    except Error as e:
        conn().rollback()
        print(repr(e))

    return 200


def insert_side(side):
    try:
        conn = connection()
        cur = conn.cursor()

        cur.execute("SELECT side_id FROM side ORDER BY side_id DESC LIMIT 1")

        cur.execute(
            "INSERT INTO side(side_id, s_header, s_body) VALUES(?,?,?)",
            (
                side["side_id"],
                side["s_header"],
                side["s_body"],
            ),
        )
        conn.commit()

    except Error as e:
        conn().rollback()
        print(repr(e))

    return 200


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
            side["side_id"] = i["side_id"]
            side["s_header"] = i["s_header"]
            side["s_body"] = i["s_body"]
            sides.append(side)

    except Error as e:
        sides = []

    return sides

    
def get_cards(deck_id):
    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cards = []
        cur.execute("""
            SELECT f.correct_count AS correct, f.incorrect_count AS incorrect, 
                    front.s_header AS front_header, front.s_body AS front_body,
                    back.s_header AS back_header, back.s_body AS back_body
            FROM (
                SELECT card_in_deck.card_id FROM card_in_deck WHERE card_in_deck.deck_id = ?
            ) AS cid
                INNER JOIN flashcard AS f ON cid.card_id = f.flashcard_id
                INNER JOIN side AS front ON f.back_id = front.side_id
                INNER JOIN side AS back ON f.front_id = back.side_id
        """, (deck_id,))
        rows = cur.fetchall()
        print(len(rows))
        for i in rows:
            card = {}
            # print(i)
            for key in i.keys():
                card[key] = i[key]
            cards.append(card)
        return cards
    except Error as e:
        print("Error in get cards", e)
        return None


def get_sides_by_id(side_id):
    side = {}

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM side WHERE side_id = ?", (side_id,))
        row = cur.fetchone()

        side["side_id"] = row["side_id"]
        side["s_header"] = row["s_header"]
        side["s_body"] = row["s_body"]

    except Error as e:
        side = {}

    return side


def update_side(side):
    updated_side = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE side SET s_header = ?, s_body = ?, WHERE side_id = ?",
            (
                side["s_header"],
                side["s_body"],
            ),
        )

        conn.commit()

        # updated user
        updated_side = get_sides_by_id(side["side_id"])

    except Error as e:
        conn.rollback()
        updated_side = {}
        print("update_side", e)

    finally:
        conn.close


def delete_side(side_id):
    message = {}

    try:
        conn = connection()
        conn.execute("DELETE from side WHERE side_id = ?", (side_id,))

        conn.commit()
        message["status"] = "Deck deleted succesfully"

    except:
        conn.rollback()
        message["status"] = "Cannot delete deck"
    finally:
        conn.close()

    return message


# --------------------------------------------------------#


def insert_category(cat):

    try:
        conn = connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT category_id FROM categories ORDER BY category_id DESC LIMIT 1"
        )
        new_cat = {"category_id": int(cur.fetchone()[0]) + 1, "c_name": cat}

        cur.execute(
            "SELECT category_id FROM categories ORDER BY category_id DESC LIMIT 1"
        )
        new_cat = {"category_id": int(cur.fetchone()) + 1, "c_name": cat}

        cur.execute(
            "INSERT INTO categories(category_id, c_name) VALUES(?,?)",
            (
                new_cat["category_id"],
                new_cat["c_name"],
            ),
        )
        conn.commit()

    except Error as e:
        conn().rollback()
        print("insert_category", e)

    return 200


@app.route("/api/cats/add", methods=["GET", "POST"])
def api_add_cat():
    cat = request.get_json()["c_name"]
    # print(cat)
    return jsonify(insert_category(cat))

def get_category(user_id):
    cats = []

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            """SELECT DISTINCT categories.category_id, categories.c_name
                FROM (
                    SELECT user_decks.deck_id
                    FROM user_decks
                    WHERE user_decks.user_id = ?
                ) AS d
                INNER JOIN card_in_deck ON d.deck_id = card_in_deck.deck_id
                INNER JOIN card_category ON card_in_deck.card_id = card_category.card_id
                INNER JOIN categories ON card_category.category_id = categories.category_id""",
            (user_id,),
        )
        rows = cur.fetchall()

        for i in rows:
            cat = {}
            cat["category_id"] = i["category_id"]
            cat["c_name"] = i["c_name"]
            cats.append(cat)

    except Error as e:
        cats = []

    print(cats)
    return cats


@app.route("/api/cats", methods=["GET"])
def api_get_cats():
    return jsonify(get_category(logged_in_user_id()))


def user_history(user_id):
    history = []

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            """SELECT cur_date, correct_ratio
            FROM u_session
            WHERE sess_userid = ?
            ORDER BY cur_date DESC""",
            (user_id,),
        )
        rows = cur.fetchall()

        for i in rows:
            session = {}
            session["cur_date"] = i["cur_date"]
            session["correct_ratio"] = i["correct_ratio"]
            history.append(session)

    except Error as e:
        history = []

    return history


@app.route("/api/history", methods=["GET"])
def api_get_history():
    return jsonify(user_history(logged_in_user_id()))


@app.route("/history", methods=["GET"])
def history():
    return render_template("history.html")


# -------------Complex-------------#
def average_decks_per_user():
    message = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT AVG(c) 
            FROM (
                SELECT COUNT(*) AS c
                FROM user_decks
                GROUP BY user_decks.user_id
            )
        """
        )

        result = cur.fetchone()[0]
    except:
        conn.rollback()
        message["status"] = "Failed to find average deck count"

    finally:
        conn.close()

    return result


@app.route("/api/generic", methods=["GET"])
def api_avg_user():
    return jsonify(average_decks_per_user())


def categories_to_deck(categories_list, deck_id):
    message = {}

    category = categories_list

    try:
        conn = connection()
        # find cards from each category
        cards = []
        cur = conn.cursor()
        cur.execute(
            """
            SELECT card_category.card_id
            FROM categories
                INNER JOIN card_category ON categories.category_id = card_category.category_id
            WHERE categories.c_name LIKE ?
        """,
            (f"%{category}%",),
        )
        cards = cur.fetchall()
        # insert into the deck
        for card in cards:
            # print(card[0])
            cur.execute("INSERT INTO card_in_deck VALUES(?,?)", [deck_id, card[0]])
            # conn.execute("INSERT INTO card_in_deck VALUES(?)", zip([deck_id for x in cards], map(lambda x: x["card_id"], cards)))
        conn.commit()

        message["status"] = "Success"

    except Error as e:
        conn.rollback()
        print(repr(e))

    finally:
        conn.close()

    return message


def deck_ranking(deck_id):

    message = {}

    conn = connection()
    # Find all sessions with a deck
    cur = conn.cursor()
    cur.execute(
        """
        SELECT user.username, AVG(u_session.correct_ratio)
        FROM (
            SELECT session_id AS matching_sessions
            FROM session_deck
            WHERE session_deck.deck_id = ?
        )
            INNER JOIN u_session ON matching_sessions = u_session.session_id
            INNER JOIN user ON u_session.sess_userid = user.user_id
        GROUP BY user.user_id;
    """,
        (deck_id,),
    )

    print(cur.fetchall())

    message["status"] = "Success"

    return message


@app.route("/api/complex/<deck_id>", methods=["GET"])
def api_complex_rank(deck_id):
    return jsonify(deck_ranking(deck_id))


@app.route("/api/complex/<categories_list>&<deck_id>", methods=["GET", "PUT"])
def api_complex_cat(categories_list, deck_id):
    return jsonify(categories_to_deck(categories_list, deck_id))


# Search Bar #
def search_bar(keyword, deck, category):
    results = []

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute("""SELECT front.s_header as front_header, front.s_body as front_body, back.s_header as back_header, back.s_body as back_body, deck.d_name as deck_search, categories.c_name as category_search
                        FROM side as front, side as back, flashcard, deck, categories, card_category, card_in_deck
                        WHERE front.side_id = flashcard.front_id
                        AND back.side_id = flashcard.back_id
                        AND flashcard.flashcard_id = card_category.card_id
                        AND card_category.category_id = categories.category_id
                        AND flashcard.flashcard_id = card_in_deck.card_id
                        AND card_in_deck.deck_id = deck.deck_id
                        AND (front.s_header LIKE ? OR front.s_body LIKE ?
                        OR back.s_header LIKE ? OR back.s_body LIKE ?)
                        AND d_name = ?
                        AND c_name = ?""", ('%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', '%' + keyword + '%', deck, category,),
                    )
        
        rows = cur.fetchall()
        print(rows)

        for i in rows:
            result = {}
            result['front_header'] = i[2]
            result['front_body'] = i[3]
            result['back_header'] = i[0]
            result['back_body'] = i[1]
            result['deck_search'] = i[4]
            result['category_search'] = i[5]
            results.append(result)

    except Error as e:
        results = []
        print(e)

    return results

@ app.route("/api/search", methods=['GET', 'POST'])
def search_query():
    keyword = request.args.get("keyword")
    deck_name = request.args.get("deckname")
    category_name = request.args.get("categoryname0")
    print(keyword, deck_name, category_name)
    return jsonify(search_bar(keyword, deck_name, category_name))

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        keyword = request.form.get("keyword")
        deck_name = request.form.get("deckname")
        category_name = request.form.get("categoryname0")
        return jsonify(search_bar(keyword, deck_name, category_name))

# -------------DECKS-------------#
@app.route("/api/decks", methods=["GET"])
def api_get_decks():
    return jsonify(get_decks(logged_in_user_id()))


@app.route("/api/decks/<deck_id>", methods=["GET"])
def api_get_deck(deck_id):
    return jsonify(get_decks_by_id(deck_id))


@app.route("/api/decks/add", methods=["GET", "POST"])
def api_add_deck():
    deck = request.get_json()
    return jsonify(insert_deck(deck))


@app.route("/api/decks/update", methods=["PUT"])
def api_update_deck():
    deck = request.get_json()
    return jsonify(update_deck(deck))


@app.route("/api/decks/delete/<deck_id>", methods=["DELETE"])
def api_delete_deck(deck_id):
    return jsonify(delete_deck(deck_id))


# -----------USERS----------#
# @app.route('/api/users', methods=['GET'])
# def api_get_users():
#     return jsonify(get_users())

# @app.route('/api/users/add', methods=['GET', 'POST'])
# def api_add_user():
#     user = request.get_json()
#     return jsonify(insert_user(user))

# @app.route('/api/users/<user_id>', methods=['GET'])
# def api_get_user(user_id):
#     return jsonify(get_users_by_id(user_id))

# @app.route('/api/users/update', methods=['PUT'])
# def api_update_user():
#     user = request.get_json()
#     return jsonify(update_user(user))

# @app.route('/api/users/delete/<user_id>', methods=['DELETE'])
# def api_delete_user(user_id):
#     return jsonify(delete_user(user_id))

# -----------SIDES------------#
@app.route("/api/sides", methods=["GET"])
def api_get_sides():
    return jsonify(get_sides())

@app.route("/api/cards/<deck_id>", methods=["GET"])
def api_get_cards(deck_id):
    return jsonify(get_cards(deck_id))


@app.route("/api/sides/<side_id>", methods=["GET"])
def api_get_side(side_id):
    return jsonify(get_sides_by_id(side_id))


@app.route("/api/sides/add", methods=["GET", "POST"])
def api_add_side():
    (side1, side2) = request.get_json()
    # print(side1, side2)
    return jsonify(insert_card(side1, side2))


@app.route("/api/sides/update", methods=["PUT"])
def api_update_side():
    side = request.get_json()
    return jsonify(update_side(side))


@app.route("/api/sides/delete/<side_id>", methods=["DELETE"])
def api_delete_side(side_id):
    return jsonify(delete_side(side_id))


if __name__ == "__main__":
    app.run(debug=True)
