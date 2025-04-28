
from settings import *
from functions import *

#from piece import Piece
#from circle import Circle

import numpy as np
#import scipy

def static_angleslice(point_array, angle_list, static_angle_step = None, sparse_step = None, plot_results = False, plot_sparse_results = False):

    current_cut_radius = OUTER_RADIUS - CUT_THICKNESS

    iterations = 1
    area_removed = 0

    new_points = check_all_point_intersections(point_array, vertical_x=current_cut_radius)

    point_remove_len = dict()
    point_len = len(point_array)
    point_array, angle_list, removed_points = remove_outside_points(point_array, angle_list, new_points)
    add_dict(point_remove_len, point_len - len(point_array))

    point_array, angle_list = insert_points(point_array, angle_list, new_points)

    #print(new_points[0])
    #print()
    #for i in range(len(removed_points)):
    #    print(removed_points[i])
    #print()
    #print(new_points[1])

    area_array = angle_sort(np.concatenate((
        np.array(new_points[0])[np.newaxis, :],   # <-- turns into shape (1,2)
        removed_points,          
        np.array(new_points[1])[np.newaxis, :]
    )))

    area_removed += polygon_area(area_array)

    CUT_ANGLE_DELTA = 2 * np.pi / static_angle_step
    current_cut_angle = CUT_ANGLE_DELTA


    while current_cut_radius > INNER_RADIUS:

        if current_cut_angle < SMALL_ANGLE_THRESHOLD or abs(current_cut_angle - 2 * np.pi) < SMALL_ANGLE_THRESHOLD:
            vertical_x = np.sign(np.cos(current_cut_angle)) * current_cut_radius

            new_points = check_all_point_intersections(point_array, vertical_x=vertical_x)

            point_len = len(point_array)
            point_array, angle_list, removed_points = remove_outside_points(point_array, angle_list, new_points)
            add_dict(point_remove_len, point_len - len(point_array))

        else:
            if (abs(current_cut_angle -     (np.pi / 2)) < SMALL_ANGLE_THRESHOLD or
                abs(current_cut_angle - (3 * np.pi / 2)) < SMALL_ANGLE_THRESHOLD):

                line_k = 0

                line_m = np.sin(current_cut_angle) * current_cut_radius

            else:
                angle_k = np.tan(current_cut_angle)

                #print(angle_k)

                line_k = -1 / angle_k

                line_m = (np.sin(current_cut_angle) * current_cut_radius) - (line_k * np.cos(current_cut_angle) * current_cut_radius)

                #print("Line:", round(line_k, 2), round(line_m, 2))
            
            #print(line_k, line_m)
            
            new_points = check_all_point_intersections(point_array, line_k, line_m)

            point_len = len(point_array)
            point_array, angle_list, removed_points = remove_outside_points(point_array, angle_list, new_points)
            add_dict(point_remove_len, point_len - len(point_array))

        point_array, angle_list= insert_points(point_array, angle_list, new_points)



        ### CALCULATING REMOVED AREA ###
        area_array = angle_sort(np.concatenate((
            np.array(new_points[0])[np.newaxis, :],   # <-- turns into shape (1,2)
            removed_points,          
            np.array(new_points[1])[np.newaxis, :]
        )))
        
        area_removed += polygon_area(area_array)


        if plot_results:
            plot_points(point_array, new_points)

        if iterations % sparse_step == 0:
            if plot_sparse_results:
                plot_points(point_array, new_points)
            print(iterations, area_removed)

        #print(iterations)

        #if iterations == 1:
        print(area_array)
        print(area_removed)
        
        iterations += 1

        current_cut_angle = (current_cut_angle + CUT_ANGLE_DELTA) % (2 * np.pi)

        if iterations % static_angle_step == 0:
            current_cut_radius -= CUT_THICKNESS
        

    return iterations, area_removed, point_remove_len


def semi_anglieslice():
    pass


def main():
    
    starting_circle_array = generate_circle_points(OUTER_RADIUS, STARTING_CIRCLE_NUM_POINTS)
    angle_list = [2*np.pi*iteration/STARTING_CIRCLE_NUM_POINTS for iteration in range(STARTING_CIRCLE_NUM_POINTS)]

    static_area_iterations, static_area_removed, static_point_remove_len = static_angleslice(starting_circle_array, angle_list, static_angle_step = 25, sparse_step=SPARSE_STEP, plot_results=STATIC_PLOT, plot_sparse_results=STATIC_SPARSE_PLOT)


    ### DEBUGGING ###
    
    #print(current_point)
    #print(f"Current point: {current_point} Angle: {round(get_angle(current_point) / np.pi, 2)} pi")
    #print("Point length:", len(point_array))
    #print("Angle length:", len(angle_list))
    #print(f"Current cut number: {iterations} \n")
    
    
    print(f"Number of cuts: {static_area_iterations}")
    print(f"Removed area: {static_area_removed}")
    print(static_point_remove_len)
        
main()