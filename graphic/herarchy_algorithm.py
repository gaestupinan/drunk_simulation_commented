from bokeh.plotting import figure, show
from itertools import combinations
import random

def create_coordinate():
    #This function will return a tuple in the for (x,y) for x,y being numbers from 0-10
    x = int(random.choice(range(0,11)))
    y = int(random.choice(range(0,11)))

    return(x,y)


def create_data(number_of_coordinates):
    #The aboved mentioned function will be executed n times to create a list of coordinates (x,y) of lenght n
    list_of_coordinates = []
    for _ in range(number_of_coordinates):
        coordinate = create_coordinate()
        list_of_coordinates.append(coordinate)
    
    return list_of_coordinates


def get_distances(list_of_coordinates):
    #This dict will save the distance (key) between two coordinates saved as a tuple of two tuples: ((x1,y1),(x2,y2))
    distances_dict = {}
    #combinations returns the tuples of coordinates ((x1,y1),(x2,y2)) to be stored in the dict
    combination_of_coordinates = list(combinations(list_of_coordinates, 2))
    for element in combination_of_coordinates:
        distance = round(((element[0][0]-element[1][0])**2+(element[0][1]-element[1][1])**2)**0.5, 2)
        distances_dict[distance] = element

    return distances_dict


def new_points(list_of_coordinates, history_list, circle_list):
    #If there are less than 2 coordinates there is nothing left to sort
    if len(list_of_coordinates)<2:
        return (history_list, circle_list)
    #found the smallest distance between all coordindates:
    distances_dict = get_distances(list_of_coordinates)
    distances_list = list(distances_dict.keys())
    smallest_distance = min(distances_list)
    history_list.append(list_of_coordinates)
    #use that distance to find the coordinates in the dict:
    delete_first_coordinate = distances_dict[smallest_distance][0]
    delete_second_coordinate = distances_dict[smallest_distance][1]
    #finf the middle point between this two coordinates:
    new_x = (delete_first_coordinate[0] + delete_second_coordinate[0])/2
    new_y = (delete_first_coordinate[1] + delete_second_coordinate[1])/2
    new_coordinate = (new_x, new_y)
    #update all the dicts and lists by removing the previous two coordinates and adding the new one (new_coordinate)
    list_of_coordinates.remove(delete_first_coordinate)
    list_of_coordinates.remove(delete_second_coordinate)
    #distances_list.remove(smallest_distance)
    keys_to_delete = [distance_key for distance_key in distances_dict if delete_first_coordinate in distances_dict[distance_key] or delete_second_coordinate in distances_dict[distance_key]]
    for any_key in keys_to_delete:
        distances_dict.pop(any_key)
    #let's save the center/coordinate of the new point and the radious for drawing later a circle:
    circle_r = smallest_distance/2
    circle_list.append((new_coordinate, circle_r))
    #And run the function again, with the remaining coordinates until it reaches the base case:
    return new_points(list_of_coordinates, history_list, circle_list)


def show_hierarchy(coordinates_hierarchy, circle_coordinates):
    #This function is for visualization
    all_initial_coordinates = coordinates_hierarchy[0]
    #Let's create the lists of x and y values
    x_values = []
    y_values = []
    for coordinate in all_initial_coordinates:
        x_values.append(coordinate[0])
        y_values.append(coordinate[1])

    x_circles = []
    y_circles = []
    r_circles = []
    for circles in circle_coordinates:
        x_circles.append(circles[0][0])
        y_circles.append(circles[0][1])
        r_circles.append(circles[1])

    my_image = figure()
    my_image.cross(x_values, y_values, color="black")
    my_image.circle(x_circles, y_circles, radius=r_circles, alpha = 0.5)
    return show(my_image)

def main():
    number_of_coordinates = int(input("Number of coordinates to create: "))
    list_of_coordinates = create_data(number_of_coordinates)
    coordinates_circles = []
    arrange_of_coordinates = []
    circles_coordinates = []
    all_coordinates = new_points(list_of_coordinates, arrange_of_coordinates, coordinates_circles)
    coordinates_hierarchy = all_coordinates[0]
    circles_coordinates = all_coordinates[1]
    print(coordinates_hierarchy, circles_coordinates)
    show_hierarchy(coordinates_hierarchy, circles_coordinates)


if __name__ == "__main__":
    main()