# Kutay Cinar
# V00******

# CSC 361: Assingment 2

import sys
import struct

class GlobalHeader:

	magic_number = None		# uint32
	version_minor = None	# uint16
	version_major = None	# uint16
	thiszone = None			# int32
	sigfigs = None			# uint32
	snaplen = None			# uint32
	network = None			# uint32

	def __init__(self, buffer):
		self.magic_number, self.version_minor, self.version_major, self.thiszone, self.sigfigs, self.snaplen, self.network = struct.unpack('IHHiIII', buffer)

class PacketHeader:

	ts_sec = None			# uint32
	ts_usec = None			# uint32
	incl_len = None			# uint32
	orig_len = None			# uint32

	def __init__(self):
		self.ts_sec = 0
		self.ts_usec = 0
		self.incl_len = 0
		self. orig_len = 0

	def set_header(self, buffer):
		self.ts_sec, self.ts_usec, self.incl_len, self.orig_len = struct.unpack('IIII', buffer)

class IPV4Header:

	ihl = None				# int
	total_length = None		# int
	src_ip = None			# str
	dst_ip = None			# str

	def set_ihl(self, value):
		result = struct.unpack('B', value)[0]
		self.ihl = (result & 15) * 4

	def set_total_len(self, buffer):
		num1 = ((buffer[0] & 240) >> 4) * 16 * 16 * 16
		num2 = (buffer[0] & 15) * 16 * 16
		num3 = ((buffer[1] & 240) >> 4) * 16
		num4 = (buffer[1] & 15)
		self.total_length = num1 + num2 + num3 + num4
	
	def set_ip(self, buffer1, buffer2):
		src_addr = struct.unpack('BBBB', buffer1)
		dst_addr = struct.unpack('BBBB', buffer2)
		self.src_ip = str(src_addr[0]) + '.' + str(src_addr[1]) + '.' + str(src_addr[2]) + '.' + str(src_addr[3])
		self.dst_ip = str(dst_addr[0]) + '.' + str(dst_addr[1]) + '.' + str(dst_addr[2]) + '.' + str(dst_addr[3])
		
class TCPHeader:

	src_port = None			# int
	dst_port = None			# int
	seq_num = None			# int
	ack_num = None			# int
	data_offset = None		# int
	flags = None			# dict
	window_size = None		# int
	checksum = None			# int
	ugp = None				# int

	def __init__(self):
		self.src_port = 0
		self.dst_port = 0
		self.seq_num = 0
		self.ack_num = 0
		self.data_offset = 0
		self.flags = {}
		self.window_size =0
		self.checksum = 0
		self.ugp = 0

	def set_src_port(self, buffer):
		num1 = ((buffer[0] & 240) >> 4) * 16 * 16 * 16
		num2 = (buffer[0] & 15) * 16 * 16
		num3 = ((buffer[1] & 240) >> 4) * 16
		num4 = (buffer[1] & 15)
		self.src_port = num1 + num2 + num3 + num4
	
	def set_dst_port(self,buffer):
		num1 = ((buffer[0] & 240) >> 4) * 16 * 16 * 16
		num2 = (buffer[0] & 15) * 16 * 16
		num3 = ((buffer[1] & 240) >> 4) * 16
		num4 = (buffer[1] & 15)
		self.dst_port = num1 + num2 + num3 + num4

	def set_seq_num(self, buffer):
		self.seq_num = struct.unpack(">I", buffer)[0]

	def set_ack_num(self, buffer):
		self.ack_num = struct.unpack('>I', buffer)[0]

	def set_data_offset(self, buffer):
		value = struct.unpack("B", buffer)[0]
		self.data_offset = ((value & 240) >> 4) * 4

	def set_flags(self, buffer):
		value = struct.unpack("B", buffer)[0]
		self.flags["FIN"] = value & 1
		self.flags["SYN"] = (value & 2) >> 1
		self.flags["RST"] = (value & 4) >> 2
		self.flags["ACK"] = (value & 16) >> 4

	def set_window_size(self, buffer1, buffer2):
		buffer = buffer2 + buffer1
		self.window_size = struct.unpack('H', buffer)[0]
 
	def relative_seq_num(self, orig_num):
		if (self.seq_num >= orig_num):
			relative_seq = self.seq_num - orig_num
			self.seq_num = relative_seq

	def relative_ack_num(self, orig_num):
		if (self.ack_num >= orig_num):
			relative_ack = self.ack_num - orig_num + 1
			self.ack_num = relative_ack			

class Packet:

	header = None			# PacketHeader
	ipv4 = None				# IPV4Header
	tcp = None				# TCPHeader
	data = None				# byte
	payload = None			# int
	timestamp = None		# int

	def __init__(self):
		self.header = PacketHeader()
		self.ipv4 = IPV4Header()
		self.tcp = TCPHeader()
		self.data = b''
		self.payload = 0
		self.timestamp = 0

	def set_header(self, buffer):
		self.header.set_header(buffer)

	def set_data(self, buffer):
		self.data = buffer

	def set_number(self, value):
		self.number = value

	def set_rtt(self, p):
		rtt = p.timestamp - self.timestamp
		self.RTT_value = round(rtt, 8)

	def set_timestamp(self, orig_time):
		seconds = self.header.ts_sec
		microseconds = self.header.ts_usec
		self.timestamp = round(seconds + microseconds * 0.000001 - orig_time, 6)

	def set_ipv4(self):
		self.ipv4.set_ihl(self.data[14:15])
		self.ipv4.set_total_len(self.data[16:18])
		self.ipv4.set_ip(self.data[26:30], self.data[30:34])

	def set_tcp(self):
		offset = 14 + self.ipv4.ihl
		self.tcp.set_src_port(self.data[offset+0: offset+2])
		self.tcp.set_dst_port(self.data[offset+2: offset+4])
		self.tcp.set_seq_num(self.data[offset+4: offset+8])
		self.tcp.set_ack_num(self.data[offset+8: offset+12])
		self.tcp.set_data_offset(self.data[offset+12: offset+13])
		self.tcp.set_flags(self.data[offset+13: offset+14])
		self.tcp.set_window_size(self.data[offset+14: offset+15], self.data[offset+15: offset+16])

	def set_payload(self, payload):
		self.payload = payload


#############################################################
################ Parse Command Line Argument ################

# Get filename from command line
if len(sys.argv) != 2:
	print('Unexpected input. Usage: python3 TCPAnalyzer.py <sample_capture_file.cap>')
	exit()

# Set input filename from given argument
input_file = sys.argv[1]

# Open the given pcap file in the binary mode
f = open(input_file, 'rb')

#############################################################
#################### Read Global Header #####################

# Read the first 24 bytes to get the global header
global_header = GlobalHeader(f.read(24))

# Check magic_number to determine if same as that in the provided trace file
if global_header.magic_number != 2712847316:
	exit("ERROR: Given input file's magic number does not match.")

# As mentioned in Tutorial 5: you only need to follow the same magic number as that in the provided trace file

# Dictionary for storing connections
conn_dict = {} 
pcap_start_time = None

#############################################################
########## Parse Packets Headers and Packet Data) ###########
while True:

	# Read the next 16 bytes to get the packet header
	stream = f.read(16)

	# Terminate if reached end of file / empty byte
	if stream == b'':
		break

	# Create packet and parse header
	packet = Packet()
	packet.set_header(stream)

	# Check incl_len for the length of packet
	incl_len = packet.header.incl_len

	# Use relative time, i.e., the time with respect to the cap file
	if pcap_start_time is None:
		seconds = packet.header.ts_sec
		microseconds = packet.header.ts_usec
		pcap_start_time = round(seconds + microseconds * 0.000001, 6)
	
	# Read the next incl_len bytes for the packet data
	packet.set_data(f.read(incl_len))

	# Parse IPV4 header
	packet.set_ipv4()

	# Parse TCP header
	packet.set_tcp()

	# Payload and padding calculation
	payload = packet.header.incl_len - 14 - packet.ipv4.ihl - 20
	padding = packet.header.incl_len - packet.ipv4.total_length - 14
	
	if payload < 42:
		payload = 0

	packet.set_payload(payload+padding)

	# Hash the connection in a frozen set to be used as a key
	connection = frozenset([packet.ipv4.src_ip, packet.ipv4.dst_ip, packet.tcp.src_port, packet.tcp.dst_port])

	# If connection does not exist, create a key
	if connection not in conn_dict:
		conn_dict[connection] = []

	number = len(conn_dict[connection]) + 1
	packet.set_number(number)

	# Append packet to dictionary		
	conn_dict[connection].append(packet)

# end while

#############################################################
##################### Required Output #######################

tcp_total = len(conn_dict)

print('A) Total number of connections:', tcp_total)
print('______________________________________\n')

print('B) Connections\' details:\n')

# Initilize TCP stats
tcp_complete = []
tcp_packets = []
tcp_window_size = []
tcp_reset = 0

rtt = []

i = 1
for conn in conn_dict:
	
	# Initilize/reset first, last packet
	p_first = None
	p_last = None
	
	# Initilize/reset flag counters
	syn_count = 0
	fin_count = 0
	rst_count = 0

	# Initilize/reset lists for src and dst packets
	src_conn = []
	dst_conn = []
	
	print('Connection %d:' % i)
	
	# Iterate packets of connection
	for j in range(len(conn_dict[conn])):

		packet = conn_dict[conn][j]
		
		if packet.tcp.flags['SYN'] == 1:
			# The start time is the time when the first SYN is seen for this connection
			if p_first is None:
				p_first = packet
			syn_count += 1

		if packet.tcp.flags['FIN'] == 1:
			fin_count += 1
			#The end time is the time when the last FIN is seen for this connection
			p_last = packet
			
		if packet.tcp.flags['RST'] == 1:
			rst_count += 1

		packet.set_timestamp(pcap_start_time)

		# Put packets sent from source to destination or vice versa in their lists
		if packet.ipv4.src_ip == p_first.ipv4.src_ip:
			src_conn.append(packet)
		else:
			dst_conn.append(packet)

	# Print connection information
	print('Source Address:', p_first.ipv4.src_ip)
	print('Destination Address:', p_first.ipv4.dst_ip)
	print('Source Port:', p_first.tcp.src_port)
	print('Destination Port:', p_first.tcp.dst_port)
	print('Status: S%dF%d' % (syn_count, fin_count) )

	if rst_count != 0:
		tcp_reset += 1

	# (Only if the connection is complete provide the following information) 
	if p_last is not None:

		# Start, end time and duration calculation
		p_first.set_timestamp(pcap_start_time)
		p_last.set_timestamp(pcap_start_time)
		duration = p_last.timestamp - p_first.timestamp

		print('Start time:', p_first.timestamp, 'seconds')
		print('End time:', p_last.timestamp, 'seconds')
		print('Duration:', round(duration,6), 'seconds')
		
		# Append durations of complete tcp connections for part D
		tcp_complete.append(duration)

		# Packet numbers
		print('Number of packets sent from Source to Destination:', len(src_conn))
		print('Number of packets sent from Destination to Source:', len(dst_conn))
		print('Total number of packets:', (len(src_conn)+len(dst_conn)) )

		# Append packet numbers of complete tcp connections for part D
		tcp_packets.append(len(src_conn)+len(dst_conn))
		
		# Packet bytes
		src_bytes = 0
		dst_bytes = 0

		for k in range(len(src_conn)):
			src_bytes += src_conn[k].payload

		for k in range(len(dst_conn)):
			dst_bytes += dst_conn[k].payload

		print('Number of data bytes sent from Source to Destination:', src_bytes, 'bytes')
		print('Number of data bytes sent from Destination to Source:', dst_bytes, 'bytes')
		print('Total number of data bytes:', (src_bytes + dst_bytes), 'bytes')

		# Append window sizes of complete tcp connections for part D
		for l in range(len(conn_dict[conn])):
			tcp_window_size.append(conn_dict[conn][l].tcp.window_size)

		# RTT Calculation
		for p1 in src_conn:
			for p2 in dst_conn:
				# Handshake calculation
				if p1.tcp.seq_num + p1.tcp.flags['SYN'] == p2.tcp.ack_num and p1.timestamp < p2.timestamp:
					rtt.append(p2.timestamp - p1.timestamp)
					break
				# Endshake calculation
				if p1.tcp.seq_num + p1.tcp.flags['FIN'] == p2.tcp.ack_num and p1.timestamp < p2.timestamp:
					rtt.append(p2.timestamp - p1.timestamp)
					break
				# General calculation
				if p1.tcp.seq_num + p1.payload == p2.tcp.ack_num and p1.timestamp < p2.timestamp:
					rtt.append(p2.timestamp - p1.timestamp)
					break


	print('END ')
	print('+++++++++++++++++++++++++++++++++')

	i = i + 1
	
# end for loop

print('______________________________________\n')

print('C) General:\n')

print('Total number of complete TCP connections:', len(tcp_complete))
print('Number of reset TCP connections:', tcp_reset)
print('Number of TCP connections that were still open when the trace capture ended:', tcp_total - len(tcp_complete))

print('______________________________________\n')

print('D) Complete TCP connections:\n')

print('Minimum time duration:', round(min(tcp_complete), 6), 'seconds')
print('Mean time duration:', round(sum(tcp_complete) / len(tcp_complete), 6), 'seconds')
print('Maximum time duration:', round(max(tcp_complete), 6), 'seconds')

print()

print('Minimum RTT value:', round(min(rtt),6), 'seconds')
print('Mean RTT value:', round(sum(rtt)/len(rtt),6), 'seconds')
print('Maximum RTT value:', round(max(rtt),6), 'seconds')

print()

print('Minimum number of packets including both send/received:', round(min(tcp_packets), 6))
print('Mean number of packets including both send/received:', round(sum(tcp_packets) / len(tcp_packets), 6))
print('Maximum number of packets including both send/received:', round(max(tcp_packets), 6))

print()

print('Minimum number of window size including both send/received:', round(min(tcp_window_size), 6))
print('Mean number of window size including both send/received:', round(sum(tcp_window_size) / len(tcp_window_size), 6))
print('Maximum number of window size including both send/received:', round(max(tcp_window_size), 6))

print('______________________________________\n')

# End of program