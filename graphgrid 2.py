import sys
import pdb, time
import Tkinter as tk
import bfs_engine
import Queue
from HamsterAPI.comm_ble import RobotComm
import threading


class GraphGrid(object):
	def __init__(self, frame,  nodesUp, nodesDown, start_node, goal_node, evil_nodes=None):
		self.node_dist = 60
		self.node_size = 20
		self.gui_root = frame
		self.canvas = None
		self.graph = dict()
		self.evil_nodes=evil_nodes
		self.moveQ=Queue.Queue()
		self.directions=[]
		for i in range (nodesUp):
			for j in range (nodesDown):
	        		rset=set()
	        		if (str(i)+'-'+str(j) not in self.evil_nodes):
		        		if (j<nodesDown-1 and str(i)+'-'+str(j+1) not in self.evil_nodes):
			        		rset.add(str(i)+'-'+str(j+1))
			        	if (j>0 and str(i)+'-'+str(j-1) not in self.evil_nodes):
			        		rset.add(str(i)+'-'+str(j-1))
			        	if (i<nodesUp-1 and str(i+1)+'-'+str(j) not in self.evil_nodes):
			        		rset.add(str(i+1)+'-'+str(j))
			        	if (i>0 and str(i-1)+'-'+str(j) not in self.evil_nodes):
			        		rset.add(str(i-1)+'-'+str(j))
	        			self.graph[str(i)+"-"+str(j)]=rset

		self.start_node = start_node
		self.goal_node = goal_node
		self.hpaths=[]
		self.nodes_location=list()
		for x in self.graph.keys():
			r=x
			m=x.split('-')
			t=(r,[1+int(m[0]), 1+int(m[1])]) #make tuple
			self.nodes_location.append(t)
		self.display_graph()


	def display_graph(self):
		# for robot in gRobotList:
		# 	print("dsplay graph", robot)
		# 	robot.set_wheel(0,30)
		# 	robot.set_wheel(1,-30)
		# 	time.sleep(1)

		self.canvas = tk.Canvas(self.gui_root, bg="white", width=300, height=300)
		self.canvas.pack(expand=1, fill='both')
		for node in self.nodes_location:
			print 'node in display graph', node
			if node[0] == self.start_node:
				self.draw_node(node, 'purple')
			elif node[0] == self.goal_node:
				self.draw_node(node, 'pink')
			else:
				self.draw_node(node, 'lightblue')
		#pdb.set_trace()
		# get list of names of connected nodes
			connected_nodes = self.graph[node[0]]
		# find location for each connected node and draw edge
			if connected_nodes:
				for connected_node in connected_nodes:
		# step into node locations list
					for a_node in self.nodes_location:
						if connected_node == a_node[0]:
							#print("draw edge")
							self.draw_edge(node, a_node,'black')


	def highlight_path(self, path):
		#m=self.start_node.split('-')
		t=(self.start_node,[1+int(self.start_node.split('-')[0]), 1+int(self.start_node.split('-')[1])])
		self.hpaths.append(t)
		for node_name in path:
			if (node_name != self.start_node):          
				for a_node in self.nodes_location:
					if node_name == a_node[0] and node_name!=self.goal_node:
					    self.hpaths.append(a_node)
					    #print 'node in highlight path', a_node
					    self.draw_node(a_node, 'green')

		t=(self.goal_node,[1+int(self.goal_node.split('-')[0]), 1+int(self.goal_node.split('-')[1])])
		self.hpaths.append(t)

		for nodex in range (len(self.hpaths)-1):
			#print(self.hpaths[nodex])
			if (nodex!=len(self.hpaths)-1 and self.hpaths[nodex][1][0]==self.hpaths[nodex+1][1][0] and self.hpaths[nodex][1][1]<self.hpaths[nodex+1][1][1]):
				print("Down")
				self.directions.append("Down")
			elif (nodex!=len(self.hpaths)-1 and self.hpaths[nodex][1][0]==self.hpaths[nodex+1][1][0] and self.hpaths[nodex][1][1]>self.hpaths[nodex+1][1][1]):
				print("Up")
				self.directions.append("Up")
			elif (nodex!=len(self.hpaths)-1 and self.hpaths[nodex][1][1]==self.hpaths[nodex+1][1][1] and self.hpaths[nodex][1][0]>self.hpaths[nodex+1][1][0]):
				print("Left")
				self.directions.append("Left")
			else:
				self.directions.append("Right")
				print("Right")
			self.draw_edge(self.hpaths[nodex], self.hpaths[nodex+1], "red")

		#Finishes, pauses and waits for frame.mainloop() to be called

		# print "FINISHED WITH HIGHLIGHT PATH"
		# self.gui_root.mainloop()




	def draw_node(self, node, n_color):
		node_name = node[0]
		x = node[1][0]
		y = node[1][1]
		cpair="("+node[0].split('-')[0]+", "+node[0].split('-')[1]+")"
		dist = self.node_dist
		size = self.node_size
		self.canvas.create_oval(x*dist-size, y*dist-size, x*dist+size, y*dist+size, fill=n_color)
		self.canvas.create_text(x*dist, y*dist,fill="white",text=cpair)
		return

	def draw_edge(self, node1, node2, e_color):
		x1 = node1[1][0]
		y1 = node1[1][1]
		x2 = node2[1][0]
		y2 = node2[1][1]
		dist = self.node_dist
		self.canvas.create_line(x1*dist, y1*dist, x2*dist, y2*dist, fill=e_color, width=2)
		return


class StateToMovements(object):
	def __init__(self, moves):
		self.moves=moves
		self.intersection=False
		print(self.intersection)
		self.tryMaze()

	def tryMaze(self):
		if (self.moves[0]=="Right"):
			self.turnLeft()
			print("right")
		elif (self.moves[0]=="Left"):
			self.turnLeft()
			print("left")
		else:
			self.goForward()
			print("forward")

		for i in range (1, len(self.moves)):
			if (self.moves[i-1]==self.moves[i]):
				print("forward")
				self.peep()
				self.goForward()
			elif ((self.moves[i-1]=="Right" and self.moves[i]=="Down") or (self.moves[i-1]=="Left" and self.moves[i]=="Up") or (self.moves[i-1]=="Up" and self.moves[i]=="Right") or (self.moves[i-1]=="Down" and self.moves[i]=="Left")):
				print("right")
				self.turnRight()
			else:
				print("left")
				self.turnLeft()

	def goForward(self):
		# print "in go forward"
		robot=gRobotList[0]
		while self.intersection==False:
			l=((robot.get_floor(0)-30)*(.4+(100-robot.get_floor(0))/100))-10
			r=((robot.get_floor(1)-30)*(.4+(100-robot.get_floor(1))/100))-10
			l*=2
			r*=2
			robot.set_wheel(0,int(l))
			robot.set_wheel(1,int(r))
			if (robot.get_floor(0)<30 and robot.get_floor(1)<30):
				self.intersection=True
		# time.sleep(1.9)
		robot.set_wheel(0,0)
		robot.set_wheel(1,0)
		time.sleep(.5)
		self.intersection=False
		return

	def peep(self):
		robot=gRobotList[0]
		robot.set_wheel(0,30)
		robot.set_wheel(1,30)
		time.sleep(.3)
		robot.set_wheel(0,0)
		robot.set_wheel(1,0)
		time.sleep(.4)


	def turnRight(self): #90 degrees
		# print "actually in turn right"
		robot=gRobotList[0]
		while (robot.get_floor(0)<30 or robot.get_floor(1)<30):
			robot.set_wheel(0,30)
			robot.set_wheel(1,0)
		time.sleep(.2)
		self.goForward()


	def turnLeft(self):
		# print "actually in turn left"
		robot=gRobotList[0]
		while (robot.get_floor(0)<30 or robot.get_floor(1)<30):
			robot.set_wheel(0,0)
			robot.set_wheel(1,30)
		time.sleep(.2)
		self.goForward()
							

def main():

	gMaxRobotNum = 1 # max number of robots to control
	comm = RobotComm(gMaxRobotNum)
	comm.start()
	print 'Bluetooth starts'
	global gRobotList
	gRobotList = comm.robotList



	frame = tk.Tk()
	frame.title('Simple Graph Display')
	frame.geometry("600x600")

	# while (True):
	# 	print "len grobotlist", len(gRobotList)
	# 	if gRobotList:
	# 		for robot in gRobotList:
	# 			print "in for loop", robot
	# 			robot.set_wheel(0,100)
	# 			robot.set_wheel(1,100)
	# 			time.sleep(5)
	# 			break_v = True
	# 			break;
	# 	if break_v:
	# 		break

	height=int(raw_input("How wide should the grid be? "))
	width=int(raw_input("How tall should the grid be? "))

	start_node = '0-1'
	start_node=raw_input("What is the start node? ")
	try:
		while (int(start_node.split('-')[0])<0 or int(start_node.split('-')[1])>width-1 or int(start_node.split('-')[0])>height-1 or int(start_node.split('-')[1])<0):
			print(start_node.split('-'))
			start_node=raw_input("What is the start node? ")
	except:
		start_node='0-1'

	end_node = '0-2'
	end_node=raw_input("What is the end node? ")
	try:
		while (int(end_node.split('-')[0])<0 or int(end_node.split('-')[1])>width-1 or int(end_node.split('-')[0])>height-1 or int(end_node.split('-')[1])<0
			 or start_node==end_node):
			print(start_node.split('-'))
			start_node=raw_input("What is the end node? ")
	except:
		end_node='0-1'



	evil_nodes=[]
	evil_node=raw_input("Enter an evil node; n to quit ")
	while (evil_node!='n'):
		if (int(evil_node.split('-')[0])<0 or int(evil_node.split('-')[1])>width-1 or int(evil_node.split('-')[0])>height-1 or int(evil_node.split('-')[1])<0
			 or start_node==evil_node or end_node==evil_node):
			evil_node=raw_input("Enter an evil node; n to quit ")
		else:
			evil_nodes.append(evil_node)

			evil_node=raw_input("Enter an evil node; n to quit ")


	display = GraphGrid(frame, height, width, start_node, end_node, evil_nodes)

	bfs = bfs_engine.BFS(display.graph)

	p = bfs.bfs_shortest_path(start_node, end_node)

	display.highlight_path(p)


	# StateToMovements(display.directions)
	FSM_thread=threading.Thread(name='FSM thread',target=StateToMovements, args=(display.directions,))
	FSM_thread.setDaemon(True)
	FSM_thread.start()

	frame.mainloop()

	#stops working

	
	comm.stop()
	
	comm.join()
	return


if __name__==main():
	sys.exit(main())
