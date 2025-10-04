.echo on
.bail on

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE
);
INSERT INTO users (username, email) VALUES ('matt', 'matt@gmail.com');
INSERT INTO users (username, email) VALUES ('mark', 'mark@gmail.com');

/*
    The failed INSERT will cause an ABORT.
    ABORT is the default conflict resolution strategy.
    In this example, we explicitly added the normally implicit 'OR ABORT'.
    Since we specified '.bail on', execution will not continue.
    Otherwise, the script would have continued.
    This means that 'luke' and 'john' will not get added to the table.
*/
INSERT OR ABORT INTO USERS (username) VALUES ('person', 'person@gmail.com');

INSERT INTO users (username, email) VALUES ('luke', 'luke@gmail.com');
INSERT INTO users (username, email) VALUES ('john', 'john@gmail.com');
