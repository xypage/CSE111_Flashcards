CREATE TABLE IF NOT EXISTS flashcard (
    flashcard_id        INTEGER NOT NULL PRIMARY KEY,
    front_id            INTEGER NOT NULL,
    back_id             INTEGER NOT NULL,
    correct_count       INTEGER NOT NULL,
    incorrect_count     INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS deck (
    deck_id             INTEGER NOT NULL PRIMARY KEY,
    d_name              VARCHAR(50) NOT NULL,
    d_description       VARCHAR(200) NOT NULL,
    icon_path           VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS card_in_deck (
    deck_id                INTEGER NOT NULL,
    card_id                INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS user (
    user_id             INTEGER NOT NULL PRIMARY KEY,
    username            VARCHAR(25) NOT NULL,
    u_password          VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS user_decks (
    user_id                INTEGER NOT NULL,
    deck_id                INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS u_session (
    session_id          INTEGER NOT NULL PRIMARY KEY,
    cur_date            datetime DEFAULT(getdate()),
    correct_ratio       INTEGER NOT NULL,
    sess_userid         INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS session_deck (
    session_id          INTEGER NOT NULL,
    deck_id                INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS spacing (
    spacing_id          INTEGER NOT NULL PRIMARY KEY,
    card_id             INTEGER NOT NULL,
    s_interval          INTEGER NOT NULL,
    ef                  DECIMAL(5, 4) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    category_id         INTEGER NOT NULL PRIMARY KEY,
    c_name              VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS card_category (
    category_id            INTEGER NOT NULL,
    card_id                INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS side (
    side_id             INTEGER NOT NULL PRIMARY KEY,
    s_header            VARCHAR(100) NOT NULL,
    s_body              VARCHAR(200) NOT NULL,
    img_path            VARCHAR(50)
);