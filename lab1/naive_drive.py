import picar_4wd as fc
import time
from picar_4wd import servo

FORWARD_SPEED = 15
BACKWARD_SPEED = 10
DIST_TO_OBSTACLE = 30

ANGLE_RANGE = 180
STEP = 18
us_step = STEP
#inital scan angle is set to 90
current_angle = 90
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []

def scan_step(ref):
    global scan_list, us_step, current_angle
    current_angle -= us_step 
    if current_angle >= max_angle: 
        current_angle = max_angle
        us_step = STEP
    elif current_angle <= min_angle: 
        current_angle = min_angle 
        us_step = -STEP
    status = fc.get_status_at(current_angle, ref1=ref)
   
    scan_list.append(status)
    if current_angle == min_angle or current_angle == max_angle:
        if us_step > 0:
            scan_list.reverse()
        tmp = scan_list.copy()
        scan_list = []
        return tmp
    else:
        return False

def naive_drive():
    servo.set_angle(0)
    
    while True:
        scan_list = scan_step(DIST_TO_OBSTACLE)
        if not scan_list:
            continue
        print("scan_list:", scan_list)
        
        #scan angular range 54°~126°
        scan_range = scan_list[3:8] 
        print("scan_list:", scan_range)
      
        if scan_range != [2,2,2,2,2]:
            fc.stop()
            fc.backward(BACKWARD_SPEED)
            time.sleep(0.2)
            
            #get the rough location of the obstacle
            obstacle_loc_range = [i for i, num in enumerate(scan_range) if num < 2]
            obstacle_cnt = sum(obstacle_loc_range) // 2
            # if the obstacle is near its left side, turn right, else turn left
            fc.turn_right(FORWARD_SPEED) if obstacle_cnt < len(scan_range) // 2 else fc.turn_left(FORWARD_SPEED)
       
        else:
            fc.forward(FORWARD_SPEED)

if __name__ == "__main__":
    try: 
        naive_drive()
    finally: 
        fc.stop()
