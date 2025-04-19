
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
    return np.arctan(point[1] / point[0])

def get_sign(x):
  if x > 0:
    return 1
  elif x < 0:
    return -1
  else:
    return 0

def reduce_magnitude(value, reduction):
    return get_sign(value) * (abs(value) - reduction)

def generate_circle_points(radius, num_points=100, center=(0, 0)):
    theta = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)
    return np.column_stack((x, y))

def check_all_point_intersections(point_array, line_k = None, line_m = 0, vertical_x = None):
    intersecrion_points = list()
    
    # First it checks the two points that cross the 2pi line
    check_point_a = point_array[0]
    check_point_b = point_array[-1]
    
    intersecrion_point = check_point_intersection(check_point_a, check_point_b, line_k, line_m, vertical_x)
    
    if intersecrion_point: 
        if is_between(intersecrion_point[0], check_point_a[0], check_point_b[0]):
            intersecrion_points.append(intersecrion_point)
    
    for position in range(len(point_array) - 1):
        check_point_a = point_array[position]
        check_point_b = point_array[position + 1]
        
        intersecrion_point = check_point_intersection(check_point_a, check_point_b, line_k, line_m, vertical_x)
        if intersecrion_point:
            if is_between(intersecrion_point[0], check_point_a[0], check_point_b[0]):
                intersecrion_points.append(intersecrion_point)
            if len(intersecrion_points) == 2:
                return intersecrion_points
    return intersecrion_points
        
        
def check_point_intersection(point_a, point_b, line_k = None, line_m = 0, vertical_x = None):
    
    if vertical_x is not None:
        if abs(point_b[0] - point_a[0]) < SMALL_THRESHOLD:
            if point_b[0] == vertical_x:
                raise("Several intersections between segments")
            else:
                return None
        else:
            point_k = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
            point_m = point_a[1] - point_a[0]*point_k
            return (vertical_x, point_k*vertical_x + point_m) 
             
    elif line_k is not None:
        
        point_k = (point_b[1] - point_a[1]) / (point_b[0] - point_a[0])
        point_m = point_a[1] - point_a[0]*point_k
        
        if point_k == line_k:
            if point_m == line_m:
                raise("Several intersections between segments")
            else:
                return None
        else:
            intersection_x = (point_m - line_m) / (line_k - point_k)
            
            return (intersection_x, float(point_k*intersection_x + point_m))  
        
def remove_outside_points(point_array, angle_list, line_k = None, line_m = 0, vertical_x = None):
    return_point_array = list()
    return_angle_list = list()
    row = 0
    
    print("Point length:", len(point_array))
    print("Angle length:", len(angle_list))
    
    for point in point_array:
        
        if vertical_x is not None:
            if vertical_x > 0 and point[0] < vertical_x:
                return_point_array.append(point)
                return_angle_list.append(angle_list[row])
        elif line_k is not None:
            line_y = line_k*point[0]
            if line_y > 0 and point[1] < line_y:
                return_point_array.append(point)
                return_angle_list.append(angle_list[row])

        row += 1
        
    return np.array(return_point_array), return_angle_list

def insert_points(point_array, angle_list, new_points):
    return_point_array = point_array
    return_angle_list = angle_list
    
    for new_point in new_points:
        new_point_angle = get_angle(new_point)
        insertion_index = bisect_left(angle_list, new_point_angle)
        
        return_point_array = np.insert(point_array, insertion_index, new_point, axis=0)
        return_angle_list.insert(insertion_index, new_point_angle)
    
    return return_point_array, return_angle_list
    
    
    
def find_next_cut_point(new_points):
    Q_1_point_exists = False
    Q_4_point_exists = False
    Q_1_point = None
    
    for point in new_points:
        point_angle = get_angle(point)
        if is_between(point_angle, 0, np.pi*0.5):
            Q_1_point_exists = True
            if get_angle(Q_1_point):
                if get_angle(Q_1_point) > point_angle:
                    Q_1_point = point
            else:
                Q_1_point = point
            
        elif is_between(point_angle, np.pi*1.5, np.pi*2):
            Q_4_point_exists = True

    if Q_1_point_exists and Q_4_point_exists:
        current_point = Q_1_point
    else:
        current_point = None
        for point in new_points:
            if get_angle(current_point):
                if get_angle(point) > get_angle(current_point):
                    current_point = point
            else:
                current_point = point
    current_angle = get_angle(current_point)
    return np.array([current_point[0] - (CUT_THICKNESS*np.cos(current_angle)), current_point[1] - (CUT_THICKNESS*np.sin(current_angle))])

def plot_points(point_array, current_point):
    x = point_array[:, 0]  # All rows, first column (x-coordinates)
    y = point_array[:, 1]  # All rows, second column (y-coordinates)
    
    # Create the scatter plot
    plt.figure(figsize=(8, 6))  # Optional: Adjust figure size
    plt.scatter(x, y)
    plt.scatter(current_point[0], current_point[1], color='red', marker='o', s=100)

    # Add labels and title
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Plot of 2D Points")

    # Add grid (optional)
    plt.grid(True)

    # Show the plot
    plt.show()