CREATE TABLE IF NOT EXISTS flashcard (
    front_id            DECIMAL(4,0) NOT NULL,
    back_id             DECIMAL(4,0) NOT NULL,
    correct_count       DECIMAL(4,0) NOT NULL,
    incorrect_count     DECIMAL(4,0) NOT NULL
);

CREATE TABLE IF NOT EXISTS deck (
    deck_id             DECIMAL(4,0) NOT NULL,
    d_name              VARCHAR(55) NOT NULL,
    d_description       VARCHAR(75) NOT NULL,
    icon_path           VARCHAR(75)
);

CREATE TABLE IF NOT EXISTS user (
    user_id             DECIMAL(4,0) NOT NULL,
    username            VARCHAR(25) NOT NULL,
    u_password          VARCHAR(25) NOT NULL
);

CREATE TABLE IF NOT EXISTS u_session (
    session_id          DECIMAL(4,0) NOT NULL,
    cur_date            datetime DEFAULT(getdate()),
    correct_ratio       DECIMAL(4,0) NOT NULL,
    sess_userid         DECIMAL(3,0) NOT NULL
);

CREATE TABLE IF NOT EXISTS spacing (
    spacing_id          DECIMAL(3,0) NOT NULL,
    card_id             DECIMAL(3,0) NOT NULL,
    s_interval          datetime(10) NOT NULL,
    ef                  DECIMAL(6,3) NOT NULL
);

CREATE TABLE IF NOT EXISTS categories (
    category_id         DECIMAL(3,0) NOT NULL,
    c_name              VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS side (
    side_id             DECIMAL(3,0) NOT NULL,
    s_header            VARCHAR(30) NOT NULL,
    s_body              VARCHAR(100) NOT NULL,
    img_path            VARCHAR(30)
);