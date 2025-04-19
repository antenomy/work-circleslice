
from settings import *
from functions import *

#from piece import Piece
from circle import Circle

import numpy as np
import scipy



def main():
    
    point_array = generate_circle_points(OUTER_RADIUS, STARTING_CIRCLE_NUM_POINTS)
    angle_list = [2*np.pi*iteration/STARTING_CIRCLE_NUM_POINTS for iteration in range(STARTING_CIRCLE_NUM_POINTS)]
    
    iterations = 1
    current_cut_radius = OUTER_RADIUS - CUT_THICKNESS
    
    new_points = check_all_point_intersections(point_array, vertical_x=current_cut_radius)
    point_array = remove_outside_points(point_array, vertical_x=current_cut_radius)
    insertion_indexes = find_insertion_indexes()
    
    
    current_point = np.array([OUTER_RADIUS, 0])
    
    while current_cut_radius > INNER_RADIUS:
        
        if current_point[1] == 0:
            vertical_x = reduce_magnitude(current_point[0], CUT_THICKNESS)
            new_points = check_all_point_intersections(point_array, vertical_x=vertical_x)
            
            point_array = remove_outside_points(point_array, vertical_x=vertical_x)
            
        else:
            if current_point[0] == 0:
                line_k = 1
                line_m = reduce_magnitude(current_point[1], CUT_THICKNESS)
            else:
                angle_k = current_point[1]/current_point[0] #check for current_point 0
                current_theta = get_angle(current_point)
                
                line_k = -1 / angle_k
                line_m = current_point[1] - CUT_THICKNESS*np.sin(current_theta)

            new_points = check_all_point_intersections(point_array, line_k, line_m)
            point_array = remove_outside_points(point_array, line_k, line_m)

            
        insertion_indexes = find_insertion_indexes()
            
        for point in new_points:
            

            
        
        
        
        # cut_circle = Circle(current_cut_radius)
        # cut_theta = np.arcsin()
        # cut_count = (2 * np.pi)
        
        
        point_list[0]
        
        
        
        
        
        iterations += 1
        current_cut_radius -= CUT_THICKNESS
        
        current_point = 0 # set next point
        
        
        print(f"Number of cuts: {iterations}")
            
        


