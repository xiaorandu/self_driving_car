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


#returns a 1 for turn right, 0 for turn left.
def more_space_right(arr):
    # Initialize counts
    x = y = 0

    # Count 2's from the end until a 0 or 1 is encountered
    for i in reversed(arr):
        if i == 2:
            x += 1
        else:
            break

    # Count 2's from the beginning until a 0 or 1 is encountered
    for i in arr:
        if i == 2:
            y += 1
        else:
            break

    # Compare counts and return result
    if x >= y:
        return 1 #turn right
    else:
        return 0 #turn left

def scan_step(ref):
    global scan_list, angle_to_dist, us_step, current_angle
    current_angle -= us_step 
    if current_angle >= max_angle: 
        current_angle = max_angle
        us_step = STEP
    elif current_angle <= min_angle: 
        current_angle = min_angle 
        us_step = -STEP

    angle_to_dist[current_angle] = fc.get_distance_at(current_angle)
    cur_status = fc.get_status_at(current_angle, ref1=ref)
    scan_list.append(cur_status)


    if current_angle == min_angle or current_angle == max_angle:
        if us_step > 0:
            scan_list.reverse()
            scan_list.pop(0)
            scan_list.append(2)
        scan_copy = scan_list.copy()
        dist_copy = angle_to_dist.copy()
        scan_list = []
        angle_to_dist = {}
        return (scan_copy, dist_copy)
    else:
        return (None, None)

def naive_drive():
    servo.offset = SERVO_OFFSET
    servo.set_angle(0)

    obstacle_map = ObstacleMap(size=100, debug=True)
    
    while True:
        scan_list, angle_to_dist = scan_step(DIST_TO_OBSTACLE)
        if not scan_list:
            continue
        
        
        #scan angular range 54° through -54°
        scan_range = scan_list[0:7] 
        print(f"scan_range:\t{scan_range}")
      
        if 1 in scan_range or 0 in scan_range:
            fc.stop()
            fc.backward(BACKWARD_SPEED)
            time.sleep(0.2)
            
            # which side of the obstacle can we see more around?
            if more_space_right(scan_range):
                fc.turn_right(FORWARD_SPEED)
            else:
                fc.turn_left(FORWARD_SPEED)
       
        else:
            fc.forward(FORWARD_SPEED)

def avoid_obstacles():
    car = Picar()
    car.scan_env_and_map()
    path = car.find_path(end_row=50, end_col=99)
    print(f"Moves to perform: {len(path)}")

    for tup in path[1:]:
        print(f"To move: {tup}")
        dir_to_steer, steer_coords = car.get_direction(tup[0], tup[1])
        print(f"direction: {dir_to_steer}\nsteer_cords: {steer_coords}")
        
        # FIXME: none of these have been checked
        if dir_to_steer == Direction.NORTH:
            car.forward()
        elif dir_to_steer == Direction.EAST:
            car.turn_right()
            time.sleep(1)
            car.forward()
        elif dir_to_steer == Direction.WEST:
            car.turn_left()
            time.sleep(1)
            car.forward()
        
        car.update_location(steer_coords)
        time.sleep(.1)
        
        




if __name__ == "__main__":
    try: 
        # naive_drive()
        avoid_obstacles()
    finally: 
        fc.stop()
