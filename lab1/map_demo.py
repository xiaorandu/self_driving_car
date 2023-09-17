import picar_4wd as fc
import time
from picar_4wd import servo
from obstacle_map import ObstacleMap
from Picar import Picar, Direction

FORWARD_SPEED = 10
BACKWARD_SPEED = 10
DIST_TO_OBSTACLE = 35
SERVO_OFFSET = 45 # customize to make the servo point straight forward at angle zero. If it is already, just set this to zero.

ANGLE_RANGE = 144
STEP = 18
us_step = STEP
#inital scan angle is set to 72
current_angle = 90
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []
angle_to_dist = {}


def demo_obstacle_map():
    servo.offset = 30
    servo.set_angle(0)
    obs_map = ObstacleMap(debug=True)
    obs_map.do_map()




if __name__ == "__main__":
    try: 
        demo_obstacle_map()
    finally: 
        fc.stop()
