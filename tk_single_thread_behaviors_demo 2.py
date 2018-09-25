'''

/* =======================================================================

   (c) 2015, Kre8 Technology, Inc.



   Written By Dr. David Zhu, Qin Chen



   Last updated: May 28th, 2016



   PROPRIETARY and CONFIDENTIAL

   ========================================================================*/

'''

import sys

import time  # sleep

import Tkinter as tk

import threading

import Queue

from HamsterAPI.comm_ble import RobotComm

#from HamsterAPI.comm_usb import RobotComm



gMaxRobotNum = 8; # max number of robots to control

gRobotList = []



class ThreadedBehaviors(object):

    def __init__(self):

        self.behavior='Pause'

        self.gQuit = False

        t = threading.Thread(target=self.behaviors)

        t.daemon = True

        t.start()

        self.behavior_handle = t



    def behaviors(self):

        while not self.gQuit:

            if self.behavior == 'Square':

                self.square()

            elif self.behavior == 'Shy':

                self.shy()

            elif self.behavior == 'Dance':

                self.dance()

            elif self.behavior == 'Follow':

                self.follow()

            elif self.behavior == 'Pause':

                self.pause()       

            else:

                print 'waiting for robot...'

        print "exiting behaviors loop"



    def square(self):

        if gRobotList:

            for robot in gRobotList:

                for i in range(3):

                    #time.sleep(1)

                    robot.set_wheel(0, 30)

                    robot.set_wheel(1, 30)

                    time.sleep(1.6)

                    robot.set_wheel(0, -30)

                    robot.set_wheel(1, 30)

                    time.sleep(0.8)

        #time.sleep(0.1)

        return





    def shy(self):        

        if gRobotList:

            for robot in gRobotList:

                prox_l = robot.get_proximity(0)

                prox_r = robot.get_proximity(1)

                if (prox_l > 40 or prox_r > 40):

                    robot.set_wheel(0,20-prox_l)

                    robot.set_wheel(1,20-prox_r)

                    robot.set_musical_note((prox_l+prox_r)/2)  

                    time.sleep(0.1)

                else:

                    robot.set_wheel(0,0)

                    robot.set_wheel(1,0)

                    robot.set_musical_note(0)

                    time.sleep(0.1)

        #time.sleep(0.5)                   

        

    def follow(self):

        if gRobotList:

            for robot in gRobotList:

                prox_l = robot.get_proximity(0)

                prox_r = robot.get_proximity(1)

                if prox_l < 10 and prox_r < 10: #nothing in sight

                    robot.set_wheel(0, 0)

                    robot.set_wheel(1, 0)

                elif prox_l < 70 or prox_r < 70: # either sensor sees target within follow range

                    robot.set_wheel(0, 70-prox_l)

                    robot.set_wheel(1, 70-prox_r)

                else: # too close to target

                    robot.set_wheel(0, 0)

                    robot.set_wheel(1, 0)

        return

        

    def dance(self):

        if gRobotList:

            for robot in gRobotList:

                prox_l = robot.get_proximity(0)

                prox_r = robot.get_proximity(1)         

                if (prox_l > 45 or prox_r > 45):

                    robot.set_wheel(0, 10-prox_l)

                    robot.set_wheel(1, 10-prox_r)

                    robot.set_musical_note((prox_l+prox_r)/2) 

                    time.sleep(0.1)

                elif (prox_l < 40 or prox_r < 40) and (prox_l > 10 and prox_r > 10):

                    robot.set_wheel(0, 80-prox_l)

                    robot.set_wheel(1, 80-prox_r)

                    robot.set_musical_note((prox_l+prox_r)/2)  

                    time.sleep(0.1)

                else:

                    robot.set_wheel(0,0)

                    robot.set_wheel(1,0)

                    robot.set_musical_note(0)                   

                    time.sleep(0.2)

        return



    def pause(self):

        if gRobotList:

            for robot in gRobotList:

                robot.set_wheel(0,0)

                robot.set_wheel(1,0)

                robot.set_musical_note(0)

        time.sleep(0.1)

        return



    def Square(self, event=None):

        self.behavior = "Square"



    def Shy(self, event=None):

        self.behavior = "Shy"



    def Follow(self, event=None):

        self.behavior = "Follow"



    def Dance(self, event=None):

        self.behavior = "Dance"



    def Pause(self, event=None):

        self.behavior = 'Pause'

        

class GUI(object):

    def __init__(self, root, behaviors):

        self.root = root

        self.behaviors = behaviors

        self.initUI()



    def initUI(self):

        frame = self.root

        canvas = tk.Canvas(frame, bg="white", width=300, height=300)

        canvas.pack(expand=1, fill='both')

        canvas.create_rectangle(175, 175, 125, 125, fill="green")

  

        button0 = tk.Button(frame,text="Square")

        button0.pack(side='left')

        button0.bind('<Button-1>', self.behaviors.Square)



        button1 = tk.Button(frame,text="Shy")

        button1.pack(side='left')

        button1.bind('<Button-1>', self.behaviors.Shy)



        button2 = tk.Button(frame,text="Follow")

        button2.pack(side='left')

        button2.bind('<Button-1>', self.behaviors.Follow)



        button3 = tk.Button(frame,text="Dance")

        button3.pack(side='left')

        button3.bind('<Button-1>', self.behaviors.Dance)



        button4 = tk.Button(frame,text="Pause")

        button4.pack(side='left')

        button4.bind('<Button-1>', self.behaviors.Pause)



        button5 = tk.Button(frame,text="Exit")

        button5.pack(side='left')

        button5.bind('<Button-1>', self.stopProg)



    def stopProg(self, event=None):

        self.behaviors.gQuit = True

        for robot in gRobotList:

            robot.reset()

        time.sleep(0.5)

        self.behaviors.behavior_handle.join()

        self.root.quit()

        return



def main(argv=None):    

    global gRobotList

    # instantiate COMM object

    comm = RobotComm(gMaxRobotNum)

    comm.start()

    print 'Bluetooth starts'  

    gRobotList = comm.robotList



    behaviors = ThreadedBehaviors()

    

    frame = tk.Tk()

    GUI(frame, behaviors)

    frame.mainloop()



    comm.stop()

    comm.join()

    print("terminated!")



if __name__ == "__main__":

    sys.exit(main())