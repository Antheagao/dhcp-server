from socket import *

def main():
	# Declare variables
	MAX_BYTES = 1024
	DHCP_SERVER = ('', 67)
	DHCP_CLIENT = ('255.255.255.255', 68)
	ip_list = []
	xid = []
	hardware_address = []
	
	# Create a UDP socket
	s = socket(AF_INET, SOCK_DGRAM)
	print("Setting up server...")

	# Allow socket to broadcast messages
	s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

	# Bind socket to the well-known port reserved for DHCP servers
	s.bind(DHCP_SERVER)
	print("Server is listening...")
	print('======================================================')

	# Create a list of available ip addresses
	ip_list = create_ip_address()

	# Create an offer for each client
	while 1:
		# Recieve a UDP message for DHCP discovery
		msg, addr = s.recvfrom(MAX_BYTES)
		print("Received DHCP Discover!!!")

		# Get the client MAC address and print it
		print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
		hardware_address.append(msg[28])
		for i in range(29, 34):
			print(":" + format(msg[i], 'x'), end = '')
			hardware_address.append(msg[i])
		print()

		# Get the client XID and print it
		print("Client's XID is " + format(msg[7], 'x'), end = '')
		xid.append(msg[7])
		for index in range(6, 3, -1):
			print("." + format(msg[index], 'x'), end = '')
			xid.append(msg[index])
		print()
		xid.reverse()

		# Send a UDP message for DHCP Offer
		msg = dhcp_offer(xid, hardware_address)
		xid = []
		hardware_address = []
		print("Sending DHCP Offer...")
		print('======================================================')
		s.sendto(msg, DHCP_CLIENT)

		# Create an acknowledgement for each client
		while 1:
			# Recieve a UDP message for DHCP Request
			msg, addr = s.recvfrom(MAX_BYTES)
			print("Received DHCP Request!!!")

			# Get the client MAC address and print it
			print("Client's MAC Address is " + format(msg[28], 'x'), end = '')
			hardware_address.append(msg[28])
			for i in range(29, 34):
				print(":" + format(msg[i], 'x'), end = '')
				hardware_address.append(msg[i])
			print()
			
			# Get the client XID and print it
			print("Client's XID is " + format(msg[7], 'x'), end = '')
			xid.append(msg[7])
			for index in range(6, 3, -1):
				print("." + format(msg[index], 'x'), end = '')
				xid.append(msg[index])
			print()
			xid.reverse()

			# Send a UDP message for DHCP Acknowledge
			msg = dhcp_ack(xid, hardware_address)
			xid = []
			hardware_address = []
			print("Sending DHCP Acknowledge...")
			print('======================================================')
			s.sendto(msg, DHCP_CLIENT)
			

# Function to create list of ip addresses as bytes
def create_ip_address():
	# Declare variables
	NUM_ADDRESSES = 48
	ip_string_list = []
	ip_byte_list = []
	subnet = 0
	subnet_count = 0
	user = 2

	# Create list of string ip addresses matching subnets
	for index in range(0, NUM_ADDRESSES):
		ip_string_list.append('192.168.' + str(subnet) + '.' + str(user))
		user += 1
		subnet_count += 1
		
		# Increment the subnet number and reset the user amount
		if (subnet_count % 8 == 0):
			subnet += 1
			subnet_count = 0
			user = 2
	
	# Convert string ip addresses to 32-byte addresses
	for index in ip_string_list:
		ip_byte_list.append(bytes(map(int, index.split('.'))))

	# Return the ip addresses
	return ip_byte_list


# Function to print byte ip addresses in string form
def print_ip(ip_list):
	for index in ip_list:
		#print('.'.join(f'{c}' for c in index))
		print('.'.join(str(c) for c in index))


def dhcp_offer(xid, hardware_address):
	# Create a DHCP offer message
	OP = bytes([0x02])
	HTYPE = bytes([0x01])
	HLEN = bytes([0x06])
	HOPS = bytes([0x00])
	XID = bytes(xid)
	SECS = bytes([0x00, 0x00])
	FLAGS = bytes([0x00, 0x00])

	# Client IP Address 
	CIADDR = bytes([0x00, 0x00, 0x00, 0x00])

	# 192.168.1.100 : Your IP address (IP being offered) *Changed*
	YIADDR = bytes([0xC0, 0xA8, 0x00, 0x02])

	# 192.168.0.1 : Server IP address *Changed*
	SIADDR = bytes([0xC0, 0xA8, 0x00, 0x01])

	# Gateway IP address
	GIADDR = bytes([0x00, 0x00, 0x00, 0x00])

	# Client Hardware Address *Changed*
	CHADDR1 = bytes([hardware_address[0]] + [hardware_address[1]] +\
		 			[hardware_address[2]] + [hardware_address[3]]) 
	CHADDR2 = bytes([hardware_address[4]] + [hardware_address[5]] +\
					[0x00, 0x00])
	CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
	CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
	CHADDR5 = bytes(192)

	# Magic Cookie
	Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])

	# DHCP Offer
	DHCPOptions1 = bytes([53, 1, 2])

	# 255.255.255.0 : Subnet Mask
	DHCPOptions2 = bytes([1, 4, 0xFF, 0xFF, 0xFF, 0x00])

	# 192.168.0.1 : Router IP *Changed*
	DHCPOptions3 = bytes([3, 4, 0xC0, 0xA8, 0x00, 0x01])
	
	# 86400s(1 day) : IP address lease time
	DHCPOptions4 = bytes([51, 4, 0x00, 0x01, 0x51, 0x80])

	# DHCP Server *Changed*
	DHCPOptions5 = bytes([54, 4, 0xC0, 0xA8, 0x00, 0x01])

	# Put the message together and send it to the client
	offer = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR + YIADDR\
				 + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4\
				 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2\
				 + DHCPOptions3 + DHCPOptions4 + DHCPOptions5

	return offer


def dhcp_ack(xid, hardware_address):
	# Create DHCP ack message
	OP = bytes([0x01])		# Changed
	HTYPE = bytes([0x01])
	HLEN = bytes([0x06])
	HOPS = bytes([0x00])
	XID = bytes(xid)
	SECS = bytes([0x00, 0x00])
	FLAGS = bytes([0x00, 0x00])

	# Client IP Address 
	CIADDR = bytes([0x00, 0x00, 0x00, 0x00])

	# 192.168.1.100 : Your IP address (IP being offered) *Changed*
	YIADDR = bytes([0xC0, 0xA8, 0x00, 0x02])

	# 192.168.0.1 : Server IP address *Changed*
	SIADDR = bytes([0xC0, 0xA8, 0x00, 0x01])

	# Gateway IP address
	GIADDR = bytes([0x00, 0x00, 0x00, 0x00])

	# Client Hardware Address *Changed*
	CHADDR1 = bytes([hardware_address[0]] + [hardware_address[1]] +\
		 			[hardware_address[2]] + [hardware_address[3]]) 
	CHADDR2 = bytes([hardware_address[4]] + [hardware_address[5]] +\
					[0x00, 0x00])
	CHADDR3 = bytes([0x00, 0x00, 0x00, 0x00]) 
	CHADDR4 = bytes([0x00, 0x00, 0x00, 0x00]) 
	CHADDR5 = bytes(192)

	# Magic Cookie
	Magiccookie = bytes([0x63, 0x82, 0x53, 0x63])

	# DHCP Ack
	DHCPOptions1 = bytes([53, 1, 5])

	# 255.255.255.0 : Subnet Mask
	DHCPOptions2 = bytes([1, 4, 0xFF, 0xFF, 0xFF, 0x00])

	# 192.168.0.1 : Router IP *Changed*
	DHCPOptions3 = bytes([3, 4, 0xC0, 0xA8, 0x00, 0x01])
	
	# 86400s(1 day) : IP address lease time
	DHCPOptions4 = bytes([51, 4, 0x00, 0x01, 0x51, 0x80])

	# DHCP Server *Changed*
	DHCPOptions5 = bytes([54, 4, 0xC0, 0xA8, 0x00, 0x01])

	# Put the message together and send it to the client
	ack = OP + HTYPE + HLEN + HOPS + XID + SECS + FLAGS + CIADDR + YIADDR\
				 + SIADDR + GIADDR + CHADDR1 + CHADDR2 + CHADDR3 + CHADDR4\
				 + CHADDR5 + Magiccookie + DHCPOptions1 + DHCPOptions2\
				 + DHCPOptions3 + DHCPOptions4 + DHCPOptions5

	return ack

main()