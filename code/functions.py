
from settings import *

import numpy as np

def linear_func(x, k, m = 0):
    return (x * k) + m

def is_between(x, a, b):
    top = max(a,b)
    bot = min(a,b)
    
    return bot <= x <= top

def get_angle(point):
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
    
    if is_between(intersecrion_point, check_point_a[0], check_point_b[0]):
        intersecrion_points.append(intersecrion_point)
    
    for position in range(len(point_array) - 1):
        check_point_a = point_array[position]
        check_point_b = point_array[position + 1]
        
        intersecrion_point = check_point_intersection(check_point_a, check_point_b, line_k, line_m, vertical_x)
        
        if is_between(intersecrion_point, check_point_a[0], check_point_b[0]):
            intersecrion_points.append(intersecrion_point)
            
    return intersecrion_points
        
        
def check_point_intersection(point_a, point_b, line_k = None, line_m = 0, vertical_x = None)
    
    if vertical_x is not None:
        if point_b[0] == point_a[0] and point_b[0] == vertical_x:
            raise("Several intersections between segments")
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
            
            return (intersection_x, point_k*intersection_x + point_m)  
        
def remove_outside_points(point_array, line_k = None, line_m = 0, vertical_x = None):
    return_array = np.zeros_like(point_array)
    row = 0
    
    for point in point_array:
        
        if vertical_x is not None:
            if vertical_x > 0 and point[0] < vertical_x:
                return_array[row] = point
        elif line_k is not None:
            line_y = line_k*point[0]
            if line_y > 0 and point[1] < line_y:
                return_array[row] = point

        row += 1
        
    return return_array

def sort_in_new_point_list