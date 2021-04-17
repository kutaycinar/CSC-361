# Kutay Cinar
# V00******

# CSC 361: Assingment 1

import sys
import socket
import ssl
import re

#############################################################
################ Parse Command Line Argument ################

# Set socket default timeout to 10
socket.setdefaulttimeout(10) 

# Get URI from command line
if len(sys.argv) != 2:
	print('Unexpected input. Usage: python3 SmartClient.py www.uvic.ca')
	exit()

# Set hostname from given argument
hostname = sys.argv[1]

#############################################################
################ Checking HTTPS and HTTP 2.0 ################

# Set context variables to check for H2
context = ssl.create_default_context()
context.set_alpn_protocols(["h2"])

# Create socket and wrap socket with SSL
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock = context.wrap_socket(sock, server_hostname=hostname)

try:
	sock.connect((hostname, 443))

	# Connection established, therefore, HTTPS must be enabled
	https = True

	# Check if H2 is set and assign h2
	if sock.selected_alpn_protocol() == 'h2':
		h2 = True
	else:
		h2 = False

	sock.close() # close connection

except Exception as e:
	# Unable to create SSL connection, no HTTPS 
	https = False
	# If HTTPS is not enabled, HTTP2 cannot exist
	h2 = False


#############################################################
############# Check HTTP 1.1 with/without SSL ###############
if https is True:

	# Set context variables
	context = ssl.create_default_context()
	context.set_alpn_protocols(["http/1.1", "http/1.0"])

	# Create SSL connection
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock = context.wrap_socket(sock, server_hostname=hostname)
	
	try:
		sock.connect((hostname, 443))
	except:
		exit('Cannot connect to given URI')

else:
	# Otherwise, create non SSL connection
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	try:
		sock.connect((hostname, 80))
	except:
		exit('Cannot connect to given URI')

#############################################################
########## Get a HTTP response to check Cookies #############

# Set HTTP 1.1 as false by default
h1 = False

# Check if site has a redirect by sending a test 1.1 request
request =  'GET / HTTP/1.1\r\nHost: ' + hostname + '\r\n\r\n'

try:
	sock.send(request.encode())
	response = sock.recv(10000).decode('utf-8', 'ignore')
except Exception as e:
	exit(e)

# If there's a new location for the website, find and use it
if re.search("HTTP/1.\d 30\d", response):

	location = re.search("Location: https?://(.*?)/", response, re.IGNORECASE)

	if location is not None:

		hostname = location[1]

		sock.close() # close previous connection

		# Re-establish connections with new hostname depending on HTTPS
		if https is True:

			# EDGE CASE: Connect securely first to check H2 with new alias
			context = ssl.create_default_context()
			context.set_alpn_protocols(["h2"])

			# Create SSL connection
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock = context.wrap_socket(sock, server_hostname=hostname)
			
			try:
				sock.connect((hostname, 443))

				# Set HTTP 2 true if selected protol is correct
				if sock.selected_alpn_protocol() == 'h2':
					h2 = True
			except:
				# If a exception, HTTP 2 must be false
				h2 = False

			sock.close() # close connection

			# EDGE CASE: Connect securely again to check H1 with new alias
			context = ssl.create_default_context()
			context.set_alpn_protocols(["http/1.1", "http/1.0"])
			
			# Create SSL connection
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			sock = context.wrap_socket(sock, server_hostname=hostname)
			
			try:
				sock.connect((hostname, 443))
			except:
				exit('Cannot connect to given URI')

			# Set HTTP 1.1 true if selected protol is correct
			if sock.selected_alpn_protocol() == 'http/1.1':
				h1 = True

		else:
			# Otherwise, connect un-securely to alias
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

			try:
				sock.connect((hostname, 80))
			except:
				exit('Cannot connect to given URI')

		# Send a new HTTP 1.1 request and get response for cookies
		request =  'GET /test.html HTTP/1.0\r\nHost: ' + hostname + '\r\n\r\n'

		sock.send(request.encode())
		response = sock.recv(10000).decode('utf-8', 'ignore')

# If HTTP 1.1 flag was not changed previously, regex parse the response
if h1 is False:

	# Check if HTTP 1.1 is supported
	if re.search("HTTP.1.1", response, re.IGNORECASE):
		h1 = True

	else:
		# HTTP 1.1 does not exist
		h1 = False

		# In this case, create a request from HTTP 1.0 to parse for cookies
		request =  'GET / HTTP/1.0\r\nHost: ' + hostname + '\r\n\r\n'
		sock.send(request.encode())

		response = sock.recv(10000).decode('utf-8', 'ignore')
	
sock.close() # close connection

#############################################################
##################### Required Output #######################

# Helper function to print output
def yesNo(boolean):
	if boolean:
		return "yes"
	else:
		return "no"

print('website: ' + hostname)
print('1. Supports of HTTPS: ' + yesNo(https))
print('2. Supports HTTP 1.1: ' + yesNo(h1))
print('3. Supports HTTP 2.0: ' + yesNo(h2))
print('4. List of Cookies: ')
print()

#############################################################
####################### Check Cookies #######################

cookies = re.findall("Set-Cookie: (.+)", response, re.IGNORECASE)

# If there are cookies, then iterate them
if(cookies):

	for cookie in cookies:

		# Set cookie name
		name = re.search("(.*?)[=;]", cookie)
		if name:
			name = name.group(1)
		else:
			name = ""

		# Set expire time
		expire = re.search("expires=(.*?);", cookie, re.IGNORECASE)
		if expire:
			expire = ", expires time: " + expire.group(1)
		else:
			expire = ""

		# Set domain name
		domain = re.search("domain=(.*?);", cookie, re.IGNORECASE)
		if domain:
			domain = ", domain name: " + domain.group(1)
		else:
			domain = ""

		# Print cookie details
		print("cookie name: " + name + expire + domain)
   
else:
	# Otherwise, there are no cookies
	print("no cookies.")

# End of program