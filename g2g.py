from pyCreate2 import create2
import math
import odometry
import lab11_plot
from lab11_plot import myLine
class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.servo = factory.create_servo()
        self.odometry = odometry.Odometry()

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

        index = 0
        # points = [ [1,0, "red"], [1,1,"blue"], [2,1,"blue"]]
        # points = [ [1,0, "red"], [1,1,"red"]]
        points = []
        iFile = open("hardOutput.txt", "r")
        for line in iFile:
            words = line.split()
            myTempLine = myLine(words[0], words[1], words[2], words[3], words[4], words[5])
            points.append(myTempLine)
        for i in points:
            print(i.xStart, i.yStart, i.xEnd, i.yEnd, i.color, i.type)

        print("START")
        print(self.odometry.x, self.odometry.y)
        # move_forward = False
        # move_theta = False
        while self.time.time() < end_time and index < len(points):

            state = self.create.update()
            self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)

            if state is None:
                break

            print("test")
            goal_x = float(points[index].xEnd)
            goal_y = float(points[index].yEnd)

            print(goal_x)
            print(goal_y)
            print("odometry")
            print(self.odometry.x)
            print(self.odometry.y)
            print(self.odometry.theta)

            theta_error = self.odometry.theta - math.atan2(goal_y - self.odometry.y, goal_x - self.odometry.x) % (2*3.14)
            dist_error = math.sqrt(math.pow(goal_x - self.odometry.x, 2) + math.pow(goal_y - self.odometry.y, 2))
            print("theta error: %f" % theta_error)
            print("dist error: %f" % dist_error)

            while abs(theta_error) > 0.05:
                state = self.create.update()
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                theta_error = math.atan2(goal_y - self.odometry.y, goal_x - self.odometry.x) - self.odometry.theta
                clamped_theta_error = max(min(60*theta_error, 100), -100)
                self.create.drive_direct(int(clamped_theta_error), int(-clamped_theta_error))
                self.time.sleep(0.2)

            while dist_error > 0.1:
                state = self.create.update()
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                print("dist error: %f" % dist_error)
                dist_error = math.sqrt(math.pow(goal_x - self.odometry.x, 2) + math.pow(goal_y - self.odometry.y, 2))
                clamped_dist_error = max(min(300*dist_error, 100), -100)
                self.create.drive_direct(int(clamped_dist_error), int(clamped_dist_error))
                self.time.sleep(0.01)
            

            if index < len(points)-1 and (points[index].color != points[index+1].color):
                self.create.drive_direct(0,0)
                print("COLOR PAUSE!")
                self.time.sleep(8)
            index += 1

        print("done!") # completed moving through all the items...
