'''
/* =======================================================================
   (c) 2015, Kre8 Technology, Inc.
   This is a program that is provided to students in Robot AI class.
   Students use this it to build different Hamster behaviors.

   Name:          starter1.py
   By:            Qin Chen
   Last Updated:  6/10/16

   PROPRIETARY and CONFIDENTIAL
   ========================================================================*/
'''
import sys
import time
import threading
import Tkinter as tk
from HamsterAPI.comm_ble import RobotComm	# no dongle
#from HamsterAPI.comm_usb import RobotComm	# yes dongle

################################
# Hamster control
################################
class RobotBehaviorThread(threading.Thread):
	def __init__(self):
		super(RobotBehaviorThread, self).__init__()
		self.go = False
		self.done = False
		self.Square = False
		self.Shy = False
		self.Dance = False
		self.Follow = False
		self.Pause = False
		self.Keyboard_control = False
		return

	def run(self):
		robot=None
		while not self.done:
			if gRobotList:
				robot = gRobotList[0]	# max 1 robot per student
			if robot and self.go:
				#############################################
				print("test")
				#############################################
			if robot and self.Square: 

				robot.set_wheel(0, 30)
				robot.set_wheel(1, 30)
				time.sleep(1.5)
				robot.set_wheel(0, 0)
				robot.set_wheel(1, 30)
				time.sleep(1.5)

			if robot and self.Shy:

				left = robot.get_proximity(0)
				right = robot.get_proximity(1)
				if left > 30 and right > 30:

					robot.set_wheel(0, -30)
					robot.set_wheel(1, -30)

				else:
					robot.set_wheel(0, 0)
					robot.set_wheel(1, 0)

			if robot and self.Dance:

				left = robot.get_proximity(0)
				right = robot.get_proximity(1)

				if left > 30 and right > 30:

					robot.set_wheel(0, 30)
					robot.set_wheel(1, 30)
					#robot.set_musical_note(40)
					time.sleep(1)
					robot.set_wheel(0, -30)
					robot.set_wheel(1, -30)
					#robot.set_musical_note(60)
					time.sleep(1)
				else:

					robot.set_wheel(0, 0)
					robot.set_wheel(1, 0)

			if robot and self.Follow:

				left = robot.get_proximity(0)
				right = robot.get_proximity(1)

				if left > 20:
					robot.set_wheel(0, 0)
					robot.set_wheel(1, 30)
				elif right > 20:
					robot.set_wheel(0, 30)
					robot.set_wheel(1, 0)
				else:
					robot.set_wheel(0, 0)
					robot.set_wheel(1, 0)

			
			if robot and self.Pause:

				self.go = False
				self.Square = False
				self.Shy = False
				self.Follow = False
				self.Dance = False
				robot.set_wheel(0,0)
				robot.set_wheel(1,0)

				
				#############################################
				# END OF YOUR WORKING AREA!!!
				#############################################					
		# stop robot activities, such as motion, LEDs and sound
		# clean up after exit button pressed
		if robot:
			robot.reset()
			time.sleep(0.1)
		return

class GUI(object):
	def __init__(self, root, robot_control):
		self.root = root
		self.robot_control = robot_control
		root.geometry('250x30')
		root.title('Hamster Control')

		b1 = tk.Button(root, text='Go')
		b1.pack(side='left')
		b1.bind('<Button-1>', self.startProg)

		b2 = tk.Button(root, text='Exit')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.stopProg)

		b2 = tk.Button(root, text='Square')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.SquareProg)

		b2 = tk.Button(root, text='Shy')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.ShyProg)

		b2 = tk.Button(root, text='Dance')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.DanceProg)

		b2 = tk.Button(root, text='Follow')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.FollowProg)

		b2 = tk.Button(root, text='Pause')
		b2.pack(side='left')
		b2.bind('<Button-1>', self.PauseProg)


		return
	
	def startProg(self, event=None):
		self.robot_control.go = True
		return

	def stopProg(self, event=None):
		self.robot_control.done = True		
		self.root.quit() 	# close window
		return

	def SquareProg(self, event=None):
		self.robot_control.Square = True
		return

	def ShyProg(self, event=None):
		self.robot_control.Shy = True
		return

	def DanceProg(self, event=None):
		self.robot_control.Dance = True
		return

	def FollowProg(self, event=None):
		self.robot_control.Follow = True
		return

	def PauseProg(self, event=None):
		self.robot_control.Pause = True
		return


#################################
# Don't change any code below!! #
#################################

def main():
    # instantiate COMM object
    global gRobotList

    gMaxRobotNum = 1 # max number of robots to control
    comm = RobotComm(gMaxRobotNum)
    comm.start()
    print 'Bluetooth starts'  
    gRobotList = comm.robotList

    behaviors = RobotBehaviorThread()
    behaviors.start()

    frame = tk.Tk()
    GUI(frame, behaviors)
    frame.mainloop()

    comm.stop()
    comm.join()
    print("terminated!")

if __name__ == "__main__":
    sys.exit(main())