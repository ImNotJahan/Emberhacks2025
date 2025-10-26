CREATE TABLE IF NOT EXISTS users (
    id        INTEGER PRIMARY KEY,
    username  VARCHAR(64) NOT NULL,
    email     VARCHAR(128) NOT NULL,
    password  VARCHAR(128) NOT NULL
);