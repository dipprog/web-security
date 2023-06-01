# Server-Side Request Forgery(SSRF)

## What is SSRF?

Server-Side Request Forgery (SSRF) is a vulnerability that occurs when an attacker can manipulate the server to make `unintended HTTP requests to internal or external resources`. This vulnerability can be exploited to access sensitive information, perform unauthorized actions, or pivot within an internal network.

To understand SSRF better, let's consider a `real-life analogy`:

Imagine you visit a restaurant and order a meal. You notice that the menu offers a feature where the waiter will go to any neighboring restaurant to bring you a specific dish if they don't have it. The waiter writes down your request and leaves the restaurant to fulfill it. However, there's a flaw in the system: `the waiter doesn't validate or check if the neighboring restaurant is actually part of the allowed list`.

Exploiting SSRF is like taking advantage of this flaw. You `provide the waiter with a request to visit a different restaurant of your choice`. Since the system doesn't validate the request properly, the waiter goes to the restaurant you specified, retrieves the dish, and brings it back to you. This way, you have `successfully made the waiter act on your behalf to interact with another establishment`.

In the context of web applications, an SSRF vulnerability `allows an attacker to manipulate the server to send HTTP requests to arbitrary destinations`. Here's an example to illustrate this:

Suppose there is a web application with a functionality that fetches and displays the content of a given URL. The application takes a URL as a parameter and retrieves the content using a server-side HTTP request. However, the application fails to properly validate the supplied URL.

An attacker could exploit this vulnerability by providing a malicious URL, such as "http://victim.com/private-info". When the server makes the HTTP request to fetch the content, it inadvertently retrieves and exposes sensitive information from the "victim.com" domain, which may contain internal resources or confidential data.

Moreover, SSRF can extend beyond accessing external resources. Attackers can abuse SSRF to target internal systems that are typically inaccessible from external networks. For instance, an attacker could provide the server with a local IP address or a special "loopback" address like "http://127.0.0.1" to access services running internally. This could allow them to interact with databases, internal APIs, or even exploit other vulnerabilities on the server.

To mitigate SSRF vulnerabilities, developers should implement strict input validation and enforce a whitelist of allowed URLs or IP addresses. Additionally, network segregation and access controls can limit the impact of SSRF attacks by isolating sensitive resources from the web application's server.

## Types of SSRF

1. Regular / In band
2. Blind / Out-of-band

## Impact of SSRF Attacks

SSRF (Server-Side Request Forgery) attacks can have significant impacts on web applications and the underlying infrastructure. Here are some potential consequences and impacts of SSRF attacks:

1. `Unauthorized Access to Internal Resources`: By exploiting an SSRF vulnerability, attackers can gain unauthorized access to internal resources, such as databases, APIs, or backend systems, that are typically inaccessible from external networks. This can lead to data breaches, manipulation of sensitive information, or unauthorized actions within the internal network.

2. `Data Exposure and Information Leakage`: SSRF attacks can result in the disclosure of sensitive information. Attackers can fetch and retrieve data from internal resources, potentially exposing confidential data, personally identifiable information (PII), or proprietary information to unauthorized parties.

3. `Network Scanning and Port Scanning`: In some SSRF attacks, attackers leverage the vulnerability to scan internal networks and discover open ports or services. This information can be used to identify potential entry points for further exploitation or to map the network for future attacks.

4. `Impact on Availability and Performance`: SSRF attacks can impact the availability and performance of the targeted server or application. Attackers can abuse SSRF to make excessive requests to external resources, leading to resource exhaustion, network congestion, or denial-of-service (DoS) conditions.

5. `Attack Pivoting and Lateral Movement`: Successful SSRF attacks can act as a stepping stone for attackers to pivot within the internal network. By accessing internal resources, they can move laterally to compromise other systems, escalate privileges, or launch subsequent attacks on critical infrastructure components.

6. `Cloud Environment Compromise`: In cloud environments, SSRF attacks can be particularly impactful. Attackers can abuse SSRF to access metadata services, retrieve sensitive information, and potentially compromise the entire cloud infrastructure, leading to the compromise of multiple interconnected services or instances.

7. `Reputation and Legal Consequences`: Organizations that fall victim to SSRF attacks can suffer reputational damage and loss of customer trust. Additionally, if the attack results in the exposure of personal or confidential data, it can lead to legal and regulatory consequences, such as violating data protection laws or industry compliance standards.

## OWASP Top 10

- OWASP 2021 - A10 > SSRF

## How to find SSRF Vulnerabilities

To find SSRF vulnerabilities, you can employ both black box and white box testing techniques. Here's how you can approach each method:

**Black Box Testing**:

1. `Input Fuzzing`: Start by identifying input parameters where URLs or IP addresses are accepted. Generate a variety of test cases with different values, including local IP addresses, loopback addresses, and external URLs. Monitor the application's behavior for any unexpected requests or responses that indicate potential SSRF vulnerabilities.

2. `Parameter Tampering`: Manipulate the input parameters to inject known SSRF payloads, such as "http://127.0.0.1" or "http://attacker.com". Observe the application's response for any signs of SSRF, such as requests to internal or unauthorized resources.

3. `URL Redirect Testing`: Test any features that involve URL redirection or follow-up requests. Inject URLs that redirect to external or internal resources and examine if the application follows the redirection and performs unintended requests.

4. `Out-of-Band (OOB) Testing`: Employ techniques like DNS resolution, HTTP callbacks, or email notifications to detect SSRF vulnerabilities that do not provide immediate responses. Insert payloads that trigger outbound communication and analyze if the server makes the expected external requests.

**White Box Testing**:

1. `Source Code Review`: Analyze the application's source code, paying specific attention to sections where HTTP requests are made. Look for unvalidated user inputs that are used to construct the requests. Check if input validation and proper URL sanitization mechanisms are in place to prevent SSRF.

2. `Static Analysis Tools`: Utilize static code analysis tools that can identify potential SSRF vulnerabilities by scanning the code for insecure input handling or suspicious HTTP request construction.

3. `Boundary Testing`: Determine the boundaries and constraints for URLs or IP addresses in the application. Perform tests with inputs near the boundaries to identify any weaknesses in input validation.

4. `Access Control and Whitelisting Review`: Review the application's access control mechanisms and whitelisting practices. Ensure that only authorized URLs or IP addresses are permitted for internal or external requests.

5. `Architecture Review`: Examine the network architecture to identify any potential SSRF-prone components, such as reverse proxies, load balancers, or internal services that interact with external resources. Assess their configuration and access controls to ensure proper security measures are in place.

Determine URL parser in various technologies to exploit SSRF

## How to exploit SSRF vulnerabilities

`Request` :

```http
POST /product/stock HTTP/1.0
Content-Type: application/x-www-
form-urlencoded
Content-Length: 118


stockApi=http://stock.weliketoshop.net:8080/product/stock/check%3FproductId%3D6%26storeId%3D1
```

`Response` :

```http
HTTP/1.1 200 OK
Content-Type: text/plain;
charset=utf-8
Connection: close
Content-Length: 3


506

```

Malicious Request / Response

`Request`:

```http
POST /product/stock HTTP/1.0
Content-Type: application/x-www-
form-urlencoded
Content-Length: 118


stockApi=http://localhost/admin
```

`Response` :

```http
Admin page
```

### Exploiting Regular SSRF

- If the application allows for user-supplied arbitrary URLs, try the following attacks:

  - Determine if a port number can be specified
  - If successful, attempt to port-scan the internal network using Burp Intruder
  - Attempt to connect to other services on the loopback address

- If the application does not allow for arbitrary user-supplied URLs, try to bypass defenses using the following techniques:
  - Use different encoding schemes
    - decimal-encoded version of 127.0.0.1 is 2130706433
    - 127.1 resolves to 127.0.0.1
    - Octal representation of 127.0.0.1 is 017700000001
  - Register a domain name that resolves to internal IP address(DNS Rebinding)
  - Use your own server that redirects to an internal IP address(HTTP Redirection)
  - Exploit inconsistencies in URL parsing
  - Videos link: https://www.youtube.com/watch?v=voTHFdL9S2k&ab_channel=BlackHat
  - Slide link: https://cheatsheetseries.owasp.org/assets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet_Orange_Tsai_Talk.pdf

### Exploiting Blind / Out-of-band

- If the application is vulnerable to blind SSRF, try to exploit the
  vulnerability using the following techniques: - Attempt to trigger an HTTP request to an external system you control and monitor the system for network interactions from the vulnerable server - Can be done using Burp Collaborator - If defenses are put in place, use the techniques mentioned in the previous slides to obfuscate the external malicious domain - Once you’ve proved that the application is vulnerable to blind SSRF, you need to determine what your end goal is - An example would be to probe for other vulnerabilities on the server itself or other backend systems

## How to prevent SSRF vulnerabilities

To prevent SSRF (Server-Side Request Forgery) vulnerabilities, you can implement several best practices and security measures. Here are some key steps to consider:

1. `Input Validation and Sanitization`: Implement strict input validation and sanitization techniques to ensure that user-supplied input is properly validated and sanitized. Validate the input parameters to ensure they conform to expected formats and consider using libraries or frameworks that provide built-in input validation mechanisms.

2. `Whitelisting and Strict URL/Domain Validation`: Maintain a whitelist of trusted and intended URLs or IP addresses. Validate and enforce strict URL or domain validation to ensure that only authorized and safe resources can be accessed.

3. `Implement Secure Request Libraries or APIs`: Utilize secure request libraries or APIs that have built-in protection against SSRF vulnerabilities. These libraries or APIs may include features like URL blacklisting, URL parsing, or built-in protection mechanisms against accessing internal resources.

4. `Network Segregation and Access Controls`: Implement proper network segregation by separating the web application server from critical internal resources. Utilize firewalls, network access controls, and proper network architecture to restrict access to sensitive systems and resources.

5. `Least Privilege Principle`: Apply the principle of least privilege to the web application server and associated components. Grant minimal permissions required for the server to perform its intended functions. Avoid providing unnecessary privileges that could be exploited in an SSRF attack.

6. `Secure Configuration and Hardening`: Ensure that servers, frameworks, and components are securely configured. Disable or restrict unnecessary functionality or features that could be abused for SSRF. Follow security best practices and guidelines provided by the relevant vendors or frameworks.

7. `Patch Management and Updates`: Regularly update and patch software, libraries, and frameworks used in the application. Keep track of security updates and promptly apply them to address any known vulnerabilities, including SSRF-related issues.

8. `Security Testing and Code Review`: Perform regular security testing, including penetration testing, vulnerability assessments, and code review, to identify and address SSRF vulnerabilities. Utilize both automated tools and manual testing techniques to detect potential SSRF flaws.

9. `Security Awareness and Training`: Educate developers, system administrators, and other stakeholders about SSRF risks, prevention techniques, and security best practices. Foster a security-conscious culture within the organization to prioritize security at all stages of development and deployment.
