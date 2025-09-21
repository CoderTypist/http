CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (username, email)
VALUES
    ('jsmith', 'john.smith@gmail.com'),
    ('wsmith', 'will.smith@gmail.com'),
    ('asmith', 'azmuth@gmail.com'),
    ('olmyth', 'olmyth@gmail.com'),
    ('banned', 'unkind.person@gmail.com');

.print
SELECT * FROM users;

UPDATE users SET email = 'allen.smith@gmail.com' WHERE username = 'asmith';
UPDATE users SET username = 'osmith', email = 'ole.smith@gmail.com' WHERE username = 'olmyth';
DELETE FROM users WHERE username = 'banned';

.print
SELECT * FROM users;
