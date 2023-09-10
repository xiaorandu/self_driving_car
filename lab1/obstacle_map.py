import numpy as np


class ObstacleMap:
    def __init__(self, size: int = 100) -> None:
        self.size = size
        self.update = False
        self.obstacle_map = np.zeros((size, size), dtype=int)

    def set_update(self, to_set: bool) -> None:
        self.update = to_set

    def map(self, angle_to_dist: dict) -> None:
        if self.update:
            for angle, distance in angle_to_dist.items():
                print(f"angle:\t{angle}")
                if distance:
                    # Convert polar coordinates to Cartesian coordinates
                    # x = int(distance * np.sin(np.radians(angle)))
                    # y = int(distance * np.cos(np.radians(angle)))
                    # TODO: should this be done with radians???
                    x = int(distance * np.sin(angle))
                    y = int(distance * np.cos(angle))
                    print(f"x {x}")
                    print(f"y {y}")
                    
                    # Ensure the coordinates are within the bounds of the array
                    if 0 <= x < 100 and 0 <= y < 100:
                        # Mark the obstacle position on the map
                        self.obstacle_map[x][y] = 1