CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER REFERENCES orders,
    item_no INTEGER,
    product_id INTEGER REFERENCES inventory,
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);

.print
.print --- inventory (before) ---
SELECT * FROM inventory;
.print

BEGIN TRANSACTION;
    INSERT OR ROLLBACK INTO orders (user_id) VALUES ((SELECT user_id FROM users WHERE username = 'jsmith'));
    INSERT OR ROLLBACK INTO order_items (order_id, item_no, product_id, quantity) VALUES
        (
            (SELECT MAX(rowid) FROM orders),
            1,
            (SELECT product_id FROM inventory WHERE name = 'The Magician''s Nephew'),
            3
        ),
        (
            (SELECT MAX(rowid) FROM orders),
            2,
            (SELECT product_id FROM inventory WHERE name = 'The Lion, the Witch, and the Wardrobe'),
            2
        );
    UPDATE OR ROLLBACK inventory SET quantity = quantity - 3 WHERE name = 'The Magician''s Nephew';
    UPDATE OR ROLLBACK inventory SET quantity = quantity - 2 WHERE name = 'The Lion, the Witch, and the Wardrobe';
COMMIT;

BEGIN TRANSACTION;
    INSERT OR ROLLBACK INTO orders (user_id) VALUES ((SELECT user_id FROM users WHERE username = 'osmith'));
    INSERT OR ROLLBACK INTO order_items (order_id, item_no, product_id, quantity) VALUES
        (
            (SELECT MAX(rowid) FROM orders),
            1,
            (SELECT product_id FROM inventory WHERE name = 'The Voyage of the Dawn Treader'),
            1
        ),
        (
            (SELECT MAX(rowid) FROM orders),
            2,
            (SELECT product_id FROM inventory WHERE name = 'The Last Battle'),
            1
        );
    UPDATE OR ROLLBACK inventory SET quantity = quantity - 1 WHERE name = 'The Voyage of the Dawn Treader';
    UPDATE OR ROLLBACK inventory SET quantity = quantity - 1 WHERE name = 'The Last Battle';
COMMIT;

.print --- inventory (after) ---
SELECT * FROM inventory;
.print

.print --- orders ---
SELECT
    orders.order_id,
    users.username,
    order_items.item_no,
    order_items.product_id,
    order_items.quantity,
    inventory.cost,
    inventory.name
FROM orders
JOIN users ON orders.user_id = users.user_id
JOIN order_items ON orders.order_id = order_items.order_id
JOIN inventory ON order_items.product_id = inventory.product_id;
.print

.print --- order totals ---
SELECT
    order_items.order_id,
    SUM(order_items.quantity * inventory.cost) AS order_total
FROM order_items
JOIN inventory ON order_items.product_id = inventory.product_id
GROUP BY order_items.order_id;
