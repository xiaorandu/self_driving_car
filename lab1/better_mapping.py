import picar_4wd as fc
import time
from picar_4wd import servo
from obstacle_map import ObstacleMap
from Picar import Picar, Direction
import os

# packages needed for detect_objects
import argparse
import sys
import time
import cv2
from tflite_support.task import core
from tflite_support.task import processor
from tflite_support.task import vision
import object_detection.utils
from multiprocessing import Process, Value

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

# object detection settings
MODEL = '/home/bruffrid/self_driving_car/lab1/object_detection/efficientdet_lite0.tflite'
CAMERA_ID = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
NUM_THREADS = 4
ENABLE_EDGE_TPU = False


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

def route_from_path(path, car):
    route = [] # 
    direction = Direction.NORTH
    distance = 0 # distance to move in cm
    prev = (car.x_location, car.y_location)

    for tup in path[1:]:
        # subtract the current location tuple from the previous to see which value has changed x or y.
        dir = tuple(map(lambda i, j: i - j, (tup[0], tup[1]), prev))
        prev = (tup[0], tup[1]) # update prev to current

        x = dir[0]
        y = dir[1]

        if x == 0:
            if y > 0: #move north
                if direction != Direction.NORTH:
                    if distance > 0:
                        route.append((direction, distance))
                    direction = Direction.NORTH
                    distance = 0
                distance += 1
            elif y == 0: # end of path
                if distance > 0:
                    route.append((direction, distance))
            else: #move south
                if direction != Direction.SOUTH:
                    if distance > 0:
                        route.append((direction, distance))
                    direction = Direction.SOUTH
                    distance = 0
                distance += 1
        
        elif y == 0:
            if x > 0: # move east
                if direction != Direction.EAST:
                    if distance > 0:
                        route.append((direction, distance))
                    direction = Direction.EAST
                    distance = 0
                distance += 1
            else: # move west
                if direction != Direction.WEST:
                    if distance > 0:
                        route.append((direction, distance))
                    direction = Direction.WEST
                    distance = 0
                distance += 1

    if distance > 0:
        route.append((direction, distance))
    return route

def avoid_obstacles(stop):
    car = Picar(map_size=100)
    car.scan_env_and_map()
    path = car.find_path()
    #print('move process id:', os.getpid())

    #car.move(Direction.NORTH, 5)
    #car.move(Direction.EAST, 1)
    #car.move(Direction.WEST, 1)

    route = route_from_path(path, car)

    #while not car.reached_goal():
    #    direction, distance = route[0]
    #    car.move(direction, distance)
    #    new_path = car.rescan_and_reconcile_maps()
    #    route = route_from_path(new_path, car)

        # account for bad reading
    #    if not route and not car.reached_goal():
    #        new_path = car.rescan_and_reconcile_maps()
    #        route = route_from_path(new_path, car)

    #fc.stop()
    #print(f"Success, you drove to the destination")

    for dir_dist in route:
        direction = dir_dist[0]
        distance = dir_dist[1]
        if stop.value == 1:
            # pause for 5 seconds if it sees a stop sign.
            time.sleep(5)
        car.move(direction, distance)
        


def detect_objects(model: str, camera_id: int, width: int, height: int, num_threads: int,
        enable_edgetpu: bool, stop) -> None:
    """Continuously run inference on images acquired from the camera.

    Args:
        model: Name of the TFLite object detection model.
        camera_id: The camera id to be passed to OpenCV.
        width: The width of the frame captured from the camera.
        height: The height of the frame captured from the camera.
        num_threads: The number of CPU threads to run the model.
        enable_edgetpu: True/False whether the model is a EdgeTPU model.
    """
    #print('obj process id:', os.getpid())

    # Variables to calculate FPS
    counter, fps = 0, 0
    start_time = time.time()
    fps_avg_frame_count = 10

    # Start capturing video input from the camera cv2.CAP_GSTREAMER
    cap = cv2.VideoCapture(camera_id, cv2.CAP_V4L2, (cv2.CAP_PROP_HW_ACCELERATION, cv2.VIDEO_ACCELERATION_ANY))
    #print(cv2.getBuildInformation())
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    # Initialize the object detection model
    base_options = core.BaseOptions(
        file_name=model, use_coral=enable_edgetpu, num_threads=num_threads)
    detection_options = processor.DetectionOptions(
        max_results=3, score_threshold=0.3)
    options = vision.ObjectDetectorOptions(
        base_options=base_options, detection_options=detection_options)
    detector = vision.ObjectDetector.create_from_options(options)

    # Continuously capture images from the camera and run inference
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            sys.exit(
                'ERROR: Unable to read from webcam. Please verify your webcam settings.'
            )

        counter += 1
        image = cv2.flip(image, -1) # -1 flips the image horizontally and vertically. 1 flips horizontally. 0 flips vertically.

        # Convert the image from BGR to RGB as required by the TFLite model.
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Create a TensorImage object from the RGB image.
        input_tensor = vision.TensorImage.create_from_array(rgb_image)

        # Run object detection estimation using the model.
        detection_result = detector.detect(input_tensor)

        # Calculate the FPS
        if counter % fps_avg_frame_count == 0:
            end_time = time.time()
            fps = fps_avg_frame_count / (end_time - start_time)
            start_time = time.time()

        # Show the FPS
        fps_text = 'FPS = {:.1f}'.format(fps)
        #print(fps_text)
        stop.value = 0

        # Detect specific objects
        for detection in detection_result.detections:
            category = detection.categories[0]
            category_name = category.category_name

            # PERSON
            if category.index == 0 and category.score > .75:
                # stop until person is no longer detected
                #print('Car detects a person.')
                pass

            # TRAFFIC LIGHT
            if category.index == 9 and category.score > .75:
                pass

            # STOP SIGN
            if category.index == 12 and category.score > .75:
                #sees a stop sign.
                #print('Car detects a stop sign.')
                stop.value = 1

    cap.release()

if __name__ == "__main__":
    try: 
        stop = Value('b', 0)
        #print('parent process id:', os.getpid())

        p1 = Process(target = avoid_obstacles, args=(stop,))
        p1.start()
        p2 = Process(target = detect_objects, args = (MODEL, CAMERA_ID, FRAME_WIDTH, FRAME_HEIGHT, NUM_THREADS, ENABLE_EDGE_TPU, stop,))
        p2.daemon = True # stop this process once p1 finishes.
        p2.start()
        p1.join() # don't stop execution of parent and daemon processes until p1 finishes.

    finally: 
        fc.stop()
