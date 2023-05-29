## The table below breaks down the cipher suite string above into what is preferred in order (best key exchange algorithm/strongest encryption first).

| Order |	Key Exchange Algorithm |	Authentication Algorithm |	Bulk Encryption Algorithm |	Mac Algorithm |
|-------|------------------------|---------------------------|----------------------------|---------------|
|#1	|	Elliptic Curve Diffie–Hellman (ECDH)|Elliptic Curve Digital Signature Algorithm (ECDSA)|AES 256 in Galois Counter Mode (AES256-GCM)|SHA384|
|#2 |	Elliptic Curve Diffie–Hellman (ECDH)|RSA|AES 256 in Galois Counter Mode (AES256-GCM)|SHA384|
|#3	|	Elliptic Curve Diffie–Hellman (ECDH)|Elliptic Curve Digital Signature Algorithm (ECDSA)|ChaCha20 (CHACHA20)|POLY1305SHA256|
|#4	|	Elliptic Curve Diffie–Hellman (ECDH)|RSA|ChaCha20 (CHACHA20)|POLY1305SHA256|
|#5	|	Elliptic Curve Diffie–Hellman (ECDH)|Elliptic Curve Digital Signature Algorithm (ECDSA)|AES 128 in Galois Counter Mode (AES128-GCM)|SHA256|
|#6	|	Elliptic Curve Diffie–Hellman (ECDH)|RSA|AES 128 in Galois Counter Mode (AES128-GCM)|SHA256|
