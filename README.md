# Distributed-Key-Value-Pair

A demonstration of the implementation of a distributed columnary NoSQL implementation for big data.  
A distributed key-value store with multiple nodes, node management, replica management and fault tolerance.  
Support for GET and POST requests.

## Command Format:  
**GET**:  _`<tablename> <rowid> <column family>:<column>`_  
**POST**: _`<tablename> <rowid> <column family>:<column> <value>`_

## Technologies used:  

1. Node.JS
2. Python

## Distributed communication:  

1. ZeroMQ - zmq library for python
2. NodeJS child processes - through PythonShell

## Architecture:  

The architecture consists of 4 layers,

1. Client - where the user enters the get/post commands
2. Web Server - to handle client requests
3. Application Master - node management, fault tolerance, replication management
4. Node Manager - management of indivisual nodes
