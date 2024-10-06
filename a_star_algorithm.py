
import heapq

def importenvironment(environment):
    # Step 1: Clean the outermost list
    environment = environment[0].strip('[]')
    
    # Step 2: Split the environment into individual rows
    rows = environment.split('", "')  # This splits the environment into rows

    matrix = []

    for row in rows:
        # Step 3: Clean the row and split into individual coordinates
        row = row.strip('[]"')  # Remove any leftover brackets and quotes
        coordinates = row.split(", '")  # Split into individual coordinate strings

        matrix_row = []
        for coord in coordinates:
            # Step 4: Strip braces and spaces, then split by commas to get x, y, z
            coord = coord.strip("{} '")  # Clean braces and spaces
            x_value, y_value, z_value = map(float, coord.split(','))  # Convert x, y, z to floats

            # Step 5: Check z_value to mark as obstacle (1) or free space (0)
            if z_value != 0:
                matrix_row.append(1)  # Mark as obstacle if z-axis is non-zero
            else:
                matrix_row.append(0)  # Free space if z is zero
        
        matrix.append(matrix_row)  # Add the processed row to the matrix

    return matrix

# Converts 1D index to 2D (row, col) index based on the matrix width
def index_to_coordinates(index, width):
    return index // width, index % width

# Converts 2D (row, col) index to 1D index
def coordinates_to_index(row, col, width):
    return row * width + col

# Heuristic function: Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* algorithm implementation
def a_star(matrix, start_idx, end_idx):
    rows, cols = len(matrix), len(matrix[0])
    start = index_to_coordinates(start_idx, cols)
    end = index_to_coordinates(end_idx, cols)

    # Priority queue
    open_list = []
    heapq.heappush(open_list, (0, start))

    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, end)}

    while open_list:
        _, current = heapq.heappop(open_list)

        # If we reach the target
        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(coordinates_to_index(current[0], current[1], cols))
                current = came_from[current]
            path.append(coordinates_to_index(start[0], start[1], cols))  # Append start point
            return path[::-1]  # Return reversed path

        # Possible 4-directional movement
        neighbors = [
            (current[0] - 1, current[1]),  # Up
            (current[0] + 1, current[1]),  # Down
            (current[0], current[1] - 1),  # Left
            (current[0], current[1] + 1),  # Right
        ]

        for neighbor in neighbors:
            row, col = neighbor
            if 0 <= row < rows and 0 <= col < cols and matrix[row][col] == 0:  # Ensure valid position and not obstacle
                tentative_g_score = g_score[current] + 1

                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return []  # Return empty path if no solution found

# Main function to process all start and end points
def find_paths(matrix, start_points, end_points):
    all_paths = []
    for start_idx, end_idx in zip(start_points, end_points):
        path = a_star(matrix, start_idx, end_idx)
        all_paths.append(path)
    return all_paths

def print_individual_numbers(list_of_lists):
    for sublist in list_of_lists:
        for number in sublist:
            print(number)

# Example usage
if __name__ == "__main__":
    environment = [['{0, 0, 0}, {1, 0, 0}, {2, 0, 1}', '{0, 1, 0}, {1, 1, 1}, {2, 1, 0}']]
    matrixinitial = importenvironment(environment)

    start = [0]
    end = [5]

    paths = find_paths(matrixinitial, start, end)
    print_individual_numbers(paths)
