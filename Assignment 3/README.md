# TraceRouteAnalyzer.py

The purpose of this assignment is to learn about the IP protocol. This python program analyzes a trace of IP datagrams created by _traceroute_.

To make terminologies consistent, in this assignment we call the source node as the computer that executes traceroute. The ultimate destination node refers to the host that is the ultimate destination defined when running traceroute. In addition, an intermediate destination node refers to the router that is not the ultimate destination node but sends back a ICMP message to the source node.

Run by providing a .pcap file.
```
python TraceRouteAnalyzer.py <sample_trace_file.cap>
```

This program outputs the following information:

- Lists the IP address of the source node, the IP address of ultimate destination node, the IP address(es) of the intermediate destination node(s). If multiple intermediate destination nodes exist, they should be ordered by their hop count to the source node in the increasing order
- Checks the IP header of all datagrams in the trace file, and list the set of values in the protocol field of the IP headers. Note that only different values are listed in a set.
- Number of fragments created from the original datagram. Note that 0 means no fragmentation. Prints out the offset (in terms of bytes) of the last fragment of the fragmented IP datagram. Note that if the datagram is not fragmented, the offset is 0
- Calculates the average and standard deviation of round trip time (RTT) between the source node and the intermediate destination node (s) and the average round trip time between the source node and the ultimate destination node. The average and standard deviation are calculated over all fragments sent/received between the source nodes and the (intermediate/ ultimate) destination node.

The output format is as follows: (Note that the values do not correspond to any trace file):
```
The IP address of the source node: 192.168.1.12
The IP address of ultimate destination node: 12.216.216.2
The IP addresses of the intermediate destination nodes:
router 1: 24.218.01.102,
router 2: 24.221.10.103,
router 3: 12.216.118.1.

The values in the protocol field of IP headers:
1: ICMP
17: UDP


The number of fragments created from the original datagram is: 3

The offset of the last fragment is: 3680

The avg RTT between 192.168.1.12 and 24.218.01.102 is: 50 ms, the s.d. is: 5 ms
The avg RTT between 192.168.1.12 and 24.221.10.103 is: 100 ms, the s.d. is: 6 ms
The avg RTT between 192.168.1.12 and 12.216.118.1 is: 150 ms, the s.d. is: 5 ms
The avg RTT between 192.168.1.12 and 12.216.216.2 is: 200 ms, the s.d. is: 15 ms
```
