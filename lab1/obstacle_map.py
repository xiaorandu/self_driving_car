import numpy as np
import sys

CLEARANCE = 10
class ObstacleMap:
    """
    Mantains a map of the environment by populating a 2d array while moving forward
    """
    def __init__(self, size: int = 100, debug: bool = False) -> None:
        self.size = size
        self.debug = debug
        self.obstacle_map = np.zeros((size, size), dtype=int)
        self.clearance = CLEARANCE

        if self.debug:
            import sys
            np.set_printoptions(threshold=sys.maxsize)

    @DeprecationWarning
    def set_update(self, to_set: bool) -> None:
        self.update = to_set

    def reset_map(self) -> None:
        if self.debug:
            print(f"Resetting obstacle map\n{self.obstacle_map}")
        self.obstacle_map = np.zeros((self.size, self.size), dtype=int)

    def get_map(self):
        return self.obstacle_map


    def do_map(self, angle_to_dist: dict) -> None:
        new_points = []
        obstacles = []
        for angle, distance in angle_to_dist.items():
            if distance >= 0:
                #convert angles from degrees to radians
                rad = np.radians(angle)
                x = int((self.size / 2) - int(distance * np.sin(rad)))
                y = int(distance * np.cos(rad))
                
                # Ensure the coordinates are within the bounds of the array
                if 0 <= x < self.size and 0 <= y < self.size:
                    new_points.append((x, y))
                    self.obstacle_map[x][y] = 1
            else:
                new_points.append((None, None))

        for i in range(len(new_points) - 1):
            x1, y1 = new_points[i]
            x2, y2 = new_points[i + 1]

            if None in [x1, y1, x2, y2]:
                continue

            # num= number of points to generate on each line
            x_line = np.linspace(x1, x2, num=100)
            y_line = np.linspace(y1, y2, num=100)

            for x, y in zip(x_line, y_line):
                self.obstacle_map[int(x)][int(y)] = 1
                obstacles.append((int(x), int(y)))

        #TODO: remove duplicates from obstacles array.    
        self.add_clearance(self.clearance, obstacles, self.obstacle_map)
    
    #add clearance to the obstacles

    # extend every obstacle coord by CLEARANCE in x and y.
    # if obstacle detected at angle 0.0 with distance 20 (x==50) this will add obstacle entries to the grid from x==48-52 y==18-22 if CLEARANCE is set to 2.
    def add_clearance(self, clearance, obstacles, obstacle_map):
        clearance_list = []
        for i in range(-clearance, clearance + 1):
            for j in range(-clearance, clearance + 1):
                clearance_list.append((i, j))
        
        for obstacle in obstacles:
            for c in clearance_list:
                x, y = obstacle[0] + c[0], obstacle[1] + c[1]
                if 0 <= x < self.size and 0 <= y < self.size:
                    obstacle_map[x][y] = 1
        
        return obstacle_map
