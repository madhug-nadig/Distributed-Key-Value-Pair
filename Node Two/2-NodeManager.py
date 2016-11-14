import zmq
import os

#For creating a directory in the local FS
def make_path(command_array, path):
	print("\nRecived: \nCommand: " + str(command))

	try:
		os.makedirs(path, exist_ok = True)
	#chutiyapa, baadme theek karunga.
	except OSError as exception:
		pass

	print("\n\nTable:", command_array[0], "\nRow_ID:", command_array[1])
	for i in range(2, len(command_array), 2):
		famcol = command_array[i].split(':')
		print(famcol)
		f = open(path + '\\' + famcol[0] + '.txt', 'a', encoding = 'utf-8')

		f.write(str(command_array[1]) + '\t' + str(famcol[1]) + '\t' + str(command_array[i+1]))
		f.write('\n')
		f.close()

		print("\nColumn Family:", famcol[0], "\nColumn" ,famcol[1], "\nValue:", command_array[i+1])

#For searching for the given key in the local FS
def search_for(command_array, path):
	
	print("\n\nTable:", command_array[0], "\nRow_ID:", command_array[1])

	if not os.path.exists(path):
		return "Not Found at path: " + path

	famcol = command_array[2].split(':')
	
	if not os.path.exists(path+ '\\' + famcol[0] + '.txt'):
		return "Not Found at: " + path+ '\\' + famcol[0] + '.txt'
	f= open(path+ '\\' + famcol[0] + '.txt', 'r', encoding = 'utf-8')
	for line in f.readlines():
		line_list = line.split('\t')
		print(line_list[0], command_array[1],line_list[1], famcol[1])
		if line_list[0] == command_array[1] and line_list[1] == famcol[1]:
			return line_list[2]
	
	return "Not Found"


# ZeroMQ Context
context = zmq.Context()

# Run the server
while True:
    
	# Define the socket using the "Context"
	sock = context.socket(zmq.REP)
	sock.bind("tcp://127.0.0.1:5678")
	data = sock.recv().decode("utf-8")
	dataarray = data.split(";")
	job_type = dataarray[0]

	if job_type == 'post':
		command = dataarray[1]
		command_array = command.split()
		make_path(command_array, r'C:\Users\Nadig\Desktop\Big Data Project\Node Two\tables\\' + command_array[0])

	elif job_type == 'get':
		command = dataarray[1]
		command_array = command.split()
		print("\nRecived: \nCommand: " + str(command))
		res = search_for(command_array, r'C:\Users\Nadig\Desktop\Big Data Project\Node Two\tables\\' + command_array[0])
		print(res)

	else:
		print('Error: Unknow job type ', job_type)