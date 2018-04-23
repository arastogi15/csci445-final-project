"""
Example to use the pen holder
Use "python3 run.py --sim lab11_penholder_test" to execute
"""
import math
from pyCreate2.robot import pen_holder

class Run:
    def __init__(self, factory):
        """Constructor.

        Args:
            factory (factory.FactoryCreate)
        """
        self.create = factory.create_create()
        self.time = factory.create_time_helper()
        self.penholder = factory.create_pen_holder()
        self.base_speed = 100

    def run(self):
        self.create.start()
        self.create.safe()

        # Set the color to green
        # the arguments are RGB ranging from 0 to 1
        # On the robot, this will wait for a human to
        # swap the pens.
        self.penholder.set_color(0.0, 1.0, 0.0)

        self.penholder.go_to(-0.025)

        self.create.drive_direct(self.base_speed, self.base_speed)
        self.time.sleep(5)
        self.create.drive_direct(0, 0)

        # self.penholder.go_to(0.0)

        r, l, time = self.penholder.rotate_around_marker(self.base_speed, 2*math.pi)
        print("speed vals: ",r,l, time)
        self.create.drive_direct(23.5, l)
        self.time.sleep(time)
        self.create.drive_direct(self.base_speed, self.base_speed)

        self.create.stop()
