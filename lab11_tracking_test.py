"""
Example code for the external tracking.
Use "python3 run.py --sim lab11_tracking_test" to execute
"""

import math
import math
import odometry
from pyCreate2 import create2


class Run:
    def __init__(self, factory):
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.odometry = odometry.Odometry()

        self.base_speed = 60

        # sd_{x,y,theta} and rate are only for simulation to change the noise and update rate respectively.
        # They are ignored on the robot.
        self.tracker = factory.create_tracker(1, sd_x=0.01, sd_y=0.01, sd_theta=0.01, rate=10)

    def fusePredict(self,odometry_data, r, alpha):
        predict_x = odometry_data.x
        predict_y = odometry_data.y
        predict_theta = odometry_data.theta

        

        if r is not None:
            print("odometry theta: %f" % predict_theta)
            print("camera theta: %f" % r["position"]["y"])
            predict_x = alpha*predict_x + (1-alpha)*(r["position"]["x"])
            predict_y = alpha*predict_y + (1-alpha)*(r["position"]["y"])
            predict_theta = alpha*predict_theta + (1-alpha)*(r["orientation"]["y"]) # given in radians...
            self.time.sleep(0.0)

        # Values can be found using variable_name["x"]
        #                           variable_name["y"]
        #                           variable_name["theta"]
        return {
            'x': predict_x,
            'y': predict_y,
            'theta': predict_theta
      }     

    def run(self):

        self.create.start()
        self.create.safe()

        # request sensors
        self.create.start_stream([
            create2.Sensor.LeftEncoderCounts,
            create2.Sensor.RightEncoderCounts,
        ])

        # setup to store predicted location
        p = None 
        r = self.tracker.query()
        for i in range(4):
            if p is not None:
                print("BEFORE")
                print(p["x"],p["y"],math.degrees(p["theta"]))

            # self.time.sleep(0.0)
            # r = self.tracker.query()

            self.create.drive_direct(self.base_speed, self.base_speed)
            self.time.sleep(10)
            self.create.drive_direct(self.base_speed*0.6, -1*0.6*self.base_speed)
            self.time.sleep(4);

            state = self.create.update()
            if state is not None:
                self.odometry.update(state.leftEncoderCounts, state.rightEncoderCounts)

            r = self.tracker.query()

            p = self.fusePredict(self.odometry, r, 0.5)
            print("AFTER")
            print(r)

            print(p["x"],p["y"],math.degrees(p["theta"]))
            print()

        while True:
            pass



