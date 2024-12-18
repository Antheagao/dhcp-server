from socket import *

MAX_BYTES = 1024
DHCP_SERVER = ('', 67)
DHCP_CLIENT = ('255.255.255.255', 68)

# Create a UDP socket
s = socket(AF_INET, SOCK_DGRAM)

# Allow socket to broadcast messages
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

# Bind socket to the well-known port reserved for DHCP servers
s.bind(DHCP_SERVER)

print("Server is listening")
# Recieve a UDP message
msg, addr = s.recvfrom(1024)

# Print the client's MAC Address from the DHCP header
print("Client's MAC Address is " + format(msg[28], 'x'), end = '')

for i in range(29, 34):
	print(":" + format(msg[i], 'x'), end = '')
print()

# Send a UDP message (Broadcast)
s.sendto(b'Hello World!', DHCP_CLIENT)



def create_addresses():
	# Declare variables
	num_addresses = 20
	address_string_list = []
	address_byte_list = []

	# Create list of string ip addresses matching subnet
	for index in range(2, num_addresses + 1):
		address_string_list.append('192.168.0.' + str(index))
	
	# Convert string ip addresses to 32-byte addresses
	for index in address_string_list:
		address_byte_list.append(socket.inet_aton(address_string_list[index]))

	# Return the ip addresses
	return address_byte_list

"""def make_address():
	print("Creating an IP address...")
	ip = '192.168.1.1'
	ip_as_bytes = bytes(map(int, ip.split('.')))
	print("IP in byte form: " + str(ip_as_bytes))
	return ip_as_bytes"""

#ip = '192.168.1.1'
		#msg = bytes(map(int, ip.split('.')))

'''for i in range(28, 34):
			print(msg[i])'''

'''print(msg)'''
'''print(addr)'''

'''count = 0
for i in msg:
	print(i, " ===> ", count)
	count += 1'''

"""print_ip(ip_list)"""

#global MAX_BYTES
#global DHCP_SERVER
#global DHCP_CLIENT
#global s