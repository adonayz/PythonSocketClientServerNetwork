Adonay Resom (azresom@wpi.edu)



DESCRIPTION OF FILES/PROGRAMS

Programs are written in Python 2.7
	- http_client.py
	- http_server.py

The server uses the host name 'localhost'

http_client.py
	To run this program use command line in the followings format:
		python http_client.py [--ttl] server_url port_number
			*Hint* -ttl is optional (used to print RTT value)
	
	For example if you want to fetch the homepage of bbc.com you can use
		python http_client.py bbc.com 80
			*Hint* remember to use port 80 for http sites

http_server.py
	To run this program use command line in the followings format:
		python http_server.py port_number
			*Hint* it is preferable if you use a number above 5000 (7000 used for tests)
	
	If you want to access files from the server using a web browser fo the following url format
		http://localhost:port_number/file_path

If you want to fetch a file from the server created by http_server.py useing http_client.py use
		python http_server.py 7000
		python http_client.py localhost/file_path 7000