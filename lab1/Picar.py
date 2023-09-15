import picar_4wd as fc
from enum import Enum
from picar_4wd import servo
from obstacle_map import ObstacleMap
from astar import astar

FORWARD_SPEED = 10
BACKWARD_SPEED = 10
DIST_TO_OBSTACLE = 35
SERVO_OFFSET = 20 # customize to make the servo point straight forward at angle zero. If it is already, just set this to zero.

ANGLE_RANGE = 144
STEP = 18
#inital scan angle is set to 72
current_angle = 90
max_angle = ANGLE_RANGE/2
min_angle = -ANGLE_RANGE/2
scan_list = []
angle_to_dist = {}

class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = 3
    WEST = 4


coords_to_direction ={
    (0, 0): Direction.NORTH,
    (0, 1): Direction.EAST,
    (-1, 0): Direction.SOUTH,
    (0, -1): Direction.WEST,
}

class Picar:
    def __init__(self):
        servo.offset = SERVO_OFFSET
        servo.set_angle(0)
        self.servo_step = STEP

        self.forward_speed = FORWARD_SPEED
        self.backward_speed = BACKWARD_SPEED


        self.obstacle_map = ObstacleMap()
        self.x = int(self.obstacle_map.size / 2)
        self.y = 0
        self.orientation = Direction.NORTH
        self.angle_to_dist = {}

        self.direction_map = {
            Direction.NORTH: {(0, 1): Direction.EAST, (1, 0): Direction.SOUTH, (0, -1): Direction.WEST},
            Direction.EAST:  {(0, 1): Direction.SOUTH, (1, 0): Direction.WEST, (0, -1): Direction.NORTH},
            Direction.SOUTH: {(0, 1): Direction.WEST, (1, 0): Direction.NORTH, (0, -1): Direction.EAST},
            Direction.WEST:  {(0, 1): Direction.NORTH, (1, 0): Direction.EAST, (0, -1): Direction.SOUTH},
        }


    # TODO: make these functions so they go for proper distance 
    # ie --> turn right turns 90 degrees

    def forward(self) -> None:
        fc.forward(self.forward_speed)
    
    def backward(self) -> None:
        fc.backward(self.backward_speed)

    def turn_right(self) -> None:
        fc.turn_right(self.forward_speed)

    def turn_left(self) -> None:
        fc.turn_left(self.forward_speed)

    def stop(self) -> None:
        fc.stop()

    def change_orientation(self, dir_to_steer: Direction) -> None:
        self.orientation = self.direction_map[self.orientation][dir_to_steer]

    def scan_env_and_map(self) -> None:
        self.angle_to_dist = {}
        cur_angle = min_angle
        while cur_angle <= max_angle:
            self.angle_to_dist[cur_angle] = fc.get_distance_at(cur_angle)
            cur_angle += self.servo_step

        self.obstacle_map.do_map(self.angle_to_dist)
    
    def find_path(self, end_row: int, end_col: int) -> list[tuple]:
        # TODO: find end destination
        path = astar(self.x, self.y, end_row, end_col, self.obstacle_map.get_map())
        print(f"Astar path:\t{path}")

        return path
    
    def get_direction(self, x_dest, y_dest) -> Direction:
        x_diff = int(x_dest - self.x)
        y_diff =  int(y_dest - self.y)
        return coords_to_direction[x_diff, y_diff]
    
    def update_location(self, to_steer: Direction) -> None:
        self.x += to_steer[0]
        self.y += to_steer[1]
        self.change_orientation(to_steer)