# Example run

```
$ python main.py

Database schema
- stores(store_id INTEGER, name TEXT, city TEXT)
- products(product_id INTEGER, name TEXT, unit_price REAL)
- sales(sale_id INTEGER, sale_date TEXT, store_id INTEGER, product_id INTEGER,
        quantity INTEGER, revenue REAL)

Ask a question about the data (or type 'exit'):

> Which store had the highest revenue in November 2024?

Generated SQL
SELECT s.name, SUM(sa.revenue) AS total_revenue
FROM sales sa
JOIN stores s ON s.store_id = sa.store_id
WHERE sa.sale_date BETWEEN '2024-11-01' AND '2024-11-30'
GROUP BY s.name
ORDER BY total_revenue DESC
LIMIT 1;

Answer
The Downtown store had the highest revenue in November 2024, bringing in
about $4,180 in total sales, roughly 18% more than the next best-performing
location.

> Show me the daily revenue trend for the Downtown store in October 2024.

Generated SQL
SELECT sa.sale_date, SUM(sa.revenue) AS revenue
FROM sales sa
JOIN stores s ON s.store_id = sa.store_id
WHERE s.name = 'Downtown' AND sa.sale_date BETWEEN '2024-10-01' AND '2024-10-31'
GROUP BY sa.sale_date
ORDER BY sa.sale_date;

Chart saved to charts/latest_chart.png

Answer
Downtown's daily revenue in October hovered around $120-150 on weekdays and
spiked to over $200 on weekends, with the highest single day being Saturday,
October 26th.
```
