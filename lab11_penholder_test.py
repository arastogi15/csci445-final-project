"""
Example to use the pen holder
Use "python3 run.py --sim lab11_penholder_test" to execute
"""
import math
from pyCreate2.robot import pen_holder

from pyCreate2 import create2
import odometry
# import pd_controller2
import pid_controller



class Run:
    def __init__(self, factory):
        """Constructor.

        Args:
            factory (factory.FactoryCreate)
        """
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.penholder = factory.create_pen_holder()
        self.base_speed = 400
        self.pidTheta = pid_controller.PIDController(300, 5, 50, [-10, 10], [-200, 200], is_angle=True)
        self.pidDistance = pid_controller.PIDController(1000, 0, 50, [0, 0], [-200, 200], is_angle=False)
        self.odometry = odometry.Odometry()



    def run(self):
        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])


        # Set the color to green
        # the arguments are RGB ranging from 0 to 1
        # On the robot, this will wait for a human to
        # swap the pens.
        self.penholder.set_color(0.0, 1.0, 0.0)

        self.penholder.go_to(-0.025)

        # self.create.drive_direct(self.base_speed, self.base_speed)
        # self.time.sleep(5)
        # self.create.drive_direct(0, 0)

        # self.penholder.go_to(0.0)

        waypoints = [
            [2.0, 0.0],
            [3.0, 2.0],
            [2.5, 2.0],
            [0.0, 1.5],
            [0.0, 0.0]
        ]

        w_translated = []

        self.penholder.go_to(0)
        for w in waypoints
            # self.penholder.go_to(-.025)
            w_translated.append(self.penholder.translate_coords(w))
            # self.penholder.go_to(0)

        print(w_translated)

        start_time = self.time.time()


        for waypoint in w_translated:
            goal_theta = math.atan2(waypoint[1] - self.odometry.y, waypoint[0] - self.odometry.x)
            print("going to: ", waypoint)
            print("rotate to: ", goal_theta)
            self.penholder.rotate_around_marker(self.base_speed, goal_theta)
            while True:
                state = self.create.update()
                if state is not None:
                    self.penholder.go_to(-.025)
                    self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)
                    goal_theta = math.atan2(waypoint[1] - self.odometry.y, waypoint[0] - self.odometry.x)
                    theta = math.atan2(math.sin(self.odometry.theta), math.cos(self.odometry.theta))
                    # f.write("{},{},{}\n".format(self.time.time() - start_time, theta, goal_theta))
                    print("[{},{},{}]".format(self.odometry.x, self.odometry.y, math.degrees(self.odometry.theta)))

                    output_theta = self.pidTheta.update(self.odometry.theta, goal_theta, self.time.time())
                        
                    # self.create.drive_direct(int(self.base_speed), int(self.base_speed))
                    print("driving")

                    # base version:
                    # self.create.drive_direct(int(self.base_speed+output_theta), int(self.base_speed-output_theta))

                    # improved version 1: stop if close enough to goal 


                    distance = math.sqrt(math.pow(waypoint[0] - self.odometry.x, 2) + math.pow(waypoint[1] - self.odometry.y, 2))
                    output_distance = self.pidDistance.update(0, distance, self.time.time())
                    if distance < 0.1:
                        self.penholder.go_to(0)
                        self.create.drive_direct(0, 0)
                        break
                    print("driving")
                    self.create.drive_direct(int(output_theta + output_distance), int(-output_theta + output_distance))

                    





        # r, l, time = self.penholder.rotate_around_marker(self.base_speed, 2*math.pi)
        # print("speed vals: ",r,l, time)
        # self.create.drive_direct(r, l)
        # self.time.sleep(time)
        # self.create.drive_direct(self.base_speed, self.base_speed)

        self.create.stop()
