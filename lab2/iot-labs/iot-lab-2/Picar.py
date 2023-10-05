import picar_4wd as fc
from enum import Enum
from picar_4wd import servo
from obstacle_map import ObstacleMap
from astar import astar
import time

FORWARD_SPEED = 10
SEC_PER_CM = .0425 # configure to make sure it only goes forward 1 cm.
BACKWARD_SPEED = 10
TURNING_SPEED = 100
TIME_TO_TURN_RIGHT_90 = .7 #in seconds
TIME_TO_TURN_LEFT_90 = 1
DIST_TO_OBSTACLE = 35
DISTANCE_OFFSET = 0 #-4.36 # offset to make sure objects are detected at accurate distance as measured from front of vehicle. They were being measured as being too far away.
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

normalize_direction = {
    Direction.EAST: {
        (0,1): (-1,0),
        (1,0): (0,1),
        (0,-1): (1,0),
        (-1,0): (0,-1)
    },
    Direction.SOUTH: {
        (0,1): (0,-1),
        (1,0): (-1,0),
        (0,-1): (0,1),
        (-1,0): (1,0)
    },
    Direction.WEST: {
        (0,1): (1,0),
        (1,0): (0,-1),
        (0,-1): (-1,0),
        (-1,0): (0,1)
    }
}


class Picar:
    def __init__(self, map_size: int = 100):
        servo.offset = SERVO_OFFSET
        servo.set_angle(0)
        self.servo_step = STEP

        self.forward_speed = FORWARD_SPEED
        self.sec_per_cm = SEC_PER_CM
        self.distance_offset = DISTANCE_OFFSET
        self.backward_speed = BACKWARD_SPEED
        self.turning_speed = TURNING_SPEED
        self.time_to_turn_right_90 = TIME_TO_TURN_RIGHT_90
        self.time_to_turn_left_90 = TIME_TO_TURN_LEFT_90


        self.obstacle_map = ObstacleMap(size=map_size)
        self.x_location = int(self.obstacle_map.size / 2)
        self.y_location = 0
        self.orientation = Direction.NORTH

        self.x_end = 99
        self.y_end = 80

        self.angle_to_dist = {}

    def move(self, direction, distance) -> None:
        if direction == Direction.NORTH:
            if self.orientation == Direction.NORTH:
                self.forward(distance)
            elif self.orientation == Direction.SOUTH:
                self.backward(distance)
            elif self.orientation == Direction.EAST:
                self.move_left(distance)
                self.orientation = Direction.NORTH
            elif self.orientation == Direction.WEST:
                self.move_right(distance)
                self.orientation = Direction.NORTH

        elif direction == Direction.SOUTH:
            if self.orientation == Direction.NORTH:
                self.backward(distance)
            elif self.orientation == Direction.SOUTH:
                self.forward(distance)
            elif self.orientation == Direction.EAST:
                self.move_right(distance)
                self.orientation = Direction.SOUTH
            elif self.orientation == Direction.WEST:
                self.move_left(distance)
                self.orientation = Direction.SOUTH

        elif direction == Direction.EAST:
            if self.orientation == Direction.NORTH:
                self.move_right(distance)
                self.orientation = Direction.EAST
            elif self.orientation == Direction.SOUTH:
                self.move_left(distance)
                self.orientation = Direction.EAST
            elif self.orientation == Direction.EAST:
                self.forward(distance)
            elif self.orientation == Direction.WEST:
                self.backward(distance)

        elif direction == Direction.WEST:
            if self.orientation == Direction.NORTH:
                self.move_left(distance)
                self.orientation = Direction.WEST
            elif self.orientation == Direction.SOUTH:
                self.move_right(distance)
                self.orientation = Direction.WEST
            elif self.orientation == Direction.EAST:
                self.backward(distance)
            elif self.orientation == Direction.WEST:
                self.forward(distance)
        self.update_location_dist(direction, distance)

    def forward(self, distance) -> None:
        fc.forward(self.forward_speed)
        time.sleep(self.sec_per_cm * distance)
        fc.stop()
    
    def backward(self, distance) -> None:
        fc.backward(self.backward_speed)
        time.sleep(self.sec_per_cm * distance)
        fc.stop()

    def stop(self) -> None:
        fc.stop()

    def turn_around(self):
        fc.turn_right(self.turning_speed)
        time.sleep(2.3)
        self.forward()

    def move_right(self, distance):
        fc.turn_right(self.turning_speed)
        time.sleep(self.time_to_turn_right_90)
        self.forward(distance)
        
    def move_left(self, distance):
        fc.turn_left(self.turning_speed)
        time.sleep(self.time_to_turn_left_90)
        self.forward(distance)
    
    def scan_env_and_map(self) -> None:
        self.angle_to_dist = {}
        cur_angle = min_angle
        while cur_angle <= max_angle:
            self.angle_to_dist[cur_angle] = fc.get_distance_at(cur_angle) + self.distance_offset
            cur_angle += self.servo_step

        self.obstacle_map.do_map(self.angle_to_dist)

    def rescan_and_reconcile_maps(self) -> list[tuple]:
        new_map = ObstacleMap(size=self.obstacle_map.size)

        self.x_end = int(new_map.size / 2) + (self.x_end - self.x_location)
        self.y_end = self.y_end - self.y_location

        # if transformed endpoint is out of bounds
        if not self.x_end < new_map.size:
            print(f"Transformed end location out of bounds. New x end: {self.x_end}, but Map size {new_map.size}")
            x_diff  = self.x_end - new_map.size
            new_map = ObstacleMap(size=new_map.size + x_diff + 1) # + 1 for buffer
        if not self.y_end < new_map.size:
            print(f"Transformed end location out of bounds. New y end: {self.y_end}, but Map size {new_map.size}")
            y_diff  = self.y_end - new_map.size
            new_map = ObstacleMap(size=new_map.size + y_diff + 1) # + 1 for buffer

        self.x_location = int(new_map.size / 2)
        self.y_location = 0
        self.obstacle_map = new_map
        self.scan_env_and_map()

        return self.find_path()
        
    
    def find_path(self) -> list[tuple]:
        # TODO: find end destination
        path = astar(self.x_location, self.y_location, self.x_end, self.y_end, self.obstacle_map.get_map()) #astar signature end_r and end_c are swapped
        print(f"Astar path:\t{path}")

        return path
    
    def get_direction(self, x_dest, y_dest) -> tuple[tuple, tuple]:
        to_steer = (x_dest - self.x_location, y_dest - self.y_location)
        # convert coords
        new_coords = normalize_direction[self.orientation][to_steer] if self.orientation != Direction.NORTH else to_steer
        return new_coords, to_steer
    
    def update_location(self, new_x: int, new_y: int) -> None:
        self.x_location += new_x
        self.y_location += new_y

    def update_location_dist(self, direction: int, distance: int) -> None:
        if direction == Direction.NORTH:
            self.y_location += distance

        elif direction == Direction.SOUTH:
            self.y_location -= distance

        elif direction == Direction.EAST:
            self.x_location += distance

        elif direction == Direction.WEST:
            self.x_location -= distance


    def update_orientation(self, x: int, y: int) -> None:
        self.orientation = coords_to_direction[x, y]

    def reached_goal(self) -> bool:
        return (self.x_end == self.x_location and self.y_end == self.y_location)

        