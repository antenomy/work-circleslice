from functions import *

def unit_test():
    get_angle_UT_values = [
        ([1,0], 0),
        ([1, 1], np.pi/4),
        ([0,1], np.pi/2),
        ([-1,1], 3*np.pi/4),
        ([-1, -1], 5 * np.pi/4),
        ([-1,0], np.pi)
    ]
    for values in get_angle_UT_values:
        if get_angle(values[0]) != values[1]:
            raise ValueError(f"\nSomething is wrong with function get_angle for {values[0]}. \nSince {get_angle(values[0])} != {values[1]} ")
    print("get_angle pass")
unit_test()