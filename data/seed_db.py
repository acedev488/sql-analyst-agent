import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / 'sample.db'

STORES = [
    (1, "Downtown", "Seattle"),
    (2, "Riverside", "Portland"),
    (3, "Uptown", "Denver"),
]

PRODUCTS = [
    (1, "Espresso", 3.25),
    (2, "Latte", 4.75),
    (3, "Cappuccino", 4.50),
    (4, "Cold Brew", 4.25),
    (5, "Drip Coffee", 2.75),
    (6, "Mocha", 5.00),
    (7, "Croissant", 3.50),
    (8, "Blueberry Muffin", 3.25),
]

START_DATE = date(2024, 7, 1)
END_DATE = date(2024, 12, 31)


def build_database(path: Path = DB_PATH, seed: int = 42) -> None:
    rng = random.Random(seed)
    path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(path)
    cur = conn.cursor()

    cur.executescript(
        """
        DROP TABLE IF EXISTS sales;
        DROP TABLE IF EXISTS stores;
        DROP TABLE IF EXISTS products;

        CREATE TABLE stores (
            store_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            city TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            unit_price REAL NOT NULL
        );

        CREATE TABLE sales (
            sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
            sale_date TEXT NOT NULL,
            store_id INTEGER NOT NULL REFERENCES stores(store_id),
            product_id INTEGER NOT NULL REFERENCES products(product_id),
            quantity INTEGER NOT NULL,
            revenue REAL NOT NULL
        );
        """
    )

    cur.executemany('INSERT INTO stores VALUES (?, ?, ?)', STORES)
    cur.executemany('INSERT INTO products VALUES (?, ?, ?)', PRODUCTS)

    rows = []
    day = START_DATE
    while day <= END_DATE:
        weekend_boost = 1.4 if day.weekday() >= 5 else 1.0
        for store_id, *_ in STORES:
            for product_id, _, unit_price in PRODUCTS:
                if rng.random() < 0.15:
                    continue  # skip so not every product sells everywhere every day
                qty = max(1, round(rng.randint(1, 12) * weekend_boost))
                revenue = round(qty * unit_price, 2)
                rows.append((day.isoformat(), store_id, product_id, qty, revenue))
        day += timedelta(days=1)

    cur.executemany(
        "INSERT INTO sales (sale_date, store_id, product_id, quantity, revenue) "
        "VALUES (?, ?, ?, ?, ?)",
        rows,
    )

    conn.commit()
    conn.close()
    print(f'Built {path} with {len(rows)} sales rows.')


if __name__ == "__main__":
    build_database()
