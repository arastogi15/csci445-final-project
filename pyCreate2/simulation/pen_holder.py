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

    # Takes in marker coordinates and maps them to what robot should be going to
    # NOTE: just call this on list of waypoints (probs should work)
    def translate_coords_to_robot(self, w):
        #y - armcos(theta); x - armsin(theta)
        curr_theta = self.odometry.theta
        distance_to_w = math.sqrt(math.pow(w[0] - self.odometry.x, 2) + math.pow(w[1] - self.odometry.y, 2))
        distance_to_actual = math.sqrt(math.pow(distance_to_w, 2)  - math.pow(self.arm, 2))
        total_theta = curr_theta + math.atan2(w[1] - self.odometry.y, w[0] - self.odometry.x)
        x_ = self.odometry.x + distance_to_actual * math.cos(total_theta)
        y_ = self.odometry.y + distance_to_actual * math.sin(total_theta)
        return [x_,y_]

    # Takes in base speed of turning and and rotates clockwise around the set point. 
    # NOTE: may need to do some work on figuring out how much to turn the robot
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



