"""
Module to control a pen holder (prismatic joint)
"""

from ..vrep import vrep as vrep
import math
import odometry



class PenHolder:
    """
    Class to control a virtual pen holder in V-REP.
    The pen holder is modeled as prismatic joint and the position is set directly.
    """
    def __init__(self, client_id):
        """Constructor.

        Args:
            client_id (integer): V-REP client id.
        """
        self._clientID = client_id
        # query objects
        rc, self._joint = vrep.simxGetObjectHandle(self._clientID, "Prismatic_joint", vrep.simx_opmode_oneshot_wait)
        print(rc, self._joint)
        # self.servo = Servo(number)
        self.odometry = odometry.Odometry()
        self.length = 0.08
        self.radius = 0.1175
        self.arm = self.radius+self.length
 
        print("created pen holder")






    def go_to(self, height):
        """Go to specified target height.

        Args:
            height (float): target height in cm
        """
        vrep.simxSetJointPosition(self._clientID, self._joint, height,
                                        vrep.simx_opmode_oneshot_wait)

    def set_color(self, r, g, b):
        """Set pen color (RGB).

        Args:
            r (float): red component (0 to 1)
            g (float): green component (0 to 1)
            b (float): blue component (0 to 1)
        """
        vrep.simxSetFloatSignal(self._clientID, 'paintingColorR', r,
            vrep.simx_opmode_oneshot_wait)
        vrep.simxSetFloatSignal(self._clientID, 'paintingColorG', g,
            vrep.simx_opmode_oneshot_wait)
        vrep.simxSetFloatSignal(self._clientID, 'paintingColorB', b,
            vrep.simx_opmode_oneshot_wait)

    def translate_coords(self, x, y):
        theta = self.odometry.theta
        y_ = y-arm*math.sin*(90-theta)
        x_ = x+arm*math.cos*(90-theta)
        return x_,y_

    def rotate_around_marker(self, base_speed, angle):
        print("starting rotation")
        wb = self.radius*2
        ratio = self.length/(self.length + wb)
        rw_speed = base_speed*ratio
        lw_speed = base_speed
        sector = angle/(2*math.pi)
        print(self.length + wb)
        circle_time = (2*math.pi)*(self.length + wb)/(.001*base_speed)
        sector_time = circle_time * sector
        return rw_speed, lw_speed, sector_time



