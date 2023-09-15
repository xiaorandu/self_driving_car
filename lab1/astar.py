import heapq
from obstacle_map import ObstacleMap

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
class Node:
    def __init__(self, row, col, val):
        self.row = row
        self.col = col
        self.val = val
        self.g = float('inf') # g score, cost so far
        self.f = float('inf') # f score, total estimated cost of path
        self.prev = None  # the prev visited node

def astar(start_r, start_c, end_r, end_c, obstacle_map):
    nodes = get_nodes(obstacle_map)
    start, end = nodes[start_r][start_c], nodes[end_r][end_c]
    start.g, start.f = 0, get_dist(start, end) #get start node's g and f scores
    open_set = [(start.f, start.g, (start.row, start.col, start))]
    visited = {start:start.f}
    
    while open_set:
        _, g_score, curr = heapq.heappop(open_set) #pop the one with the smallest f score

        if curr[2] == end: #reach the distination
            break 
        neighbors = get_neighbors(curr[2], nodes)
        for neighbor in neighbors:
            if neighbor.val == 1: #check if it is an obstacle
                continue
            dist_to_neighbor = g_score + 1
            if dist_to_neighbor >= neighbor.g:
                continue
            
            neighbor.prev = curr[2]
            neighbor.g = dist_to_neighbor
            neighbor.f = dist_to_neighbor + get_dist(neighbor, end)
            
            if neighbor in visited:
                # update the node with smaller f score if it've been visited
                if neighbor.f < visited[neighbor]:
                    visited[neighbor] = neighbor.f
                    heapq.heappush(open_set,(neighbor.f, neighbor.g, (neighbor.row, neighbor.col, neighbor)))
                    
            else:
                visited[neighbor] = neighbor.f
                heapq.heappush(open_set,(neighbor.f, neighbor.g, (neighbor.row, neighbor.col, neighbor)))
       
    return get_path(end)

#takes in a 2D array integers and returns a 2D array of Node objects
def get_nodes(map):
    nodes = []
    for i, r in enumerate(map):
        nodes.append([])
        for j, val in enumerate(r):
            nodes[i].append(Node(i, j, val))

    return nodes

#calculate the manhattan distance
def get_dist(curr, end):
    dx = abs(curr.row - end.row)
    dy = abs(curr.col - end.col)
    
    return dx + dy

#get curr node's neighbor list
def get_neighbors(curr, nodes):
    neighbors = [] #append the left, right, top and bottom neighbors
    
    for dx, dy in DIRECTIONS:
        next_x, next_y = curr.row + dx, curr.col + dy
        if 0 <= next_x < len(nodes) and 0 <= next_y < len(nodes[0]):
            neighbors.append(nodes[next_x][next_y])
   
    return neighbors

#construct the path
def get_path(end):
    if not end.prev:
        return []
    
    curr = end
    path = [(curr.row,curr.col,curr.f)]
    while curr.prev:
        path.append((curr.prev.row,curr.prev.col,curr.prev.f))
        curr = curr.prev
        
    return path[::-1]

if __name__ == "__main__":
    obstacle_map = ObstacleMap(10).obstacle_map
    print(f"obs map:\n{obstacle_map}")
    astar(0, 0, 5, 5, obstacle_map)

    
