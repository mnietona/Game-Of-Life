from constants import *
from model.fauna import Fauna

class Fox(Fauna):
    
    def __init__(self, grid_size, smart_level = 1):
        super().__init__(grid_size, health=FOX_HEALTH, radius=FOX_RADIUS, delta=FOX_DELTA_RADIUS)
        self.target_type = "Rabbit"
        self.smart_level = smart_level
        self.adjust_radius_based_on_intelligence()  
    
    def name_fr(self):
        return "Renard"
    
    def interact_with_environment(self, i, j, grid):
        rabbit_position = grid.find_nearest_target((i, j), self.radius, self.target_type)
        nearest_burrow_position = grid.find_nearest_burrow((i, j))
        new_position = (i, j)
        
        if rabbit_position :
            distance_to_nearest_burrow = grid.calculate_distance((i, j), nearest_burrow_position)
            if distance_to_nearest_burrow >= MIN_DISTANCE_TO_BURROW:  
                new_position = self.move(i, j, grid)
                self.replay(new_position, grid)
            else:
                new_position = self.move_randomly(i, j, grid)
        else:
            new_position = self.move_randomly(i, j, grid)
            self.replay(new_position, grid)
        
        self.after_interaction(new_position, grid)
        return new_position

    def ajust_population(self, grid):
        num_fox = 1
        if grid.count_population(Fox) <= 2:
            self.health += FOX_HEALTH
            num_fox = 5
        return num_fox
    
    def replay(self, new_position, grid):        
        if self.smart_level == 3:
            return self.move(new_position[0], new_position[1], grid)
    
    def try_reproduce(self, grid):
        num_fox = self.ajust_population(grid)
        
        if self.health > FOX_SOME_REPRODUCTION_THRESHOLD:
            self.health -= FOX_COST_OF_REPRODUCTION
            if grid.count_population(Fox) < (grid.size ** 2) / 20:
                grid.populate_entities(Fox, num_fox, self.smart_level)
    
    @property
    def color(self):
        return RED