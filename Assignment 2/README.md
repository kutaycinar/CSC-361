# TCPAnalyzer.py

The purpose of this project is to understand the details of state management in Transmission Control Protocol (TCP). This program is written to analyze the TCP protocol behavior.

With a TCP trace file, this program parses and process the trace file, and tracks the TCP state information. A sample TCP trace file (sample-capture-file.cap) is
provided. During the period traced, a single web client accesses different web sites on the Internet.

Run by providing a .cap file:
```
python TCPAnaylzer.py <sample-capture-file.cap>
```

As an example output, after running the program with sample-capture-file.cap:
```
A) Total number of connections: 48
______________________________________

B) Connections' details:

Connection 1:
Source Address: 192.168.1.164
Destination Address: 142.104.5.64
Source Port: 1200
Destination Port: 80
Status: S2F1
Start time: 0.0 seconds
End time: 43.612948 seconds
Duration: 43.612948 seconds
Number of packets sent from Source to Destination: 54
Number of packets sent from Destination to Source: 77
Total number of packets: 131
Number of data bytes sent from Source to Destination: 3063 bytes
Number of data bytes sent from Destination to Source: 100559 bytes
Total number of data bytes: 103622 bytes
END 
+++++++++++++++++++++++++++++++++
.
.
.
+++++++++++++++++++++++++++++++++
Connection 48:
Source Address: 192.168.1.164
Destination Address: 132.170.108.140
Source Port: 1247
Destination Port: 80
Status: S2F1
Start time: 266.975155 seconds
End time: 282.552335 seconds
Duration: 15.57718 seconds
Number of packets sent from Source to Destination: 9
Number of packets sent from Destination to Source: 11
Total number of packets: 20
Number of data bytes sent from Source to Destination: 285 bytes
Number of data bytes sent from Destination to Source: 11122 bytes
Total number of data bytes: 11407 bytes
END 
+++++++++++++++++++++++++++++++++
______________________________________

C) General:

Total number of complete TCP connections: 32
Number of reset TCP connections: 34
Number of TCP connections that were still open when the trace capture ended: 16
______________________________________

D) Complete TCP connections:

Minimum time duration: 0.010284 seconds
Mean time duration: 6.812052 seconds
Maximum time duration: 43.612948 seconds

Minimum RTT value: 0.000328 seconds
Mean RTT value: 0.315904 seconds
Maximum RTT value: 16.654651 seconds

Minimum number of packets including both send/received: 8
Mean number of packets including both send/received: 37.3125
Maximum number of packets including both send/received: 239

Minimum number of window size including both send/received: 0
Mean number of window size including both send/received: 15277.688442
Maximum number of window size including both send/received: 64240
______________________________________
```
