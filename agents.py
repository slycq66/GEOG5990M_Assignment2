# -*- coding: utf-8 -*-
"""
Student Id: 201581226
"""

import random

MAP_SIZE = 300  # Help define the boundary of map

# Set colors for legends on density map
Density_Color = [
    "#FFFFFF", "#008000", "#1e8000", "#2e8000", "#3b7f00", "#467f00",
    "#517e00", "#5b7d00", "#657c00", "#6f7b00", "#787900",
    "#827700", "#8b7500", "#957200", "#9e6f00", "#a86b00",
    "#b16700", "#ba6300", "#c35e00", "#cd5800", "#d65100",
    "#de4900", "#e73f00", "#ef3400", "#f72300", "#ff0000",
]

"""
Try to create a color scheme from green to red automatically,
but the module can not be imported successfully.

from colour import Color
def gen_colors():
    green = Color("green")
    colors = list(green.range_to(Color("red"),25))
    return colors
"""


# Set color for every house on map and their legend
HOUSE_COLOR = [
    "#DC143C", "#EE82EE", "#4B0082", "#0000CD", "#B0C4DE",
    "#778899", "#F0F8FF", "#5F9EA0", "#00CED1", "#7FFFAA",
    "#808000", "#FFFACD", "#FFD700", "#F5DEB3", "#FFDEAD",
    "#FF8C00", "#D2691E", "#FFA07A", "#FF4500", "#A9A9A9",
    "#7FFF00", "#008080", "#7B68EE", "#FF1493", "#2E8B57",
]


"""
The drunks will hang around after they come out of the pub.
They will stop moving after reaching their own house or meet police.
"""
class Drunk:
    
    """
    function __init__(): 

        Initialize the attribute of each drunk.
        
        _id -- the 'name' for the drunks
        
        row/col -- initial position of drunks
    
        reached -- store coordinates that drunks have passed
    """
    def __init__(self, _id):
        self.drunk_id = _id
        self.row = -1
        self.col = -1

    """
    function choose_dir(): 
        
        Make drunks move by choosing a random direction.
        
        directions -- four directions drunk can choose 
    """
    def choose_dir(self):  
        random.seed()  # Shuffle the sequence
        directions = ["up", "left", "right", "down"]
        row = self.row
        col = self.col        
        choice = random.choice(directions)  # random choose a direction
        row, col = self.move(choice)
        self.row = row
        self.col = col

    """
    function move(): 

        Simulating the way someone walks when they're drunk.
        
        Because they are drunk, they can only move 1 unit each time.
        
        The drunks stay within the map when they reach the boundaries.
    """
    def move(self, choice):
        
        row = self.row
        col = self.col

        if choice == "up":
            row = 0 if self.row - 1 <= 0 else self.row - 1
        elif choice == "left":
            col = 0 if self.col - 1 <= 0 else self.col - 1
        elif choice == "right":
            col = MAP_SIZE - 1 if self.col + 1 >= MAP_SIZE else self.col + 1
        elif choice == "down":
            row = MAP_SIZE - 1 if self.row + 1 >= MAP_SIZE else self.row + 1
        return row, col


"""
The police patrol on the road and send the drunks home after finding them.
"""
class Policeman:
    
    # the police start patrol from top left corner of the map
    def __init__(self):       
        self.row = 0
        self.col = 0

    # the police can move 20 units each time
    def do_patrol(self):
        if self.col + 20 >= MAP_SIZE:
            if self.row + 20 >= MAP_SIZE:
                self.row = 0
            else:
                self.row += 20
            self.col = 0
        else:
            self.col += 20

