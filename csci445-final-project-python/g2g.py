from pyCreate2 import create2
import math
import odometry
import lab11_plot
from lab11_plot import myLine
import pyCreate2
# from pyCreate2.robot import pen_holder

import pid_controller




class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.servo = factory.create_servo()
        self.odometry = odometry.Odometry()
        self.penholder = factory.create_pen_holder()
        self.base_speed = 100
    
    def wait(self):
        end_time = self.time.time() + 0.015
        while (self.time.time() < end_time):
            pass


    def run(self):
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])

        # go to angle...
        
        start_time = self.time.time()
        end_time = self.time.time()+300


        # ORDER:
        # Get to bottom left of door.
        # Draws door clockwise along segments (referring to segment order, not rotation), should then go left for bottom segment, turn around and go right...
        index = 0
        # segments = [ [1,0, "red"], [1,1,"blue"], [2,1,"blue"]]
        # segments = [ [1,0, "red"], [1,1,"red"]]
        
        # START DEBUG
        segments = []
        iFile = open("hardOutput.txt", "r")
        for line in iFile:
            words = line.split()
            myTempLine = myLine(words[0], words[1], words[2], words[3], words[4], words[5])
            segments.append(myTempLine)
        for i in segments:
            print(i.xStart, i.yStart, i.xEnd, i.yEnd, i.color, i.type)

        # END DEBUG

        # if len(segments) > 0:
        #     firstMove = myLine(0,-0.2,segments[0].xStart, segments[0].yStart, segments[0].color, "line")
        #     segments.insert(0,firstMove)

        print("START")
        print(self.odometry.x, self.odometry.y)
        self.penholder.set_color(0.0, 1.0, 0.0)
        self.penholder.go_to(-0.045)

        # SET GAINS!
        theta_gain = 0.5
        dist_gain = 300


# class myLine:
    
        # s1 = myLine(0,-0.2,0,1,"red", "line")
        # s2 = myLine(0,1,1,1,"red", "line")
        # s3 = myLine(1,1,1,0,"red", "line")
        # s4 = myLine(1,0,0,0,"red", "line")

        # segments = [s1, s2, s3, s4]
        colorKey = { 
            "blue": [0,0,1],
            "green":[0,1,1],
            "red":[1,0,0],
            "black":[0,0,0]
        }
        while index < len(segments):
            if segments[index].color == "none":
                self.penholder.go_to(0.0)
            else:
                self.penholder.set_color(colorKey[segments[index].color][0], colorKey[segments[index].color][1], colorKey[segments[index].color][2])
                self.penholder.go_to(-0.045)


            state = self.create.update()
            if state is not None:
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)

            # DEFINE SOME ANGLE STUFF
            print(segments[index].xEnd - segments[index].xStart)
            draw_theta = 3.14/2 + math.atan2(segments[index].yEnd - segments[index].yStart, segments[index].xEnd - segments[index].xStart)
            robot_x = segments[index].xEnd + 0.2*math.cos(draw_theta)
            robot_y = segments[index].yEnd + 0.2*math.sin(draw_theta)

            print("TARGET: (%f, %f)" % (segments[index].xEnd, segments[index].yEnd))
            print("ROBOT TARGET: (%f, %f)" % (robot_x, robot_y))



            if state is None:
                break

            print("test")
            # Next marker segments
            # goal_x = float(segments[index].xEnd)
            # goal_y = float(segments[index].yEnd)

            # # Corresponding robot segments
            # robot_coords = self.penholder.translate_coords_to_robot([goal_x, goal_y])
            # robot_x = robot_coords[0]
            # robot_y = robot_coords[1]

            # fun comment

            print(robot_x)
            print(robot_y)
            print("odometry")
            print(self.odometry.x)
            print(self.odometry.y)
            print(self.odometry.theta)

            # One of these might be wrong...
            theta_error = (math.atan2(robot_y - self.odometry.y, robot_x - self.odometry.x) - self.odometry.theta) % (2*3.14)
            dist_error = math.sqrt(math.pow(robot_x - self.odometry.x, 2) + math.pow(robot_y - self.odometry.y, 2))
            print("theta error: %f" % theta_error)
            print("dist error: %f" % dist_error)

            # TODO: reduce this range later...
            print("ROTATING TOWARDS (%f, %f)" % (robot_x, robot_y))
            while abs(theta_error) > 0.02:
                state = self.create.update()
                if state is not None:
                    self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                theta_error = (math.atan2(robot_y - self.odometry.y, robot_x - self.odometry.x) - self.odometry.theta) % (2*3.14)
                
                if theta_error <= 3.14:
                    dir_of_turn = -1
                else:
                    dir_of_turn = 1


                print("Theta error: %f" % theta_error)
                clamped_theta_error = max(min(theta_gain*theta_error, 100), -100)
                print("starting rotation")
                wb = .232 # fixed length
                length = 0.04
                ratio = length/(length + wb)
                rw_speed = self.base_speed*ratio*theta_gain
                lw_speed = self.base_speed*theta_gain
                # self.create.drive_direct(int(clamped_theta_error), int(-clamped_theta_error))

                self.create.drive_direct(int(dir_of_turn*rw_speed), int(dir_of_turn*lw_speed))
                self.wait()

            print("MOVING ROBOT TO (%f, %f)" % (robot_x, robot_y))
            print("MOVING PEN TO (%f, %f)" % (segments[index].xEnd, segments[index].yEnd))
            while dist_error > 0.1:
                state = self.create.update()
                if state is not None:
                    self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                print("dist error: %f" % dist_error)
                dist_error = math.sqrt(math.pow(robot_x - self.odometry.x, 2) + math.pow(robot_y - self.odometry.y, 2))
                clamped_dist_error = max(min(dist_gain*dist_error, 200), -200)
                self.create.drive_direct(int(clamped_dist_error), int(clamped_dist_error))
                self.wait()
            

            print("QUICK PAUSE! We got robot: (%f, %f) close to target: (%f, %f)" % (self.odometry.x, self.odometry.y, robot_x, robot_y))
            print("QUICK PAUSE! We got pen to (%f, %f)" % (segments[index].xEnd, segments[index].yEnd))
            # self.create.drive_direct(0,0)
            self.time.sleep(3)


            # TODO: FIX THIS! LAST ITEM
            if index < len(segments):
                self.create.drive_direct(0,0)
                if index != len(segments)-1 and (segments[index].color != segments[index+1].color):
                    print("COLOR PAUSE!")
                    self.time.sleep(1)
            index += 1

        print("done!") # completed moving through all the items...
        while True:
            pass
