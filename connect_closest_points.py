
def parse_coordinates(coord_strings):
    """Parse the input coordinate strings into a list of (x, y, z) tuples."""
    coords = []
    for s in coord_strings:
        # Remove braces and split the string by commas
        s = s.strip('{}')
        x, y, z = map(float, s.split(','))
        coords.append((x, y, z))
    return coords

def find_closest_in_direction(points, index, direction, tolerance=5):
    """Find the closest point in the specified direction ('N', 'S', 'E', 'W') within tolerance."""
    x1, y1, _ = points[index]
    closest_point = None
    min_distance = float('inf')
    
    for i, (x2, y2, _) in enumerate(points):
        if i == index:
            continue
        
        # Check for directions with tolerance
        if direction == 'N' and abs(x1 - x2) <= tolerance and y2 > y1:  # North: Close x, larger y
            distance = y2 - y1
        elif direction == 'S' and abs(x1 - x2) <= tolerance and y2 < y1:  # South: Close x, smaller y
            distance = y1 - y2
        elif direction == 'E' and abs(y1 - y2) <= tolerance and x2 > x1:  # East: Close y, larger x
            distance = x2 - x1
        elif direction == 'W' and abs(y1 - y2) <= tolerance and x2 < x1:  # West: Close y, smaller x
            distance = x1 - x2
        else:
            continue  # Not a valid point in the given direction
        
        if distance < min_distance:
            min_distance = distance
            closest_point = i
    
    return closest_point

def connect_closest_points(coord_strings, tolerance=5):
    """Connect each point to the closest point in all four cardinal directions with tolerance."""
    coords = parse_coordinates(coord_strings)
    start_points = []
    end_points = []
    
    directions = ['N', 'S', 'E', 'W']
    
    for i in range(len(coords)):
        for direction in directions:
            closest_point = find_closest_in_direction(coords, i, direction, tolerance)
            if closest_point is not None:
                start_points.append(i)
                end_points.append(closest_point)
    
    return start_points, end_points

# Example usage
if __name__ == "__main__":
    coord_strings = ['{1, 2, 0}', '{3, 4, 0}', '{5, 6, 0}', '{7, 8, 0}']

    # Set tolerance to 5
    start_points, end_points = connect_closest_points(coord_strings, tolerance=5)
    print("Start Points:", start_points)
    print("End Points:", end_points)
