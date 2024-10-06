
import ast
import math

# Input list of strings
coord_list_str = x  # Placeholder for your input list  # Set your custom unit distance here
tolerance = 1e-6  # Small tolerance for floating-point comparisons

# Combine all strings into one and parse the coordinate strings
coords = []
for coord_str in coord_list_str:
    # Convert each string into a list of tuples
    coords += [tuple(map(float, coord.strip('{}').split(','))) for coord in ast.literal_eval(coord_str)]

# Function to check if two points differ by approximately y (within tolerance) in one coordinate
def is_adjacent(point1, point2, y):
    diff = [abs(p1 - p2) for p1, p2 in zip(point1, point2)]
    # Return True if one coordinate differs by approximately y and the others are the same
    return sum(math.isclose(d, y, abs_tol=tolerance) for d in diff) == 1 and sum(math.isclose(d, 0, abs_tol=tolerance) for d in diff) == 2

# Function to return axis direction in the format {x, y, z}
def get_axis_direction(point, neighbor, y):
    for k in range(3):
        if math.isclose(abs(point[k] - neighbor[k]), y, abs_tol=tolerance):
            if k == 0:  # X-axis
                return "{1, 0, 0}"
            elif k == 1:  # Y-axis
                return "{0, 1, 0}"
            elif k == 2:  # Z-axis
                return "{0, 0, 1}"
    return "{0, 0, 0}"

# Lists to hold indexes of points that pass, fail, points with exactly one neighbor, and directions
passes = []
fails = []
one_neighbor = []  # To hold points with exactly one neighbor
directions = []
one_neighbor_directions = []  # To hold directions for points with one neighbor

# Iterate over all points and check the condition
for i, point in enumerate(coords):
    neighbors = []
    # Find neighbors that differ by approximately y in one coordinate
    for j, other_point in enumerate(coords):
        if i != j and is_adjacent(point, other_point, y):
            neighbors.append(j)

    # If the point has exactly one neighbor, add it to the one_neighbor list and get the direction
    if len(neighbors) == 1:
        one_neighbor.append(i)
        one_neighbor_directions.append(get_axis_direction(point, coords[neighbors[0]], y))

    # Check if there are exactly two neighbors
    elif len(neighbors) == 2:
        # Ensure both neighbors differ along the same axis and are aligned
        for k in range(3):
            if math.isclose(abs(point[k] - coords[neighbors[0]][k]), y, abs_tol=tolerance) and                math.isclose(abs(point[k] - coords[neighbors[1]][k]), y, abs_tol=tolerance):
                # Ensure the other two coordinates are the same
                if (math.isclose(coords[neighbors[0]][(k + 1) % 3], point[(k + 1) % 3], abs_tol=tolerance) and
                    math.isclose(coords[neighbors[0]][(k + 2) % 3], point[(k + 2) % 3], abs_tol=tolerance) and
                    math.isclose(coords[neighbors[1]][(k + 1) % 3], point[(k + 1) % 3], abs_tol=tolerance) and
                    math.isclose(coords[neighbors[1]][(k + 2) % 3], point[(k + 2) % 3], abs_tol=tolerance)):
                    passes.append(i)
                    directions.append(get_axis_direction(point, coords[neighbors[0]], y))  # Or use the 2nd neighbor
                    break
        else:
            fails.append(i)
    else:
        fails.append(i)

# Output the lists of indexes that pass, fail, points with one neighbor, and the directions
print("Passes:", passes)
print("Fails:", fails)
print("One Neighbor:", one_neighbor)
print("One Neighbor Directions:", one_neighbor_directions)
print("Directions:", directions)
