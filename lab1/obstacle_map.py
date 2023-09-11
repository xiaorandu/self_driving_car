import numpy as np

class ObstacleMap:
    """
    Mantains a map of the environment by populating a 2d array while moving forward
    """
    def __init__(self, size: int = 100) -> None:
        self.size = size
        self.update = False
        self.obstacle_map = np.zeros((size, size), dtype=int)

    def set_update(self, to_set: bool) -> None:
        self.update = to_set

    def reset_map(self) -> None:
        print(f"Resetting obastacle map\n{self.obstacle_map}")
        self.obstacle_map = np.zeros((self.size, self.size), dtype=int)

    def map(self, angle_to_dist: dict) -> None:
        if self.update:
            new_points = []
            for angle, distance in angle_to_dist.items():
                if distance >= 0:
                    # Convert polar coordinates to Cartesian coordinates
                    # x = int(distance * np.sin(np.radians(angle)))
                    # y = int(distance * np.cos(np.radians(angle)))
                    # FIXME: should this be done with radians???
                    x = int((self.size / 2) + int(distance * np.sin(angle)))
                    y = int(distance * np.cos(angle))
                    new_points.append((x, y))
                    
                    # Ensure the coordinates are within the bounds of the array
                    if 0 <= x < self.size and 0 <= y < self.size:
                        # Mark the obstacle position on the map
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