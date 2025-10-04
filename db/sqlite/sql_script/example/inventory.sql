CREATE TABLE IF NOT EXISTS inventory (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quantity INTEGER DEFAULT 0 CHECK (quantity >= 0),
    cost REAL NOT NULL CHECK (cost > 0),
    name TEXT NOT NULL UNIQUE CHECK (length(name) < 256),
    category TEXT DEFAULT '' CHECK (length(category) < 32),
    description TEXT DEFAULT '' CHECK (length(description < 4096))
);

INSERT INTO inventory(quantity, cost, name, category, description)
VALUES
    (90, 6.99, 'The Magician''s Nephew', 'Book', 'The first book'),
    (80, 6.99, 'The Lion, the Witch, and the Wardrobe', 'Book', 'The second book'),
    (70, 7.99, 'Prince Caspian', 'Book', 'The third book'),
    (60, 7.99, 'The Voyage of the Dawn Treader', 'Book', 'The fourth book'),
    (50, 8.99, 'The Silver Chair', 'Book', 'The fifth book'),
    (40, 8.99, 'The Horse and His Boy', 'Book', 'The sixth book'),
    (30, 8.99, 'The Last Battle', 'Book', 'The seventh book');
