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

DISTANCE_OFFSET = -5.36
SERVO_STEP = 18


def demo_obstacle_map():
    servo.offset = 45
    servo.set_angle(0)
    obs_map = ObstacleMap(debug=True)
    
    angle_to_dist = {}
    cur_angle = min_angle
    while cur_angle <= max_angle:
        angle_to_dist[cur_angle] = fc.get_distance_at(cur_angle) + DISTANCE_OFFSET
        cur_angle += SERVO_STEP
    
    obs_map.do_map(angle_to_dist)
    mat = obs_map.get_map()
    
    # print the matrix
    for row in mat:
        print(' '.join(map(str, row)))




if __name__ == "__main__":
    try: 
        demo_obstacle_map()
    finally: 
        fc.stop()
