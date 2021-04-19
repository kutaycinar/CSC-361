# TCPAnalyzer.py

The purpose of this project is to understand the details of state management in Transmission Control Protocol (TCP). This program is written to analyze the TCP protocol behavior.

With a TCP trace file, this program parses and process the trace file, and tracks the TCP state information. A sample TCP trace file (sample-capture-file.cap) is
provided. During the period traced, a single web client accesses different web sites on the Internet.

Run by providing a .cap file:
```
python TCPAnaylzer.py <sample-capture-file.cap>
```

Output format:
```
A) Total number of connections:
______________________________________

B) Connections' details:

Connection 1:
Source Address:
Destination Address:
Source Port:
Destination Port:
Status:
Start time:
End time:
Duration:
Number of packets sent from Source to Destination:
Number of packets sent from Destination to Source:
Total number of packets:
Number of data bytes sent from Source to Destination:
Number of data bytes sent from Destination to Source:
Total number of data bytes:
END
+++++++++++++++++++++++++++++++++
.
.
.
+++++++++++++++++++++++++++++++++
Connection N:
Source Address:
Destination Address:
Source Port:
Destination Port:
Status:
Start time:
End time:
Duration:
Number of packets sent from Source to Destination:
Number of packets sent from Destination to Source:
Total number of packets:
Number of data bytes sent from Source to Destination:
Number of data bytes sent from Destination to Source:
Total number of data bytes:
END
+++++++++++++++++++++++++++++++++
______________________________________

C) General:

Total number of complete TCP connections: 
Number of reset TCP connections: 
Number of TCP connections that were still open when the trace capture ended: 
______________________________________

D) Complete TCP connections:

Minimum time duration: 
Mean time duration: 
Maximum time duration: 

Minimum RTT value: 
Mean RTT value: 
Maximum RTT value: 

Minimum number of packets including both send/received: 
Mean number of packets including both send/received: 
Maximum number of packets including both send/received: 

Minimum number of window size including both send/received: 
Mean number of window size including both send/received: 
Maximum number of window size including both send/received: 
______________________________________
```
