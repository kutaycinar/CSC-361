# Kutay Cinar
# V00******

# CSC 361: Assingment 3

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
	identification = None	# int
	flags = None			# int
	fragment_offset = None	# int
	ttl = None				# int
	protocol = None			# int
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

	def set_identification(self, buffer):
		result = struct.unpack('BB', buffer)
		self.identification = int(str(hex(result[0])) + str(hex(result[1]))[2:], 16)

	def set_fragment_offset(self, buffer):
		num0 = hex(((buffer[0] & 224) >> 5))
		num1 = ((buffer[0] & 16) >> 4) * 16 * 16 * 16
		num2 = (buffer[0] & 15) * 16 * 16
		num3 = ((buffer[1] & 240) >> 4) * 16
		num4 = (buffer[1] & 15)
		self.flags = num0
		self.fragment_offset = (num1 + num2 + num3 + num4) * 8

	def set_ttl(self, buffer):
		self.ttl = struct.unpack('B', buffer)[0]

	def set_protocol(self, buffer):
		self.protocol = struct.unpack('B', buffer)[0]
		
class UDPHeader:
	
	src_port = None
	dst_port = None
	udp_length = None
	checksum = None

	def set_src_port(self, buffer):
		result = struct.unpack('BB', buffer)
		self.src_port = int(str(hex(result[0])) + str(hex(result[1]))[2:], 16)

	def set_dst_port(self, buffer):
		result = struct.unpack('BB', buffer)
		self.dst_port = int(str(hex(result[0])) + str(hex(result[1]))[2:], 16)

	def set_udp_len(self, buffer):
		result = struct.unpack('BB', buffer)
		self.udp_length = int(str(hex(result[0])) + str(hex(result[1]))[2:], 16)

	def set_checksum(self, buffer):
		result = struct.unpack('BB', buffer)
		self.checksum = str(hex(result[0])) + str(hex(result[1]))
		
class ICMPHeader:

	type_num = None
	code = None
	src_port = None
	dst_port = None
	sequence = None

	def set_type(self, buffer):
		result = struct.unpack('B', buffer)[0]
		self.type_num = int(result)

	def set_code(self, buffer):
		result = struct.unpack('B', buffer)[0]
		self.code = int(result)

	def set_src_port(self, buffer):
		result = struct.unpack('BB', buffer)
		self.src_port = int(str(hex(result[0])) + str(hex(result[1]))[2:], 16)

	def set_dst_port(self, buffer):
		result = struct.unpack('BB', buffer)
		self.dst_port = int(str(hex(result[0])) + str(hex(result[1]))[2:], 16)

	def set_sequence(self, buffer):
		result = struct.unpack('BB', buffer)
		self.sequence = int(str(hex(result[0])) + str(hex(result[1]))[2:], 16)

class Packet:

	header = None			# PacketHeader
	ipv4 = None				# IPV4Header
	icmp = None				# ICMPHeader
	udp = None				# UDPHeader
	data = None				# byte
	payload = None			# int
	timestamp = None		# int

	def __init__(self):
		self.header = PacketHeader()
		self.ipv4 = IPV4Header()
		self.icmp = ICMPHeader()
		self.udp = UDPHeader()
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
		self.timestamp = 1000 * round(seconds + microseconds * 0.000000001 - orig_time, 6)

	def set_ipv4(self):
		offset = 14 # ethernet header length
		self.ipv4.set_ihl(self.data[offset+0: offset+1])
		self.ipv4.set_total_len(self.data[offset+2: offset+4])
		self.ipv4.set_identification(self.data[offset+4: offset+6])
		self.ipv4.set_fragment_offset(self.data[offset+6: offset+8])
		self.ipv4.set_ttl(self.data[offset+8: offset+9])
		self.ipv4.set_protocol(self.data[offset+9: offset+10])
		self.ipv4.set_ip(self.data[offset+12: offset+16], self.data[offset+16: offset+20])

	def set_icmp(self):
		offset = 14 + self.ipv4.ihl
		self.icmp.set_type(self.data[offset+0: offset+1])
		self.icmp.set_code(self.data[offset+1: offset+2])
		# windows
		if self.icmp.type_num == 8 or self.icmp.type_num == 0:
			self.icmp.set_sequence(self.data[offset+6: offset+8])
		#linux
		offset += 8 + self.ipv4.ihl
		if offset+4 <= self.header.incl_len:
			if self.icmp.type_num != 8 and self.icmp.type_num != 0:
				self.icmp.set_sequence(self.data[offset+6: offset+8]) # also windows
			self.icmp.set_src_port(self.data[offset+0: offset+2])
			self.icmp.set_dst_port(self.data[offset+2: offset+4])
		else:
			self.icmp.src_port = 0
			self.icmp.dst_port = 0		

	def set_udp(self):
		offset = 14 + self.ipv4.ihl
		self.udp.set_src_port(self.data[offset+0: offset+2])
		self.udp.set_dst_port(self.data[offset+2: offset+4])
		self.udp.set_udp_len(self.data[offset+4: offset+6])
		self.udp.set_checksum(self.data[offset+6: offset+8])

#############################################################
################ Parse Command Line Argument ################

# Get filename from command line
if len(sys.argv) != 2:
	print('Unexpected input. Usage: python3 TraceRouteAnalyzer.py <sample_trace_file.cap>')
	exit()

# Set input filename from given argument
input_file = sys.argv[1]

# Open the given pcap file in the binary mode
f = open(input_file, 'rb')

#############################################################
#################### Read Global Header #####################

# Read the first 24 bytes to get the global header
global_header = GlobalHeader(f.read(24))

# Map of protocols we care about
protocol_map = {1: 'ICMP', 17: 'UDP'}
protocol_used = {}

# Lists for storing packets
src = []
dst = []
pcap_start_time = None

packet_counter = 0

#############################################################
########## Parse Packets Headers and Packet Data) ###########
while True:
	packet_counter += 1

	# Read the next 16 bytes to get the packet header
	stream = f.read(16)

	# Terminate if reached end of file / empty byte
	if stream == b'':
		break

	# Create packet and parse header
	packet = Packet()
	packet.set_header(stream)
	packet.set_number(packet_counter)

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

	# Depending on protocol, parse ICMP header
	if packet.ipv4.protocol == 1:
		packet.set_icmp()
		dst.append(packet)
		protocol_used[1] = 'ICMP'
	
	# Depending on protocol, parse UDP header
	if packet.ipv4.protocol == 17:
		packet.set_udp()
		src.append(packet)
		# condition check to find the right UDP packets
		if not 33434 <= packet.udp.dst_port <= 33529:
			continue
		protocol_used[17] = 'UDP'
		
	# Skip all other packets with protocols we don't care about
	if packet.ipv4.protocol not in protocol_map:
		continue

#############################################################
################### R2 Helper Program #######################
### DON"T RUN FOR R1 ###
# R2 TTL probe calculation:
# ttl_dict = {}
# for p in src:
# 	if p.ipv4.ttl not in ttl_dict:
# 		ttl_dict[p.ipv4.ttl] = []
# 	ttl_dict[p.ipv4.ttl].append(p)

# for ttl in sorted(ttl_dict):
# 	#print(f'ttl: {ttl:2d} -> {len(ttl_dict[ttl])} probes')
# 	print(len(ttl_dict[ttl]))
# exit()
### DON"T RUN FOR R1 ###
#############################################################

# Windows
if any(p.icmp.type_num == 8 for p in dst):

	icmp_all = dst
	src = []
	dst = []
	
	for p in icmp_all:
		if p.icmp.type_num == 8:
			src.append(p)
		if p.icmp.type_num == 11 or p.icmp.type_num == 0: #or p.icmp.type_num == 3:
			dst.append(p)

	intermediate = []
	intermediate_packets = []
	rtt_dict = {}

	for p1 in src:
		for p2 in dst:
			if p1.icmp.sequence == p2.icmp.sequence:
				if p2.ipv4.src_ip not in intermediate:
					intermediate.append(p2.ipv4.src_ip)
					intermediate_packets.append(p2)
					rtt_dict[p2.ipv4.src_ip] = []
				
				# RTT Calculation
				p1.set_timestamp(pcap_start_time)
				p2.set_timestamp(pcap_start_time)
				rtt_dict[p2.ipv4.src_ip].append(p2.timestamp-p1.timestamp)

# Linux
else:
	intermediate = []
	intermediate_packets = []
	rtt_dict = {}

	for p1 in src:
		for p2 in dst:
			if p1.udp.src_port == p2.icmp.src_port: # and p2.icmp.type_num == 11 and p2.icmp.code == 0
				if p2.ipv4.src_ip not in intermediate:
					intermediate.append(p2.ipv4.src_ip)
					intermediate_packets.append(p2)
					rtt_dict[p2.ipv4.src_ip] = []
				
				# RTT Calculation
				p1.set_timestamp(pcap_start_time)
				p2.set_timestamp(pcap_start_time)
				rtt_dict[p2.ipv4.src_ip].append(p2.timestamp-p1.timestamp)

identity_dict = {}

# figure out fragmented datagrams
for packet in src:
	if packet.ipv4.identification not in identity_dict:
		identity_dict[packet.ipv4.identification] = []

	identity_dict[packet.ipv4.identification].append(packet)

# check fragment count
frag_count = 0
for identity in identity_dict:
	if len(identity_dict[identity]) > 1:
		frag_count += 1

#############################################################
################### R1 Required Output #######################

print('The IP address of the source node:', src[0].ipv4.src_ip)
print('The IP address of ultimate destination node:', src[0].ipv4.dst_ip)
print('The IP addresses of the intermediate destination nodes:')
for i in range(len(intermediate)-1):
	print(f'\trouter {i+1}: {intermediate[i]}')
	
print()

print('The values in the protocol field of IP headers:')
for protocol in sorted(protocol_used):
	print(f'\t{protocol}: {protocol_used[protocol]}')

print()

if frag_count == 0:
	print('The number of fragments created from the original datagram is:', frag_count)
	print('The offset of the last fragment is:', frag_count, '\n')
else:
	for identity in identity_dict:
		if len(identity_dict[identity]) > 1:
			print('The number of fragments created from the original datagram', identity, 'is:', len(identity_dict[identity]))
			
			offset = max(packet.ipv4.fragment_offset for packet in identity_dict[identity])
			print('The offset of the last fragment is:', offset, '\n')

# RTT average time and standard deviation
for i in range(len(intermediate)):
	avg = round(sum(rtt_dict[intermediate[i]]) / len(rtt_dict[intermediate[i]]), 6)
	std = round( (sum(pow(x-avg,2) for x in rtt_dict[intermediate[i]]) / len(rtt_dict[intermediate[i]]))**(1/2), 6)
	print('The avg RTT between', src[0].ipv4.src_ip, 'and', intermediate[i], 'is:', avg, 'ms, the s.d. is:', std, 'ms')

# End of program