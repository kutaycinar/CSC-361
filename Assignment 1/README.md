# SmartClient.py

The project is to build a tool at web client to collect information regarding a web server. The purpose of this project is two fold:
- Hands-on experience with socket programming in Python,
- Understand the application-layer protocols HTTP/HTTPs

Given the URL of a web server, SmartClient.py finds out the following information regarding the web server:
1. whether or not the web server supports HTTPs,
2. whether or not the web server supports http1.1
3. whether or not the web server supports http2,
4. the cookie name, the expire time (if any), and the domain name (in any) of cookies that the web server will use.

Run by executing the following command:
```
python SmartClient.py <url>
```

As an example output, after running the program with www.uvic.ca:
```
website: www.uvic.ca
1. Supports of HTTPS: yes
2. Supports HTTP 1.1: yes
3. Supports HTTP 2.0: no
4. List of Cookies:

cookie name: PHPSESSID
cookie name: uvic_bar, expires time: Thu, 01-Jan-1970 00:00:01 GMT, domain name: .uvic.ca
cookie name: www_def
cookie name: TS0168706e, domain name: .www.uvic.ca
```
