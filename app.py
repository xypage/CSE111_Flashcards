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


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    print("HERE")

    if form.validate_on_submit():
        print("IN LOOP")
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            print("GOT USER")
            if bcrypt.check_password_hash(user.u_password, form.password.data):
                print("CHECKED USER")
                login_user(user)
                print("LOGGED IN")
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
            icon_path           VARCHAR(75));
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
            img_path            VARCHAR(30));
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
        print(e)


def insert_deck(deck):
    new_decks = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO deck(deck_id, d_name, d_description, icon_path) VALUES(?,?,?,?)",
            (deck["deck_id"], deck["d_name"], deck["d_description"], deck["icon_path"]),
        )
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
            deck["deck_id"] = i["deck_id"]
            deck["d_name"] = i["d_name"]
            deck["d_description"] = i["d_description"]
            deck["icon_path"] = i["icon_path"]
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

        deck["deck_id"] = row["deck_id"]
        deck["d_name"] = row["d_name"]
        deck["d_description"] = row["d_description"]
        deck["icon_path"] = row["icon_path"]

    except Error as e:
        deck = {}

    return deck


def update_deck(deck):
    updated_deck = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE deck SET d_name = ?, d_description = ?, icon_path = ? WHERE deck_id = ?",
            (
                deck["d_name"],
                deck["d_description"],
                deck["icon_path"],
            ),
        )

        conn.commit()

        # updated user
        updated_deck = get_decks_by_id(deck["deck_id"])

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


def insert_side(side):
    new_sides = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO side(side_id, s_header, s_body, img_path) VALUES(?,?,?,?)",
            (side["side_id"], side["s_header"], side["s_body"], side["img_path"]),
        )
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
            side["side_id"] = i["side_id"]
            side["s_header"] = i["s_header"]
            side["s_body"] = i["s_body"]
            side["img_path"] = i["img_path"]
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

        side["side_id"] = row["side_id"]
        side["s_header"] = row["s_header"]
        side["s_body"] = row["s_body"]
        side["img_path"] = row["img_path"]

    except Error as e:
        side = {}

    return side


def update_side(side):
    updated_side = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "UPDATE side SET s_header = ?, s_body = ?, img_path = ? WHERE side_id = ?",
            (
                side["s_header"],
                side["s_body"],
                side["img_path"],
            ),
        )

        conn.commit()

        # updated user
        updated_side = get_sides_by_id(side["side_id"])

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
        message["status"] = "Deck deleted succesfully"

    except:
        conn.rollback()
        message["status"] = "Cannot delete deck"
    finally:
        conn.close()

    return message


# --------------------------------------------------------#


def insert_category(cat):
    new_cat = {}

    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO categories(category_id, c_name) VALUES(?,?)",
            (cat["category_id"], cat["c_name"]),
        )
        conn.commit()

        new_cat = get_category(cur.lastrowid)

    except Error as e:
        conn().rollback()
        print(e)

    return insert_category


def get_category():
    cats = []

    try:
        conn = connection()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()

        for i in rows:
            cat = {}
            cat["category_id"] = i["category_id"]
            cat["c_name"] = i["c_name"]
            cats.append(cat)

    except Error as e:
        cats = []

    return cats


@app.route("/api/cats", methods=["GET"])
def api_get_cats():
    return jsonify(get_category())


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


# -------------DECKS-------------#
@app.route("/api/decks", methods=["GET"])
def api_get_decks():
    return jsonify(get_decks())


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


@app.route("/api/sides/<side_id>", methods=["GET"])
def api_get_side(side_id):
    return jsonify(get_sides_by_id(side_id))


@app.route("/api/sides/add", methods=["GET", "POST"])
def api_add_side():
    side = request.get_json()
    return jsonify(insert_side(side))


@app.route("/api/sides/update", methods=["PUT"])
def api_update_side():
    side = request.get_json()
    return jsonify(update_side(side))


@app.route("/api/sides/delete/<side_id>", methods=["DELETE"])
def api_delete_side(side_id):
    return jsonify(delete_side(side_id))


if __name__ == "__main__":
    app.run(debug=True)
