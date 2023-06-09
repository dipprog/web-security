# Directory Traversal

## What is directory traversal

Directory traversal, also known as path traversal or directory climbing, is a security vulnerability that allows an attacker to access files and directories outside of the intended scope of a web application or file system. It occurs when an application does not properly validate and sanitize user input, allowing the attacker to manipulate file paths and navigate to directories they shouldn't have access to.

The vulnerability typically arises when an application takes user-supplied input (such as file names, URLs, or parameters) and uses it directly or indirectly to construct file paths or execute file operations. If the application fails to adequately validate and sanitize the input, an attacker can craft a malicious input that includes special characters or sequences to "break out" of the intended directory structure.

For example, let's say there is a web application that allows users to download files. The application may construct the file path based on user input, like this:

```
http://example.com/download?file=user-supplied-input
```

If the application does not properly validate and sanitize the user-supplied input, an attacker can submit a manipulated input like "../secrets/confidential.txt" to traverse out of the intended directory and access sensitive files:

```
http://example.com/download?file=../secrets/confidential.txt
```

If the application blindly uses this input to construct the file path without verification, it could end up serving the confidential file to the attacker.

## Impact of directory traversal vulnerabilities

Directory traversal vulnerabilities can have significant impacts on the security and integrity of a system. Here are some potential consequences of such vulnerabilities:

1. `Unauthorized access to sensitive files`: An attacker can use directory traversal to access files outside of the intended directory. This can lead to the exposure of sensitive information such as configuration files, user databases, password files, or any other files containing confidential data.

2. `Data manipulation and deletion`: Once an attacker gains access to sensitive files, they can modify, delete, or overwrite the contents of those files. This can result in data corruption, loss of critical information, or unauthorized modifications to the system.

3. `Remote code execution`: In some cases, directory traversal vulnerabilities can be combined with other types of attacks, such as file inclusion vulnerabilities. This combination may allow an attacker to execute arbitrary code on the server, potentially leading to complete compromise of the system.

4. `Application and system compromise`: Exploiting directory traversal vulnerabilities can provide attackers with a foothold in the system, allowing them to escalate their privileges, pivot to other attack vectors, or launch further attacks on the infrastructure or other systems within the network.

5. `Privacy breaches and regulatory non-compliance`: If the compromised files contain personally identifiable information (PII) or other sensitive data, the organization may face legal and regulatory consequences, as well as damage to its reputation.

6. `Denial of service (DoS)`: An attacker could potentially use directory traversal to access and exhaust system resources, leading to a denial of service condition where the application or server becomes unresponsive or crashes.

## How to find directory traversal vulnerabilities

Finding directory traversal vulnerabilities requires a combination of black box and white box testing techniques. Let's explore how these approaches can be applied:

1. `Black Box Testing`:
   Black box testing involves testing the application from an external perspective without knowledge of its internal workings. Here are some techniques to discover directory traversal vulnerabilities in black box testing:

   a. `Input Fuzzing`: Submit various inputs, including special characters and sequences, to test how the application handles them. Look for any unexpected behavior or error messages that might indicate a directory traversal vulnerability.

   b. `Boundary Testing`: Test the application by providing inputs that go beyond expected boundaries, such as long file paths, nested directories, or excessive "../" sequences. Observe how the application responds and check if it allows access to unintended directories.

   c. `Directory Enumeration`: Try to enumerate directories and files within the application by using common directory and file names, such as "/etc/passwd" or "../etc/passwd". If the application discloses sensitive information or responds differently for valid and invalid paths, it might indicate a vulnerability.

   d. `Automated Scanners`: Utilize security testing tools, such as web vulnerability scanners, that include directory traversal checks. These tools can automatically crawl the application, injecting malicious inputs to identify potential vulnerabilities.

2. `White Box Testing`:
   White box testing involves having access to the application's internal structure and source code. This allows for a more detailed analysis of the application's security. Here are some techniques for finding directory traversal vulnerabilities in white box testing:

   a. `Code Review`: Analyze the source code and look for areas where user-supplied input is used to construct file paths or perform file operations. Check if the input is properly validated, sanitized, and restricted to a specific directory structure. Look for potential code patterns that may introduce directory traversal vulnerabilities.

   b. `Static Analysis Tools`: Utilize static analysis tools that can scan the source code and identify potential vulnerabilities, including directory traversal issues. These tools can help detect insecure coding practices, improper input handling, and other security weaknesses.

   c. `Boundary Checking`: Review how the application handles boundary cases, such as file path length limits, character restrictions, or input validations. Look for any inconsistencies or gaps that might allow directory traversal attacks.

   d. `Access Control Analysis`: Verify if the application enforces proper access controls and permissions for file operations. Ensure that user input is not directly used to access or retrieve files without appropriate validation and authorization checks.

## Exploting directory traversal

- Regular case

```
../../../../../../etc/passwd
```

```
.\..\..\...\..\..\windows\win.ini
```

- Absolute paths

```
/etc/passwd
```

- Traversal sequences stripped non-recursively

```
....//....//....//etc/passwd
```

- Bypass traversal sequence stripped defense using url encoding - single encoding or double encoding

- Bypass start of path validation

```
/var/www/images/../../../etc/passwd
```

- Bypass file extension validation using **null** byte. Ignore anything after the null byte. Doesn't work for all frameworka and language.

```
../../../etc/passwd%00.png
```

## Preventing directory traversal

Preventing directory traversal vulnerabilities is essential to ensure the security of an application or system. Here are some best practices to help prevent directory traversal attacks:

1. Input Validation and Sanitization:

   - Implement strict input validation to ensure that user-supplied input is properly formatted and conforms to expected patterns.
   - Sanitize user input to remove or escape any special characters or sequences that could be used to navigate out of the intended directory structure.
   - Use robust input validation libraries or frameworks that provide built-in protection against directory traversal attacks.

2. Use Whitelisting:

   - Employ a whitelist approach to validate user input against an approved set of characters, directory names, or allowed paths. Reject any input that does not adhere to the whitelist.
   - Avoid using blacklisting techniques, as they can be error-prone and may not cover all possible attack vectors.

3. Avoid Direct User Input in File Operations:

   - Do not use user-supplied input directly in file operations, such as reading, writing, or deleting files. Instead, use a secure file access mechanism that maps user input to the intended file paths.

4. Apply Proper Access Controls:

   - Enforce strong access controls and permissions to restrict user access to authorized directories and files. Only allow users to access the files and directories they genuinely need.

5. Implement File Path Canonicalization:

   - Normalize and canonicalize file paths to eliminate any redundant or non-standard elements, such as excessive "../" sequences or symbolic links. This helps ensure that the file paths are resolved accurately and prevent directory traversal.

6. Use Secure File System APIs:

   - Utilize secure file system APIs or libraries that handle file operations securely, mitigating directory traversal vulnerabilities automatically. These APIs may provide features like path validation, sandboxing, and restricted access to the file system.

7. Keep Software and Libraries Up-to-Date:

   - Regularly update and patch your application's software components, frameworks, and libraries. This helps ensure that any known vulnerabilities related to directory traversal or other security issues are addressed.

8. Security Testing and Code Reviews:
   - Conduct regular security testing, including penetration testing and vulnerability assessments, to identify and remediate any directory traversal vulnerabilities.
   - Perform thorough code reviews to detect insecure coding practices and potential security weaknesses that may lead to directory traversal vulnerabilities.
