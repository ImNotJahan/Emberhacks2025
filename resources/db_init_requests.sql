CREATE TABLE IF NOT EXISTS requests (
    id          INTEGER PRIMARY KEY,
    author_id   INTEGER NOT NULL,
    req         VARCHAR NOT NULL,
    response    VARCHAR NOT NULL,
    created     TEXT NOT NULL,
    CONSTRAINT fk_request_to_user FOREIGN KEY (author_id) REFERENCES users (id)
)