'''

/* =======================================================================

   (c) 2015, Kre8 Technology, Inc.



   Name:          Robot Escape

   By:            Qin Chen, David Zhu

   Last Updated:  6/10/17



   PROPRIETARY and CONFIDENTIAL

   ========================================================================*/

'''

# This program shows how threads can be created using Python Thread class and your

# own function. Another way of creating threads is subclass Thread and override

# run().

#

# In this assignment, students will learn:

# 1. how to start a thread using Python Thread class and student's own function.

# 2. Use of event queue, putting and getting items from an event queue.

# 3. Implement two event handlers: motion and alert. Description of these

#   handlers is provided where the handler code is.

#

import sys

import time

import threading

import Tkinter as tk

import Queue

from HamsterAPI.comm_ble import RobotComm



class Event(object):

    def __init__(self, event_type, event_data):

      self.type = event_type #string

      self.data = event_data #list of number or character depending on type



class BehaviorThreads(object):

    Threshold_border = 20   # if floor sensor reading falls equal or below this value, border is detected

    Threshold_obstacle = 40   # if prox sensor reading is equal or higher than this, obstacle is detected

    

    def __init__(self):

        self.gBorder_reached = False

        self.gQuit = False

        # events queues for communication between processes

        self.alert_q = Queue.Queue()

        self.motion_q = Queue.Queue()

        self.spawn_threads()



    def spawn_threads(self):

        # start a watcher thread

        t_robot_watcher = threading.Thread(name='watch thread',target=self.robot_event_watcher, args=(self.alert_q, self.motion_q))

        t_robot_watcher.daemon = True

        t_robot_watcher.start()

        self.t_robot_watcher = t_robot_watcher



        #########################################

        # start a handler thread calling robot_motion_handler(). Passing in self.motion_q

        #########################################

        t_robot_motion = threading.Thread(name='handler thread', target=self.robot_motion_handler, args=(self.motion_q,))
        t_robot_motion.daemon = True
        t_robot_motion.start()
        self.t_robot_motion = t_robot_motion

        return



    #######################################################

    # This function monitors the sensors.

    # Based on sensor readings, it puts events to two event queues. The

    # possible events are: obstacle, clear(obs free), alert and border.

    #######################################################

    def robot_event_watcher(self, q1, q2):

        just_turned_on = True

        while not self.gQuit:

            if gRobotList:

                if (just_turned_on):

                    time.sleep(1)

                    just_turned_on = False



            for robot in gRobotList:            

                prox_l = robot.get_proximity(0)

                prox_r = robot.get_proximity(1)

                line_l = robot.get_floor(0)

                line_r = robot.get_floor(1)

                if (prox_l > BehaviorThreads.Threshold_obstacle or prox_r > BehaviorThreads.Threshold_obstacle):

                    #print "obstacle detected, q1: %d %d" % (prox_l, prox_r)

                    alert_event = Event("alert", [prox_l, prox_r])

                    q1.put(alert_event)

                    

                    ##############################

                    # Create an event and put it in motion queue

                    ##############################
                    obstacle_event = Event("obstacle detected", [prox_l, prox_r])
                    q2.put(obstacle_event)

                else:

                    clear_event = Event("no obstacle ahead", [prox_l, prox_r])
                    q2.put(clear_event)

                    ##############################

                    # create an event and put it in motion queue. Take out pass

                    ##############################



                if (line_l < BehaviorThreads.Threshold_border or line_r < BehaviorThreads.Threshold_border):

                    border_event = Event("border", [line_l, line_r])

                    q1.put(border_event)

                    ##############################

                    # create an event and put it in motion queue

                    ##############################

                    finish_event = Event("border detected", [line_l, line_r])
                    q2.put(finish_event)

            time.sleep(0.01)

        return 



    def get_out (self, robot):

        #go forward more  

        robot.set_wheel(0,30)

        robot.set_wheel(1,30)  

        time.sleep(0.3)  



        #stop and signal success

        robot.set_wheel(0,0)

        robot.set_wheel(1,0)  

        robot.set_led(0,2)

        robot.set_led(1,2)

        robot.set_musical_note(40)

        time.sleep(0.5)

        robot.set_musical_note(60)

        time.sleep(1)

        robot.set_musical_note(0)

        robot.set_led(0,0)

        robot.set_led(1,0)

        return



    ##############################################################

    # Implement your motion handler. You need to get event using the passed-in queue handle and

    # decide what Hamster should do. Hamster needs to avoid obstacle while escaping. Stop after

    # border is reached.

    #############################################################

    def robot_motion_handler(self, q):

        while True: 
            for robot in gRobotList:
                thisEvent = q.get()

                if thisEvent.type == "no obstacle ahead":
                    robot.set_wheel(0, 30)
                    robot.set_wheel(1, 30)
                elif thisEvent.type == "obstacle detected":
                    if thisEvent.data[0] > thisEvent.data[1]:
                        robot.set_wheel(0, 30)
                        robot.set_wheel(1, -30)
                    else:
                        robot.set_wheel(0, -30)
                        robot.set_wheel(1, 30)
                else:
                    self.get_out(robot)
                    return
                
        

class GUI(object):

    def __init__(self, root, threads_handle):

        self.root = root

        self.t_handle = threads_handle

        self.event_q = threads_handle.alert_q

        self.canvas = None

        self.initUI()



    def initUI(self):

        frame = self.root

        self.canvas = tk.Canvas(frame, bg="white", width=300, height=300)

        self.canvas.pack(expand=1, fill='both')

        self.canvas.create_rectangle(175, 175, 125, 125, fill="blue")



        # for display proximity sonsors (red beams)

        self.prox_l_id = self.canvas.create_line(135,125,135,125, fill="red")

        self.prox_r_id = self.canvas.create_line(165,125,165,125, fill="red")

 

        button1 = tk.Button(frame,text="Start")

        button1.pack()

        button1.bind('<Button-1>', self.startRobot)

  

        button2 = tk.Button(frame,text="Exit")

        button2.pack()

        button2.bind('<Button-1>', self.stopProg)



        t_alert_handler = threading.Thread(name='alert handler thread',target=self.robot_alert_handler, args=(self.event_q,))

        t_alert_handler.daemon = True

        t_alert_handler.start()

        return



    def startRobot(self, event=None):

        while not self.t_handle.gQuit:

            if gRobotList:

                self.t_handle.gBorder_reached = False # a new start

                break

            else:

                print "waiting for robot"

        for robot in gRobotList:

            robot.set_wheel(0,40)

            robot.set_wheel(1,40)

        return



    def stopProg(self, event=None):

        print "Cleaning up"

        self.t_handle.gQuit = True

        

        for robot in gRobotList:

            robot.reset()

        time.sleep(0.5)

 

        self.root.quit()

        return



    def robot_alert_handler(self, q):

        while not self.t_handle.gQuit:

            ###################################################

            # Handles data display and warning(sound).

            # Query event queue(using passed-in queue handle).

            # If there is an "alert" event, display red beams

            # for 0.01 seconds and then erase the beams.

            ###################################################
            for robot in gRobotList:

                thisEvent = q.get(True, float('inf'))

                if thisEvent.type == "alert":

                    robot.set_led(4)
                    robot.set_led(0)
                    robot.set_musical_note(40)
                    time.sleep(0.5)
                    robot.set_musical_note(60)

                    return



gMaxRobotNum = 1 # max number of robots to control

gRobotList = []



def main():

    comm = RobotComm(gMaxRobotNum)

    comm.start()

    print 'Bluetooth starts'

    global gRobotList

    gRobotList = comm.robotList



    frame = tk.Tk()

    t_handle = BehaviorThreads()

    gui = GUI(frame, t_handle) 

    frame.mainloop()



    comm.stop()

    comm.join()

    print("terminated!")



if __name__== "__main__":

  sys.exit(main())

  