import sys
import json
import zmq
import random
import time
import _thread


#this handled the get
def get_job(command, s):
	#poller = zmq.Poller()
	#poller.register(s,zmq.POLLIN)
	#socks = dict(poller.poll(5000))
	data = "get;"
	data = data + str(command)
	
	try:
		s.send(data.encode('utf-8'), zmq.NOBLOCK)
	except Exception as e:
		print(str(e))

	return "\nThe client's get request : \nCommand: " + command

#this handles the post
def post_job(command, s):
	data = "post;"
	data = data + str(command)
	s.send(data.encode('utf-8'))

	return "\nThe client posted : \nCommand : " + command + "\n"

def main():

	opdic = []

	flag = sys.argv[1].strip()

	# ZeroMQ Context For distributed Message amogst processes
	context = zmq.Context()

	# Define the socket using the "Context". Create a transport layer socket, for TCP based communucation with other processes

	nodes={}
	number_of_nodes = 0

	f = open('../metadata/nodes.tsv', 'r')
	for i in f.readlines():
		number_of_nodes += 1
		ll  = i.split(',')
		ip_port = []
		ip_port.append(ll[1])
		ip_port.append(ll[2].strip())
		nodes[int(ll[0])] = ip_port
	f.close()

	# ZeroMQ Context For distributed Message amogst processes
	context = zmq.Context()

	# Define the socket using the "Context". Create a transport layer socket, for TCP based communucation with other processes

	socks = [None] * len(nodes)
	
	for id, ip_port in nodes.items():
		socks[id] = context.socket(zmq.REQ)
		socks[id].connect("tcp://" + ip_port[0] + ":" + ip_port[1])

	if flag == "get":
		command = sys.argv[2].strip()
		#Pass the socket reference to the get job
		f = open('../metadata/loc.tsv', 'r')
		for i in f.readlines():
			ll = i.split(',')
			if command.split()[1] == ll[0]:
				id = ll[1]
		f.close()
		
		mastr = False
		try:
			rg = get_job(command, socks[id])
			got_from = str(id+1) #+1 because the node id starts from 0
			socks[id].setsockopt(zmq.RCVTIMEO, 1000)
			socks[id].setsockopt(zmq.LINGER, 0)
			data = socks[id].recv().decode('utf-8') #receive data from the main node	
			mastr = True
		except:
			try:
					rg = get_job(command, socks[(id+1)%number_of_nodes])
					got_from = str((id+1)%number_of_nodes+1) #+1 because the node id starts from 0

			except Exception as e:
				print("ERR: " + str(e))
		
		if(mastr == False):
			data = socks[(id+1)%number_of_nodes+1].recv().decode('utf-8') #receive data from the replica node
		
		if data != "Not Found":
			opdic.append({"message": rg, "status": "successful", "value": data, "from": got_from})
		else:
			opdic.append({"message": rg, "status": "unsuccessful", "value": data, "from": got_from})

	elif flag == "post":
		command = sys.argv[2].strip()
		id = random.randint(0, number_of_nodes - 1)
		replica = (id+1) % number_of_nodes
		
		main_mode = str(id+1)		   #+1 because the node id starts from 0
		replica_node = str(replica +1) #+1 because the node id starts from 0, replicating the data to the next node
		
		#Pass the socket reference to the post job
		f = open('../metadata/loc.tsv', 'a') #rowid to location mapping
		f.write(str(command.split()[1]))
		f.write('\t')
		f.write(str(id))
		f.write('\n')
		f.close()
		
		rp = post_job(command, socks[id]) # Implement the post job in main Node
		rp2 = post_job(command, socks[replica]) # Implement the post job in replica Node
		
		opdic.append({"message": rp , "status": "successful","main": main_mode, "replica": replica_node})
	else:
		opdic.append({"status": "failed", "flag": flag})
	print(json.dumps(opdic))

main()