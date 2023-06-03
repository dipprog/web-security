## Same-Origin Policy(SOP)

SOP is a rule that is enfornced by browsers to control access to data between web applications.

**Example**:

Imagine you have two websites: "https://www.example.com" and "https://www.attacker.com." The Same-Origin Policy states that JavaScript code running on a web page from "https://www.example.com" is only allowed to access resources (such as data, cookies, or DOM elements) from the same origin, which is "https://www.example.com" in this case. So, if you have a JavaScript code snippet on "https://www.example.com" that tries to access resources from "https://www.attacker.com," the browser will block the request due to the SOP.

**Real-Life Analogy**:
Let's say you live in an apartment complex, and each apartment represents a different origin. Each apartment has its own set of belongings, and the doors and windows of each apartment represent the security boundaries. The Same-Origin Policy can be compared to the security policy within the apartment complex.

In this analogy:

- JavaScript code running on one apartment's balcony can access the items within that apartment (same origin) without any restrictions. This represents the code running on a web page accessing resources from the same origin.
- However, JavaScript code on one apartment's balcony cannot reach out to another apartment's belongings (different origin) through the windows or doors. This represents the SOP blocking access to resources from a different origin.

Similarly, the Same-Origin Policy prevents JavaScript code on a web page from accessing resources (such as cookies, data, or DOM elements) from a different origin for security reasons. This restriction helps prevent malicious activities, like unauthorized access or data theft.

It's important to note that the Same-Origin Policy applies specifically to client-side scripting languages, like JavaScript, executed within the browser. Server-side interactions are not bound by the Same-Origin Policy, and APIs can have their own mechanisms, such as CORS, to control cross-origin access.

## Origin

In web development, an "origin" refers to the combination of three components: the `protocol`, `domain`, and `port`. The protocol specifies the communication protocol used, such as HTTP or HTTPS. The domain represents the host or website's address, like 'example.com'. The port identifies the specific port number used for communication, typically omitted if using the default ports (80 for HTTP and 443 for HTTPS).

To better understand the concept of "origin," let's use an example:

**Example**:
Consider the following URLs:

1. https://www.example.com
2. http://api.example.com:8080
3. https://subdomain.example.com

In the example above, each URL represents a distinct origin due to differences in the protocol, domain, or port.

1. The first URL, "https://www.example.com," has the protocol "https," the domain "www.example.com," and uses the default port 443. This URL represents one origin.

2. The second URL, "http://api.example.com:8080," has the protocol "http," the domain "api.example.com," and uses port 8080 explicitly. This URL represents a different origin from the first one due to the protocol, port, and domain differences.

3. The third URL, "https://subdomain.example.com," has the same protocol "https" and port as the first URL but differs by having the subdomain "subdomain."

**Real-Life Analogy**:

Let's use a real-life analogy to understand the concept of "origin" better.

Imagine you have a group of houses in a neighborhood, and each house represents a distinct origin. In this analogy:

- The protocol represents the mode of transportation used to reach a house, such as walking, driving, or biking.
- The domain represents the specific street and house address where a house is located.
- The port represents a specific entrance or door used to access a house.

Using this analogy:

- Two houses on the same street but with different street numbers represent different origins (e.g., example.com vs. subdomain.example.com).
- Two houses on different streets, even if in the same neighborhood, represent different origins (e.g., example.com vs. api.example.com).
- Two entrances of the same house, representing different ports, can also represent different origins (e.g., example.com:8080 vs. example.com:3000).

The Same-Origin Policy considers these distinctions to ensure that interactions between different origins are controlled and restricted by default, promoting security and protecting users from unauthorized access to sensitive information.

# CORS

CORS(Cross-Origin Resource Sharing) is a mechanism that allows web browsers to make cross-origin requests securely. It is enforced by the browser to protect users from malicious activities.

- Uses HTTP headers to define origins that the browser permit loading resources.
- CORS makes use of 2 HTTP headers:
  - `Access-Control-Allow-Origin`
  - `Access-Control-Allow-Credentials`

### Access-Control-Allow-Origin

In the context of Cross-Origin Resource Sharing (CORS), the `Access-Control-Allow-Origin` header is used by a server to indicate which origins are allowed to access its resources. This header is sent as part of the server's response to a cross-origin request made by a client, typically a web browser.

The `Access-Control-Allow-Origin` header can have one of the following values:

1. An origin: For example, `Access-Control-Allow-Origin: https://www.example.com` indicates that the specific origin (`https://www.example.com`) is allowed to access the server's resources.
2. An asterisk (_) wildcard: For example, `Access-Control-Allow-Origin: _` means that any origin is allowed to access the server's resources.

Example:
Let's consider a scenario where a web page hosted on `https://www.example.com` makes a cross-origin request to an API endpoint hosted on `https://api.example.com`. To enable the cross-origin request, the server hosting the API needs to include the `Access-Control-Allow-Origin` header in its response.

Response from `https://api.example.com`:

```
Access-Control-Allow-Origin: https://www.example.com
```

In this example, the server explicitly allows the origin `https://www.example.com` to access its resources. The browser interprets this response and allows the JavaScript code running on `https://www.example.com` to access the API's response data.

Real-Life Analogy:
Let's imagine you are organizing a private event at your residence, and you need to control access to the event. The `Access-Control-Allow-Origin` header can be compared to the guest list that specifies who is allowed to attend.

In this analogy:

- Your residence represents the server hosting the resources.
- Each guest represents an origin (e.g., website or application) that wants to access the resources.
- The guest list represents the `Access-Control-Allow-Origin` header.

To allow access, you can either:

1. Specify the names of specific guests on the list: This is analogous to setting `Access-Control-Allow-Origin` to a specific origin, such as `https://www.example.com`.
2. Use a wildcard (_) to allow anyone to attend: This is analogous to setting `Access-Control-Allow-Origin` to `_`, indicating that any origin is allowed.

By controlling the guest list, you determine who is granted access to the event. Similarly, by setting the `Access-Control-Allow-Origin` header, the server controls which origins are allowed to access its resources.

It's important to note that allowing access from any origin (`*`) can have security implications, as it opens up the resources to potential vulnerabilities. It is generally recommended to specify the allowed origins explicitly for more secure CORS configurations.

### Access-Control-Allow-Credentials

The `Access-Control-Allow-Credentials` header is used in Cross-Origin Resource Sharing (CORS) to indicate whether the server allows the inclusion of credentials (such as cookies, HTTP authentication, or client-side certificates) in cross-origin requests.

When making cross-origin requests, browsers, by default, do not include credentials to protect user privacy and security. However, if a server wants to allow the inclusion of credentials in cross-origin requests, it needs to explicitly set the `Access-Control-Allow-Credentials` header to `true`.

Example:
Let's consider a scenario where a web page hosted on `https://www.example.com` wants to make a cross-origin request that includes credentials, such as cookies, to an API endpoint hosted on `https://api.example.com`. To allow the inclusion of credentials, the server hosting the API needs to include the `Access-Control-Allow-Credentials` header in its response.

Response from `https://api.example.com`:

```
Access-Control-Allow-Origin: https://www.example.com
Access-Control-Allow-Credentials: true
```

In this example, the server not only specifies that `https://www.example.com` is allowed to access its resources using the `Access-Control-Allow-Origin` header but also allows the inclusion of credentials with the `Access-Control-Allow-Credentials` header. The browser, upon receiving this response, allows the JavaScript code running on `https://www.example.com` to include credentials in the cross-origin request to `https://api.example.com`.

It's important to note that the `Access-Control-Allow-Credentials` header cannot be set to `true` when the `Access-Control-Allow-Origin` header is set to `*` (wildcard) because allowing credentials with a wildcard would present a security risk.

Real-Life Analogy:
Let's imagine you are organizing an exclusive club with restricted access, and you want to allow certain trusted members to bring their identification cards (credentials) for entry. The `Access-Control-Allow-Credentials` header can be compared to the club's policy on whether to accept and validate those identification cards.

In this analogy:

- The exclusive club represents the server hosting the resources.
- The trusted members represent the origins (e.g., websites or applications) that want to access the resources with their credentials.
- The identification cards represent the credentials, such as cookies or authentication tokens.

To allow the inclusion of credentials:

- If the club's policy accepts and validates the identification cards from specific trusted members, it corresponds to setting `Access-Control-Allow-Credentials: true` and specifying the allowed origins with `Access-Control-Allow-Origin`.
- If the club's policy does not accept or validate any identification cards, it corresponds to not setting `Access-Control-Allow-Credentials` or setting it to `false`, and the browser will not include credentials in the cross-origin requests.

## CORS vulnerabilities

- CORS vulnerabilities arise from CORS configuration issues.
- Forces developers to use dynamic generation

## Finding CORS Vulnerabilities

CORS vulnerabilities can be identified through both black box testing and white box testing approaches. Let's explore how each approach can help in finding CORS vulnerabilities:

1. Black Box Testing:
   Black box testing involves testing an application without knowledge of its internal implementation details. Testers typically focus on the application's input and output behavior. When testing for CORS vulnerabilities in a black box testing scenario, the tester assumes the role of an external attacker with no internal knowledge of the application.

In black box testing for CORS vulnerabilities, some common techniques include:

- Testing for Cross-Origin Resource Sharing misconfigurations: This involves sending cross-origin requests from different domains and analyzing the server's responses to check if CORS policies are correctly implemented. The tester can vary request headers, origins, and HTTP methods to identify any potential CORS misconfigurations.
- Checking for sensitive data exposure: By making cross-origin requests from different domains, the tester can check if sensitive data, such as user-specific information or authentication tokens, are exposed in the responses or accessible by unauthorized origins.

2. White Box Testing:
   White box testing involves testing an application with access to its internal details, including the source code, architectural diagrams, and configuration settings. Testers can analyze the code and configurations to gain insights into the application's implementation and identify potential security vulnerabilities.

In white box testing for CORS vulnerabilities, some techniques include:

- Reviewing server-side code and configurations: Testers can examine the server-side code and configurations to ensure that CORS policies are correctly implemented. They can check if the `Access-Control-Allow-Origin` header is set appropriately, if the `Access-Control-Allow-Credentials` header is used securely, and if other CORS-related headers are correctly handled.
- Analyzing access control mechanisms: Testers can review the code and configurations to verify if the application has proper access control mechanisms in place to restrict access to sensitive resources and prevent unauthorized cross-origin requests.

Both black box and white box testing approaches are valuable for identifying CORS vulnerabilities. Black box testing helps simulate real-world attack scenarios, while white box testing provides insight into the application's implementation and allows for a more thorough analysis. It is often recommended to combine both approaches to achieve comprehensive testing coverage.

## Exploiting CORS Vulnerabilities

### Preventing CORS Vulnerabilities
