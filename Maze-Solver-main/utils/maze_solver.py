import imageio
from heapq import heappush, heappop
from utils.visualization import visualize_maze_animated
def find_start_and_end(reduced_img):
    rows, cols = reduced_img.shape

    top_boundary = [(0, col) for col in range(cols) if reduced_img[0, col] == 1]
    bottom_boundary = [(rows - 1, col) for col in range(cols) if reduced_img[rows - 1, col] == 1]
    left_boundary = [(row, 0) for row in range(rows) if reduced_img[row, 0] == 1]
    right_boundary = [(row, cols - 1) for row in range(rows) if reduced_img[row, cols - 1] == 1]

    boundary_points = top_boundary + bottom_boundary + left_boundary + right_boundary

    if len(boundary_points) < 2:
        raise ValueError("Not enough boundary points to define start and end points.")

    start = boundary_points[0]
    end = boundary_points[-1]

    return start, end

def a_star_algorithm_animated(maze, start, end):
    rows, cols = maze.shape
    frames = []
    traversal = []
    path_nodes = []

    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    open_set = []
    heappush(open_set, (0 + heuristic(start, end), 0, start))
    came_from = {}
    g_score = {start: 0}
    step_count = 0

    while open_set:
        _, current_g, current = heappop(open_set)
        traversal.append(current)
        step_count += 1

        if step_count % 40 == 0:
            frame = visualize_maze_animated(maze, traversal, path_nodes, start, end)
            frames.append(frame)

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            path_nodes.extend(path)

            for i in range(1, len(path) + 1):
                frame = visualize_maze_animated(maze, traversal, path[:i], start, end, final_path=True)
                frames.append(frame)

            return path, frames, traversal

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dr, current[1] + dc)
            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and maze[neighbor] == 1:
                tentative_g_score = current_g + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    heappush(open_set, (tentative_g_score + heuristic(neighbor, end), tentative_g_score, neighbor))
                    came_from[neighbor] = current

    return [], frames, traversal