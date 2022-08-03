import random
import math




class drunk:
    def __init__(self, name):
        self.name = name


class drunk_normal(drunk):
    def __init__(self, name):
        super().__init__(name)

    def walk(self):                                           
        return random.choice([(1,0), (0,1), (-1,0), (0,-1)])    #the function selects one option from the list

    
class coordinate:
    def __init__(self, x,y):                        #it recieves a coordinate as (x,y)
        self.x = x
        self.y = y

    def new_position(self, new_x, new_y):
        return coordinate(self.x + new_x, self.y + new_y)   #sums the new (x,y) values to the previous
                                                            #ones so that the new position in the plane
                                                            #is given
    
    def distance(self, new_coordinate):                 #new_coordinate is an instance of coordinate(x,y)
        change_x = self.x - new_coordinate.x            #change in x is just the difference bewtween former
        change_y = self.y - new_coordinate.y            #x value and the new one. Same for y. 
        new_distance = (change_x**2+change_y**2)**0.5   #the distance between any (x,y) and (xb, yb) points
        return new_distance                                 #is square_root((x-xb)**2 +(y-yb)**2)


class Plane:
    def __init__(self):
        self.coordinates = {}                           #in this dict the coordinates of the drunk_normal will be stored 
    
    def add_drunk(self, drunk, coordinate):             #recieves an instance of drunk and coordinate classes
        self.coordinates[drunk] = coordinate            #updates the dict with a drunk (key) and its coordinate

    def get_coordinate(self, drunk):                    #return the current position (x,y) of a drunk which 
        return self.coordinates[drunk]                   #is the dict's key
    
    def move(self, drunk):
        new_x, new_y = drunk.walk()                     #obtain a new (x,y) coordinate by caling the normal_drunk.walk()
        current_coordinate = self.coordinates[drunk]    #get the current coordinate retrieving the (x,y) 
                                                        #info asociated with the drunk key
        
        new_coordinate = current_coordinate.new_position(new_x, new_y)
        
        """Several steps to explain this last line of code: 
        1). current_coordinate is an instance of the class coordinate.
        current_coordinate is a coordinate stored in the dict self.coordinates (b), from
        which [drunk] is the key (a):
        a). current_coordinate = self.coordinates[drunk]
        b). self.coordinates[drunk] = coordinate
        2). Given 1, we can use the method new_position from the class coordinate.
        This method returns a new position by adding the current (x,y) stored in
        current_coordinate to the (new_x, new_y) generated by calling the drunk,walk() method
        3). So, current_coordinate is the new position resulting from this sum: 
        (x,y) in current_coordinate + (x,y) from drunk.walk()"""
        
        self.coordinates[drunk] = new_coordinate        #we update the dict in self.coordinates with the new coordinate

def walking(plane, drunk, simulation_steps):
    starting_point = plane.get_coordinate(drunk)        #See line 44 for comment on this function

    for _ in range(simulation_steps):
        plane.move(drunk)                               #see line 47 on this function
    return starting_point.distance(plane.get_coordinate(drunk))

    """
    Again, several steps on the last line:
    1). starting_point of drunk by definition in the walk_simulation will be (0,0).
    2). Then the function plane.move(drunk) will change coordinates of drunk. 
    3).Then distance will compare the initial coordinate (starting_point) with the new drunk coordinate
    4).The new coordinate will become the starting_point for the next iteration, and so on.
    """

def walk_simulation(simulation_steps, simulation_repetitions, drunk_instance):  
    drunk = drunk_instance(name="Aroesti")                                      #instance of the drunk class with name
    starting_point = coordinate(0,0)             
    distance_walked = []                          #empty dict to save walked distances in each simulation
    for _ in range(simulation_repetitions):
        plano = Plane()                                     #creates a dict to store and drunk(key) and its coordinates
        plano.add_drunk(drunk, starting_point)
        walk_simulation = walking(plano, drunk, simulation_steps)
        distance_walked.append(round(walk_simulation, 1))   #adds to the list the distance from walking function

    return distance_walked

def main(simulation_steps, simulation_repetitions, drunk):
    for steps in simulation_steps:
        distances = walk_simulation(steps, simulation_repetitions, drunk) #See line 68 for this function
        average_distance = round(sum(distances)/len(distances),4) #Divides the total distance walked by-
                                                                  #the total number of distances stored in 
        maximum_distance = max(distances)
        minimum_distance = min(distances)
        print(f'{drunk.__name__} caminó {steps} pasos')
        print(f'Distancia promedio: {average_distance}')
        print(f'Distancia máxima: {maximum_distance}')
        print(f'Distancia mínima: {minimum_distance}')

if __name__ == "__main__":
    simulation_steps = [10, 100, 1000, 10000]   #this is the number of steps the drunk will walk by simulation
    simulation_repetitions = 100                #how many times the simulation will be executed
    main(simulation_steps, simulation_repetitions, drunk_normal)    #the main function recieves the number of steps,
