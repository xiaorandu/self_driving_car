import picar_4wd as fc
from enum import Enum
from picar_4wd import servo
from obstacle_map import ObstacleMap
from astar import astar
import time

FORWARD_SPEED = 10
FORWARD_WAIT = .05 # configure to make sure it only goes forward 1 cm.
BACKWARD_SPEED = 10
TURNING_SPEED = 70
DIST_TO_OBSTACLE = 35
DISTANCE_OFFSET = -5.36 # offset to make sure objects are detected at accurate distance as measured from front of vehicle. They were being measured as being too far away.
SERVO_OFFSET = 9 # customize to make the servo point straight forward at angle zero. If it is already, just set this to zero. 9 works for BR. Was 45.

ANGLE_RANGE = 144
STEP = 18
#inital scan angle is set to 72
current_angle = 90

# how far should the servo turn to the left? 0 is pointing forward.
max_angle = ANGLE_RANGE/2
# how far should the servo turn to the right?
min_angle = -ANGLE_RANGE/2
scan_list = []
angle_to_dist = {}


class Direction(Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


coords_to_direction = {
    (0,1): Direction.NORTH,
    (1,0): Direction.EAST,
    (0,-1): Direction.SOUTH,
    (-1,0): Direction.WEST,
}

direction_to_coords = {
    Direction.NORTH: (0,1),
    Direction.EAST: (1,0),
    Direction.SOUTH: (0,-1),
    Direction.WEST: (-1,0),
}


def normalize_direction(cur_orientation: Direction, dir_in: Direction) -> tuple:
    # Create a list of transformation tuples (rotate 90 degrees each step)
    transformations = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    # Get the index in the transformations list for the current orientation and the desired direction
    cur_orientation_index = transformations.index(direction_to_coords[cur_orientation])
    dir_in_index = transformations.index(direction_to_coords[dir_in])

    # Find the difference in indices to find how much we need to rotate
    index_diff = dir_in_index - cur_orientation_index

    # Adjust index_diff to find the shortest path to the new direction
    index_diff = (index_diff + 2) % 4 - 2

    # Get the new index based on the current orientation
    new_index = (cur_orientation_index + index_diff) % 4
    
    return transformations[new_index]

class Picar:
    def __init__(self):
        servo.offset = SERVO_OFFSET
        servo.set_angle(0)
        self.servo_step = STEP

        self.forward_speed = FORWARD_SPEED
        self.forward_wait = FORWARD_WAIT
        self.distance_offset = DISTANCE_OFFSET
        self.backward_speed = BACKWARD_SPEED
        self.turning_speed = TURNING_SPEED

        self.obstacle_map = ObstacleMap()
        self.x_location = int(self.obstacle_map.size / 2)
        self.y_location = 0
        self.orientation = Direction.NORTH

        self.angle_to_dist = {}


    def forward(self) -> None:
        fc.forward(self.forward_speed)
        time.sleep(self.forward_wait)
        fc.stop()
    
    def backward(self) -> None:
        fc.backward(self.backward_speed)

    def turn_right(self) -> None:
        fc.turn_right(self.forward_speed)

    def turn_left(self) -> None:
        fc.turn_left(self.forward_speed)

    def stop(self) -> None:
        fc.stop()

    def turn_around(self):
        fc.turn_right(self.turning_speed)
        time.sleep(2.5)
        self.forward()
        
    # def move_east(self):
    #     if self.orientation == Direction.NORTH:
    #         fc.turn_right(self.turning_speed)
    #         time.sleep(1)
    #         self.orientation = Direction.EAST
    #     self.forward()
    #     time.sleep(self.forward_wait)
    #     fc.stop()

    def move_right(self):
        fc.turn_right(self.turning_speed)
        time.sleep(1)
        self.forward()
        
    def move_left(self):
        fc.turn_left(self.turning_speed)
        time.sleep(1)
        self.forward()
     
    def move_front_right(self):
        self.turn_right()
        time.sleep(1)
        self.forward()
    
    def move_front_left(self):
        self.turn_left()
        time.sleep(1)
        self.forward()
    
    def move_back_right(self):
        self.turn_around()
        self.move_front_left()
        
    def move_back_left(self):
        self.turn_around()
        self.move_front_right()
    
    def scan_env_and_map(self) -> None:
        self.angle_to_dist = {}
        cur_angle = min_angle
        while cur_angle <= max_angle:
            self.angle_to_dist[cur_angle] = fc.get_distance_at(cur_angle) + self.distance_offset
            cur_angle += self.servo_step

        self.obstacle_map.do_map(self.angle_to_dist)
    
    def find_path(self) -> list[tuple]:
        # TODO: find end destination
        path = astar(self.x_location, self.y_location, 99, 50, self.obstacle_map.get_map())
        print(f"Astar path:\t{path}")

        return path
    
    def get_direction(self, x_dest, y_dest) -> tuple:
        to_steer = (x_dest - self.x_location, y_dest - self.y_location)
        print(f"Cur location { self.x_location} {self.y_location}")
        print(f"to steer: {to_steer}    x dest: {x_dest} y dest: {y_dest}")

        # convert coords
        new_coords = normalize_direction(
            cur_orientation=self.orientation,
            dir_in=coords_to_direction[to_steer],
        ) if self.orientation != coords_to_direction[to_steer] else to_steer
        return new_coords
    
    def update_location(self, new_x: int, new_y: int) -> None:
        self.x_location += new_x
        self.y_location += new_y

    def update_orientation(self, x: int, y: int) -> None:
        self.orientation = coords_to_direction[x, y]

        