
from settings import *

import numpy as np

import matplotlib.pyplot as plt
from bisect import bisect_left

def linear_func(x, k, m = 0):
    return (x * k) + m

def is_between(x, a, b):
    if x is None:
        return None
    top = max(a,b)
    bot = min(a,b)
    
    return bot <= x <= top

def get_angle(point):
    if point is None:
        return None
    
    angle = np.arctan2(point[1], point[0])
    
    if angle < 0:
        angle += 2 * np.pi

    return angle

def get_sign(x):
  if x > 0:
    return 1
  elif x < 0:
    return -1
  else:
    return 0
  
def add_dict(dict, element):
    if element in dict:
        dict[element] += 1
    else:
        dict[element] = 1

def reduce_magnitude(value, reduction):
    return get_sign(value) * (abs(value) - reduction)

def generate_circle_points(radius, num_points=100, center=(0, 0)):
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return np.column_stack((x, y))

def check_all_point_intersections(point_array, line_k = None, line_m = 0, vertical_x = None):
    intersecrion_points = list()
    
    for position in range(len(point_array)):
        check_point_a = point_array[position-1]
        check_point_b = point_array[position]
        
        intersecrion_point = check_point_intersection(check_point_a, check_point_b, line_k, line_m, vertical_x)
        
        
        if intersecrion_point:
            if is_between(intersecrion_point[0], check_point_a[0], check_point_b[0]):
                #print(check_point_a, check_point_b)
                intersecrion_points.append(intersecrion_point)
    
    if len(intersecrion_points) > 2:
        raise ValueError (f"{len(intersecrion_points)} is too many intersections! \n {intersecrion_points}")
    return intersecrion_points
        
        
def check_point_intersection(point_a, point_b, line_k = None, line_m = 0, vertical_x = None):
    
    if vertical_x is not None:
        if abs(point_b[0] - point_a[0]) < SMALL_THRESHOLD:
            if point_b[0] == vertical_x:
                raise ValueError("Several intersections between segments")
            else:
                return None
        else:
            point_k = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
            point_m = point_a[1] - point_a[0]*point_k
            return (vertical_x, point_k*vertical_x + point_m) 
             
    elif line_k is not None:
        if abs(point_b[0] - point_a[0]) < SMALL_THRESHOLD:
            if is_between(line_k*point_a[0] + line_m, point_a[1], point_b[1]): # check that line_y is in y range of points
                return (float(point_a[0]), float(line_k*point_a[0] + line_m))
            else:
                return None 
        else:
            point_k = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
            point_m = point_a[1] - point_a[0]*point_k
            
        if point_k == line_k:
            if point_m == line_m:
                raise ValueError("Several intersections between segments")
            else:
                return None
        else:
            intersection_x = (point_m - line_m) / (line_k - point_k)
            
            return (float(intersection_x), float(point_k*intersection_x + point_m))  
        
def remove_outside_points(point_array, angle_list, new_points):
    return_point_array = list()
    return_angle_list = list()
    removed_points = list()

    #print(new_points)
    
    angle_a = get_angle(new_points[0])
    angle_b = get_angle(new_points[1])

    if (is_between(angle_a, 0, np.pi / 2) and is_between(angle_b, 3 * np.pi / 2, np.pi * 2)) or (is_between(angle_b, 0, np.pi / 2) and is_between(angle_a, 3 * np.pi / 2, np.pi * 2)):
        # Checks which if there is a point on each side of the 2 pi line 

        for iteration in range(len(angle_list)):
            if is_between(angle_list[iteration], angle_a, angle_b):
                return_point_array.append(point_array[iteration])
                return_angle_list.append(angle_list[iteration])
            else:
                removed_points.append(point_array[iteration])
    else:
        for iteration in range(len(angle_list)):   
            if not is_between(angle_list[iteration], angle_a, angle_b):
                return_point_array.append(point_array[iteration])
                return_angle_list.append(angle_list[iteration])
            else:
                removed_points.append(point_array[iteration])

    return np.array(return_point_array), return_angle_list, np.array(removed_points)

def insert_points(point_array, angle_list, new_points):
    return_point_array = point_array
    return_angle_list = angle_list
    for new_point in new_points:
        new_point_angle = get_angle(new_point)
        insertion_index = bisect_left(angle_list, new_point_angle)
        
        return_point_array = np.insert(return_point_array, insertion_index, new_point, axis=0)
        return_angle_list.insert(insertion_index, new_point_angle)

    return return_point_array, return_angle_list

def angle_sort(new_points):

    angle_a = get_angle(new_points[0])
    angle_b = get_angle(new_points[-1])

    points = np.asarray(new_points)

    angles = np.arctan2(points[:,1], points[:,0])
    angles = np.mod(angles, 2 * np.pi)

    # Sort points by angle
    sort_order = np.argsort(angles)
    sorted_points = points[sort_order]
    break_index = 0

    if (is_between(angle_a, 0, np.pi / 2) and is_between(angle_b, 3 * np.pi / 2, np.pi * 2)) or (is_between(angle_b, 0, np.pi / 2) and is_between(angle_a, 3 * np.pi / 2, np.pi * 2)):
        for point in sorted_points:
            if get_angle(point) > 3 * np.pi / 2:
                break
            break_index += 1

        export_array = np.concatenate((sorted_points[break_index:], sorted_points[:break_index]))
    else:
        export_array = sorted_points

    return export_array 



def polygon_area(vertices):
    """
    Calculate the area of a polygon using the shoelace formula.

    Parameters:
    vertices (array-like): An (N, 2) array of x, y coordinates.

    Returns:
    float: The absolute area of the polygon.
    """
    vertices = np.asarray(vertices)

    if vertices.shape[0] < 3:
        return 0
    
    x = vertices[:, 0]
    y = vertices[:, 1]
    # Shift the coordinates
    x_shifted = np.roll(x, -1)
    y_shifted = np.roll(y, -1)
    area = 0.5 * np.abs(np.dot(x, y_shifted) - np.dot(y, x_shifted))
    return area


def plot_points(point_array, new_points, plot_current = False, current_point = None):
    x = point_array[:, 0]  # All rows, first column (x-coordinates)
    y = point_array[:, 1]  # All rows, second column (y-coordinates)
    
    first = [x[1], y[1]]
    last = [x[-1], y[-1]]

    x = x[1:-1]
    y = y[1:-1]
    
    # Create the scatter plot
    plt.figure(figsize=(8, 6))  # Optional: Adjust figure size
    plt.scatter(x, y)

    if plot_current:
        plt.scatter(current_point[0], current_point[1], color='red', marker='o', s=100)

    plt.scatter(first[0], first[1], color='yellow', marker='o', s=100)
    plt.scatter(last[0], last[1], color='green', marker='o', s=100)
    
    for point in new_points:
        plt.scatter(point[0], point[1], color='orange', marker='o', s=100)

    # Add labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Plot of 2D Points")
    
    # Set the limits for the x and y axes
    plt.xlim(-300, 300)  # x-axis limits from 0 to 10
    plt.ylim(-300, 300)  # y-axis limits from -1 to 1

    # Add grid (optional)
    plt.grid(True)

    # Show the plot
    plt.show()