WITH CustomerItemCounts AS (
  SELECT
    s.customer_id,
    m.product_name,
    COUNT(*) AS item_count,
    ROW_NUMBER() OVER (PARTITION BY s.customer_id ORDER BY COUNT(*) DESC) AS row_num
  FROM
    sales s
  JOIN
    menu m ON s.product_id = m.product_id
  GROUP BY
    s.customer_id,
    m.product_name
)
SELECT
  customer_id,
  product_name,
  item_count
FROM
  CustomerItemCounts
WHERE
  row_num = 1;