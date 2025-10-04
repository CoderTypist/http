.mode column
.bail on

.print === CLEANUP ===
.read drop.sql
.print

.print === USERS ===
.read users.sql
.print

.print === INVENTORY ===
.read inventory.sql
.print

.print === ORDERS ===
.read orders.sql
.print
