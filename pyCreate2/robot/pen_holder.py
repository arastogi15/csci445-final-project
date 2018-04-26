"""
Module to control a pen holder.
"""

from . import Servo
import math
import odometry

class PenHolder:
    def __init__(self, number, radius, length):
        self.servo = Servo(number)
        self.arm = radius+length
        self.odometry = odometry.Odometry()
        self.length = length
        self.radius = radius
        print("created pen holder")


    def go_to(self, height):
        """Go to specified target height.

        Args:
            height (float): target height in cm
        """
        self.servo.go_to(height * 1000)

    def set_color(self, r, g, b):
        """Set pen color (RGB).

        Args:
            r (float): red component (0 to 1)
            g (float): green component (0 to 1)
            b (float): blue component (0 to 1)
        """
        input('Press [Enter] after you changed the pen color to ({},{},{})'.format(r, g, b))

    def translate_coords(self, w):
        theta = self.odometry.theta
        y_ = w[1]-arm*math.sin*(90-theta)
        x_ = w[0]+arm*math.cos*(90-theta)
        return [x_,y_]

    def rotate_around_marker(base_speed, angle):
        wb = self.radius*2
        ratio = self.length/(self.length + wb)
        rw_speed = base_speed*ratio
        lw_speed = base_speed
        sector = angle/(2*math.pi)
        circle_time = (2*math.pi)*(self.length + wb)/base_speed
        sector_time = circle_time * sector
        return rw_speed, lw_speed, sector_time






