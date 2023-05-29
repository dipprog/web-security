# CSRF

## Session Management

`user > web application`

```shell
/login.php username/password: admin/admin - (1)
```

`web application > user`

```shell
Set-Cookie: session=66htna8ujukmhjsxutvd - (2)
```

`user > web application`

```shell
session=66htna8ujukmhjsxutvd
```

1. User need to access the banking application. First thing the user need to do is to supply the banking application with his credentials

2. The application then set a cookie in user browser. A `cookie` is a text file that contains some information that identifies a user to the backend. For the mejority of the application, the cookie value is long random string that is not easily predictable. Some application makes use of cookie that contains user indentifiable information like user name, the role user has in application and so on.

3. That cookie will be used to identify the user in all future requests.

When a user access a domain he/she has accessed before, the browser checks the cokie jar which contains all the information of the application the user has visited. The browser asks the cookie jar, do u have any cookies for so and so domain. If the cookie jar has any cookie related to that requested domain, then cookie get sent with the request. Now when the backend receive the cookie, it checks which user is assigned to that cookie, next it checks the the permission the user has. If the user has the permission to access the resources that was requested, then the application return the resources to the user in the browser, else, access denied message is return in the response.

## Cross Site Request Forgery(CSRF)

- It is an attack where the attacker causes the victim user to carry out an action unintentionally while that user is authenticated to a web application.

- Important pre-requsite for CSRF to be successful > victim user has to be already logged in to the application.

### Steps in CSRF vulnerability

1. Send the victim user with a malicious link that will conduct the CSRF attack
   `Attacker > Victim`

```shell
https://bank.com/email/change?email=attacker@gmail.ca
```

If the victim user is already logged in to the bank application and click on the attacker's link. Then the attacker will able to sucessfully get the victim user to change his email address to one of attacker's choice.

2. When the victim user click on the link, the browser goes through the cookie jar and ask do I have any session cookie for the domain 'bank.com' and user is logged in, so cookie jar will have the cookie related to that domain, the action will be performed on user behave with user session cookie. Email address of user will be changed to email address of the attacker. What we are really doing here is exploiting the default functionality of the browser to automatically send the cookie to the assigned domain.
   `Victim > Web application`

```shell
https://bank.com/email/change?email=attacker@gmail.ca
```

3. Now the email has been changed. so attacker will use the forget password functionality of the web application to change the password and compromise the user's account.

## CSRF condtions

- For CSRF attack to be possible, three key conditions must be in place:
  - A relevent action \*\*
  - Cookie-based session handling
  - No unpredictable request parameters

So, in order to defend CSRF attack, we append a unpredictable parameter such as csrf_token to each sensitive request.

## Impact of CSRF Attacks

- Depending on the functionality in the application that is being exploited
  - Confidentiality - it can be none / partial(Low) / High
  - Integrity - usually either Partial or High
  - Availability - can be none / partial(low) / high
- Remote code execution on the server

## How to find CSRF vulnerabilities?

- `Black Box Testing`

  - Map the application
    - Review all the key functionality in the application and make notes
  - Identify all application functions that satisfy the following conditions
    - A relevant action
    - Cookie-based session handling
    - No unpredictable request parameters
  - Create a PoC(Proof of Concept) script to exploit CSRF
    - GET request: `<img>` tag with `src` attribute set to vulnerable URL
    - POST request: form with `hidden` fields for all the required parameters and the `target` set to vulnerable URL

- `White Box Testing` - (Best to do in Black Box)
  - Identify the framework that is being used by the application.
  - Find out how this framework defends against CSRF attacks(Google search)
  - Review code to ensure that the build in defenses have not been disabled.
  - Review all sensitive functionality to ensure that the CSRF defense has been applied

## How to exploit CSRF vulnerabilities?

`GET Scenario` - (never use GET request to submit data)

```shell
GET https://bank.com/email/change?email=test@test.ca HTTP/1.1
```

Script:

```html
<html>
  <body>
    <h1>Hello World!</h1>
    <img
      src="
        https://bank.com/email/change?email=at
        tacker@gmail.ca
        "
      width="0"
      height="0"
      border="0"
    />
  </body>
</html>
```

`POST Scenario` -

```shell
POST /email/change HTTP/1.1
Host: https://bank.com
…
email=test@test.ca
```

Script:

```html
<html>
  <body>
    <h1>Hello World!</h1>
    <iframe style="display:none" name="csrf-iframe"></iframe>
    <form
      action=" https://bank.com/email/change/"
      method="POST"
      target="csrf-
iframe"
      id="csrf-form"
    >
      <input type="hidden" name="email" value="test@test.ca" />
    </form>
    <script>
      document.getElementById("csrf-form").submit();
    </script>
  </body>
</html>
```

## How to prevent CSRF attacks

- Primary defense (Compulsory)
  - Use a CSRF token in relevant requests.
    - `Unpredictable with high entropy, simlar to session tokens`
    - `Tied to the user's session` (otherwise, attacker will logged in with his account to generate a CSRF token, use that token with CSRF attack link). If they are tied together, in the backend, it will check if the csrf token is corresponding to the given session.
    - `Validated before the relevant action is execulted.`
    ```shell
    POST /my-account/change-email HTTP/1.1
    ...
    email=test%40test.ca&csrf=Xobadkdkteh3563dhhhhhhhhhsms3eyye
    ```
- Additional Defense (Addition to Primary Defense)
  - Use of Samesite cookies
- Inadequate Defense (can easily be bypassed)
  - Use of Referer header

## Primary Defense - How CSRF tokens be transmitted

- Hidden field of an HTML form that is submitted using a POST method \*(common)
- Custom request header (not common)
- Tokens submitted in the URL query string are less secure (less secure)
- Tokens generally should not be transmitted within cookies (less Secure) . Because the browser automatically send the cookies.

## How should CSRF tokens be validated?

- Generated tokens should be stored server-side within the user’s session data
- When performing a request, a validation should be performed that verifies that the submitted token matches the value that is stored in the user’s session
- Validation should be performed regardless of HTTP method or content type of the request
- If a token is not submitted, the request should be rejected

## Additional Defense - SameSite Cookies

- The SameSite attribute can be used to control whether cookies are submitted in cross-site requests. `Strict` - If the request is initiated by a third party website, then the cookie will not be send / submitted. Cookie only send if the request initiated by First party. `Lax` - will include the cookie if request is originated from a third party only if 2 conditions ar met > 1) Request use a get method. 2) Request has to be resulted from top level novigation by the user such as clicking a link.

```shell
Set-Cookie: session=test; SameSite=Strict
Set-Cookie: session=test; SameSite=Lax
Set-Cookie: flavor=choco; SameSite=None; Secure
```

## Inadequate Defense - Referer Header

The `Referer` HTTP request header contains an absolute or partial address of the page making the request.

- Referer headers can be spoofed
- The defense can usually be bypassed:
  - Example #1 – if it's not present, the application does not check for it.
  - Example #2 – the referrer header is only checked to see if it contains the domain and exact match is not made.

## Additional Resources

- Web Security Academy - CSRF
  - https://portswigger.net/web-security/csrf
- Web Application Hacker’s Handbook
  - Chapter 13 - Attacking Users: Other Techniques (pgs. 504– 511)
- OWASP – CSRF
  - https://owasp.org/www-community/attacks/csrf
- Cross-Site Request Forgery Prevention Cheat Sheet
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
- Reviewing Code for Cross-Site Request Forgery Issues Overview
  - https://owasp.org/www-project-code-review-guide/reviewing-code-for-csrf-issues
