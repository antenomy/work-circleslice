
from settings import *
from functions import *

#from piece import Piece
#from circle import Circle

import numpy as np
import scipy



def main():
    
    point_array = generate_circle_points(OUTER_RADIUS, STARTING_CIRCLE_NUM_POINTS)
    angle_list = [2*np.pi*iteration/STARTING_CIRCLE_NUM_POINTS for iteration in range(STARTING_CIRCLE_NUM_POINTS)]
    iterations = 1
    
    # First Cut
    current_cut_radius = OUTER_RADIUS - CUT_THICKNESS
    new_points = check_all_point_intersections(point_array, vertical_x=current_cut_radius)

    point_array, angle_list = remove_outside_points(point_array, angle_list, vertical_x=current_cut_radius)

    point_array, angle_list = insert_points(point_array, angle_list, new_points)
    
    current_point = find_next_cut_point(new_points) # fix this

    plot_points(point_array, current_point)
    
    while current_cut_radius > INNER_RADIUS:
        
        if current_point[1] == 0:
            vertical_x = reduce_magnitude(current_point[0], CUT_THICKNESS)
            new_points = check_all_point_intersections(point_array, vertical_x=vertical_x)
            point_array, angle_list = remove_outside_points(point_array, angle_list, vertical_x=vertical_x)
            
        else:
            if current_point[0] == 0:
                line_k = 0
                line_m = reduce_magnitude(current_point[1], CUT_THICKNESS)
            else:
                angle_k = current_point[1]/current_point[0]
                current_theta = get_angle(current_point)
                
                line_k = -1 / angle_k
                line_m = current_point[1] - line_k*current_point[0]
                print("line", line_k, line_m)

            new_points = check_all_point_intersections(point_array, line_k, line_m)
            print("new", new_points)
            point_array, angle_list = remove_outside_points(point_array, angle_list, line_k, line_m)

        point_array, angle_list= insert_points(point_array, angle_list, new_points)
        
        current_point = find_next_cut_point(new_points)
    
        

        iterations += 1
        current_cut_radius -= CUT_THICKNESS
        
        print(f"Current point: {current_point}")
        print(f"Current cut progress: {iterations}")
        
        plot_points(point_array, current_point)
    
    print(f"Number of cuts: {iterations}")
            
        
main()