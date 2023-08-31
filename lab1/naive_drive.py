import picar_4wd as fc
import time
from picar_4wd import servo

FORWARD_SPEED = 15
BACKWARD_SPEED = 10
DIST_TO_OBSTACLE = 30

def naive_drive():
    servo.set_angle(0)
    
    while True:
        scan_list = fc.scan_step(DIST_TO_OBSTACLE)
        if not scan_list:
            continue
        print("scan_list:", scan_list)
        
        #scan angular range 54°~126°
        scan_range = scan_list[3:8] 
        print(scan_range)
        
        if scan_range == [2, 2]:
            fc.forward(FORWARD_SPEED)
            
        elif scan_range != [2,2,2,2,2]:
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