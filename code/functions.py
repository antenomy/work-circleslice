
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
    
    angle_a = get_angle(new_points[0])
    angle_b = get_angle(new_points[1])

    if (is_between(angle_a, 0, np.pi / 2) and is_between(angle_b, 3 * np.pi / 2, np.pi * 2)) or (is_between(angle_b, 0, np.pi / 2) and is_between(angle_a, 3 * np.pi / 2, np.pi * 2)):
        for iteration in range(len(angle_list)):
            if is_between(angle_list[iteration], angle_a, angle_b):
                return_point_array.append(point_array[iteration])
                return_angle_list.append(angle_list[iteration])
    else:
        for iteration in range(len(angle_list)):   
            if not is_between(angle_list[iteration], angle_a, angle_b):
                return_point_array.append(point_array[iteration])
                return_angle_list.append(angle_list[iteration])

    return np.array(return_point_array), return_angle_list

def insert_points(point_array, angle_list, new_points):
    return_point_array = point_array
    return_angle_list = angle_list
    for new_point in new_points:
        new_point_angle = get_angle(new_point)
        insertion_index = bisect_left(angle_list, new_point_angle)
        
        return_point_array = np.insert(return_point_array, insertion_index, new_point, axis=0)
        return_angle_list.insert(insertion_index, new_point_angle)
    return return_point_array, return_angle_list
      
def find_next_cut_point(new_points):

    if len(new_points) != 2:
        raise ValueError(f"ERROR! {len(new_points)} is the wrong number of intersecting points!")
    
    # Assign points and angles for readability
    p0, p1 = new_points[0], new_points[1]
    a0, a1 = get_angle(new_points[0]), get_angle(new_points[1])

    # Check if this is the quadrant-wraparound case (Q1 vs Q4)
    if a0 < np.pi / 2 and a1 > 3 * np.pi / 2:
        current_point = p0
    elif a1 < np.pi / 2 and a0 > 3 * np.pi / 2:
        current_point = p1
    else:
        # Otherwise just pick the larger angle (more counterclockwise)
        if a0 > a1:
            current_point = p0
        else:
            current_point = p1
    
    current_angle = get_angle(current_point)
    return np.array([
        current_point[0] - (CUT_THICKNESS*np.cos(current_angle)), 
        current_point[1] - (CUT_THICKNESS*np.sin(current_angle))
        ])

def triangle_area(p1, p2, p3):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    return 0.5 * abs(x1*(y2 - y3) + x2*(y3 - y1) + x3*(y1 - y2))


def plot_points(point_array, current_point, new_points):
    x = point_array[:, 0]  # All rows, first column (x-coordinates)
    y = point_array[:, 1]  # All rows, second column (y-coordinates)
    
    first = [x[1], y[1]]
    last = [x[-1], y[-1]]

    x = x[1:-1]
    y = y[1:-1]
    
    # Create the scatter plot
    plt.figure(figsize=(8, 6))  # Optional: Adjust figure size
    plt.scatter(x, y)
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