# Proxy-Server
### By Amy Reichhold

## How to run Proxy-Server
On the command line, run the following command:
```
python3 proxy_server.py localhost 8888
```
Then, use a Web browser to visit this URL:
```
localhost:8888/www.google.com
```

The proxy server will fetch `www.google.com` and display the page. Note that 
the address bar continues to show that the browser is displaying 
`localhost:8888/www.google.com`, rather than directly loading 
`www.google.com`. The page may take longer to load than when accessing 
`www.google.com` directly, because the proxy server takes time to access all 
related media associated with the page (images, for example).

## Overview and Goal of Project
Everybody loves browsing the Internet, but few fully understand the technical 
processes behind it. Key considerations include identifying a resource to 
connect to, establishing that connection, and ultimately requesting and 
receiving data from the resource. The Proxy Server serves as a practical 
exercise that encompasses all these elements:

1. The Proxy Server is run using a well-known IP address and port for 
   identification.
2. It behaves as a server initially and accepts connections from HTTP clients 
   to its IP address.
3. In the connection process, the HTTP client sends a request for a resource 
   in the form of a Uniform Resource Locator (URL).
4. The Proxy Server then behaves as a client and connects to the resource 
   specified by the URL.
5. It receives data from the resource and relays it back to the HTTP client.

The resulting application provides a simple yet effective base for further 
endeavors related to the technologies used by the Proxy Server, namely sockets, 
client and server roles, Transmission Control Protocol (TCP), 
Internet Protocol (IP), HTTP headers, and data buffers.
 
### Future Work
This project started as a school assignment and thus exhibits simple operation: 
the Proxy Server accepts a request for a domain name only (without a specific 
path within the domain), retrieves data from the domain, and forwards it to 
the requesting client. The Proxy Server could be extended to allow requests 
for arbitrary URLs, making it more usable in practice.

Currently, the Proxy Server requests each supplementary resource related to a 
given web page (e.g., images and stylesheets) sequentially and perhaps with a 
conservative buffer size. This results in lower-than-expected performance when 
loading a web page via the Proxy Server. Performance could be improved by 
adding support for multiple threads or processes, or by allowing adjustments 
to the buffer size.

Finally, the Proxy Server has limited practical usefulness if it simply 
forwards requests from a client and relays the subsequent data back, as the 
client is probably better off without such an intermediary. The Proxy Server 
could be made more useful by modifying it to avoid loading advertisements, 
tracking cookies, privacy policy notices, or other common annoyances on the 
web.
