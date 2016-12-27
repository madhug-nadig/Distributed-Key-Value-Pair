# Distributed-Key-Value-Pair

A demonstration of the implementation of a distributed columnar NoSQL key-value pair based datastore for big data. With support for multiple nodes, node management, centralized control, replica management and fault tolerance. Implemented with GET(Query) and POST(entry) requests with persistent storage.  Architecture suitable for 'read once write consistently' type of applications.

Built from scratch with Python and NodeJS.

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
