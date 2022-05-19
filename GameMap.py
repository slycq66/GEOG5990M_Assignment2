# -*- coding: utf-8 -*-
"""
Student Id: 201581226
"""

import datetime

from typing import List

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize, QTimer
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtWidgets import QVBoxLayout, QWidget

import DensityMap
import MainWindow
from agents import *


MAP_SIZE = 300  # Help define the boundary of map
DRUNK_PEOPLE = 25  # Set the number of drunks 
BAR_ID = "1"  # The 'val' of the bar
POLICE_VIEWS = 20  # The police can find drunks within 20 units

# All colors are defined in hex format
BAR_COLOR = "#FFFFFF"     # Bar color 
DRUNK_COLOR = "#FFFFFF"   # Drunk color 
POLICE_COLOR = "#FF9999"  # Police color 
DRUNK_POLICE_MIX_COLOR = "#9999ff"  # Drunk color after they meet police
ROAD_COLOR = "#000000"  # Road color 


"""
Set coordinates and size for pub and houses.

Their position is determined by the coordinates in the upper left corner, 
and the area covered is determined by width and height.
"""
class MajorPlaceUnit:

    def __init__(self):
        self.up_left_row = -1
        self.up_left_col = -1
        self.width = 0
        self.height = 0


"""
Attributes for each pixel on the game map.

    val -- the type of the pixel(0 for road/ 1 for pub/ 10~250 for houses)
    
    color -- the color for different places
    
    current_color -- change the color after agents appearing on a pixel
    
    agents -- agents appearing on a pixel. self.agents[0] for drunk and self.agents[1] for police
"""
class MapUnit:
    
    def __init__(self):
        self.val = 0  
        self.color = "#FFFFFF" 
        self.current_color = "#FFFFFF"  
        self.agents: List = [None, None]  # The variable type is list
        

"""
Draw each pixel as a 4*4 rectangel label on the map and update the map after agents moving. 

Inherit standard QLabel class.  

Reference: https://blog.csdn.net/zzzzjh/article/details/82985209
""" 
class LabelMap(QtWidgets.QLabel):
    
    def __init__(self, parent, _map: MapUnit()):
        
        # Call superclass's __init__ function
        super().__init__(parent=parent)
        # Set the map size corresponding to the drawRect in the paintEvent event
        # Because the original size is 300 * 300 and area of label is 4*4，
        # the label map size is 300*4.
        self.setFixedSize(QSize(1200, 1200))
        self.map = _map
        # print(_map)

    def paintEvent(self, event):
        
        super().paintEvent(event)
        qp = QtGui.QPainter(self)
        # Set Qpen color and width
        qp.setPen(QPen(QColor(0, 0, 0), 1))
        qp.begin(self)
        for row in range(MAP_SIZE):
            for col in range(MAP_SIZE):
                # Fill the rectangle with current color
                br = QtGui.QBrush(QColor(self.map[row][col].current_color))
                qp.setBrush(br)
                qp.drawRect(QtCore.QRect(row*4, col*4, 4, 4))
        qp.end()

    def update_map(self, _map):
        
        self.map = _map
        self.update()


"""
Inherit Ui_Dialog class from Mainwindow.py
"""
class GameMap(MainWindow.Ui_Dialog):
    
    def __init__(self, dialog):
        
        super().setupUi(dialog)        # Call setupUi of the parent class

        # Initialization
        self.game_map: MapUnit() = list()     # Initialize the MapUnit
        self.density_map: set() = list()      # Initialize the DensityMapUnit
        self.init_legend()       # Initialize legend
        self.init_game_map()     # Initialize game map
        self.init_signal_slot()  # Initialize the QT signal slot
        
        # Create custom Label objects and add them to the UI's scrollArea control using QVBoxLayout
        self.label_map: LabelMap = LabelMap(None, self.game_map)
        widget = QWidget()
        la = QVBoxLayout()
        widget.setLayout(la)
        la.addWidget(self.label_map)
        self.scrollArea.setWidget(widget)
        
        # Map update timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_game_map)

    def init_signal_slot(self):
        
        # Link mouse click event with function slot_btn_start and slot_btn_draw
        self.btn_start.clicked.connect(self.slot_btn_start)
        self.btn_draw.clicked.connect(self.slot_btn_draw)
    
    def init_legend(self):
        
        # Creat legends for different classes and add them to object verticalLayout_legend on game map.
        label_bar = QtWidgets.QLabel()
        label_bar.setFixedSize(QSize(160, 25))
        label_bar.setText("Bar")
        label_bar.setStyleSheet(f"background-color:{BAR_COLOR};")
        self.verticalLayout_legend.addWidget(label_bar)
        
        label_drunk = QtWidgets.QLabel()
        label_drunk.setText("Drunk")
        label_drunk.setFixedSize(QSize(160, 25))
        label_drunk.setStyleSheet(f"background-color:{DRUNK_COLOR};")
        self.verticalLayout_legend.addWidget(label_drunk)
        
        label_police = QtWidgets.QLabel()
        label_police.setText("Police")
        label_police.setFixedSize(QSize(160, 25))
        label_police.setStyleSheet(f"background-color:{POLICE_COLOR};")
        self.verticalLayout_legend.addWidget(label_police)
        
        label_road = QtWidgets.QLabel()
        label_road.setText("Road")
        label_road.setFixedSize(QSize(160, 25))
        # Because the background color is black, the text color should be white
        label_road.setStyleSheet(f"background-color:{ROAD_COLOR};color:white")
        self.verticalLayout_legend.addWidget(label_road)
        
        label_police_drunk = QtWidgets.QLabel()
        label_police_drunk.setText("Police+Drunk")
        label_police_drunk.setFixedSize(QSize(160, 25))
        label_police_drunk.setStyleSheet(f"background-color:{DRUNK_POLICE_MIX_COLOR};")
        self.verticalLayout_legend.addWidget(label_police_drunk)
        
        for i, color in enumerate(HOUSE_COLOR):
            label = QtWidgets.QLabel()
            label.setFixedSize(QSize(160, 25))
            label.setText(f"House{i+1}")
            label.setStyleSheet(f"background-color:{color};")
            self.verticalLayout_legend.addWidget(label)
        # Print(list(enumerate(HOUSE_COLOR)))

    def init_game_map(self):

        # Initialize the Game Map and Density Map
        self.game_map.clear()
        self.density_map.clear()
        
        self.drunks: Drunk = list()  # Creates an empty list for Drunk
        self.police: Policeman = Policeman()  # Instantiate the police class
        self.police_meet_drunk = False  # Whether the police meet the drunk
        self.police_drunk_route = list()  # Plan a route home for the drunk
        self.on_work = False  # Whether the current program is running
        self.major_place: str(MajorPlaceUnit()) = dict()   
        
        # Read the original map file
        with open("drunk.plan", "r") as f:
            
            for row, line in enumerate(f.readlines()):
                map_line = list()
                items = line.split(",")
                
                for col in range(MAP_SIZE):
                    c = items[col].strip()  # Get the value of each pixel
                    # print(c)
                    mu = MapUnit()
                    mu.val = c
                    
                    """
                    This will make the bar disappear on the map, 
                    
                    because they are overwritten by the second line of code.
                    
                    # mu.current_color = mu.color = BAR_COLOR if c == "1" else ROAD_COLOR
                    # mu.current_color = mu.color = HOUSE_COLOR[int(c) // 10 - 1]
                    # if c == in [str(i*10) for i in range(1, 26)] else ROAD_COLOR
                    """

                    # The pixel has a value of 1
                    if c == "1":
                        mu.current_color = mu.color = BAR_COLOR
                    
                    # The pixel has a value of 10, 20, 30, 40, ..., 250
                    elif c in [str(i*10) for i in range(1, 26)]:
                        mu.current_color = mu.color = HOUSE_COLOR[int(c) // 10 - 1]
                    
                    # The pixel has a value of 0
                    else:
                        mu.current_color = mu.color = ROAD_COLOR
                    
                    # Compared to the road, the house and bar are more special elements, 
                    # which are rectangles made of multiple pixels. Use their width, height, 
                    # and upper-left coordinates to describe their position and area.
                    if c != "0":  
                        if self.major_place.get(c, None) is None:
                            self.major_place[c] = MajorPlaceUnit()
                            # for key,value in self.major_place.items():
                            #         print(key+": "+str(value))
                        
                        # Get the coordinates of the top left corner
                        if self.major_place[c].up_left_row == -1:  
                            self.major_place[c].up_left_row = row
                        if self.major_place[c].up_left_col == -1:  
                            self.major_place[c].up_left_col = col
                        
                        # Subtract the coordinate of the leftmost point from the coordinate
                        # of the rightmost point to determine the width.
                        if self.major_place[c].width < row - self.major_place[c].up_left_row:
                            self.major_place[c].width = row - self.major_place[c].up_left_row
                            
                        # Subtract the coordinate of the uppermost point from the coordinate
                        # of the lowest point to determine the height.
                            
                        if self.major_place[c].height < col - self.major_place[c].up_left_col:
                            self.major_place[c].height = col - self.major_place[c].up_left_col

                    map_line.append(mu)
                self.game_map.append(map_line)
                self.density_map.append([set() for i in range(MAP_SIZE)])

    def update_game_map(self):

        current_drunk = self.drunks[0]  # Drunk in the loop

        if self.police_meet_drunk:     
            
            """
            When the drunk appears in the line of sight of the police, the police 
            will appear in the position of the drunk, so it is necessary to reset 
            the color of the pixel where the policeman was before.
            """
            self.game_map[self.police.row][self.police.col].current_color = \
            self.game_map[self.police.row][self.police.col].color
            self.game_map[self.police.row][self.police.col].agents[1] = None
            # print("Presently the drunk met the policeman")
            
            # After sending the drunk home, the police resumed their patrols from where they drop the drunk
            if (self.game_map[current_drunk.row][current_drunk.row].val == str(current_drunk.drunk_id * 10))\
                    or (len(self.police_drunk_route) == 0):  
                self.police_meet_drunk = False
                self.game_map[self.police.row][self.police.col].agents[1] = self.police
                self.game_map[self.police.row][self.police.col].current_color = POLICE_COLOR
                self.police_drunk_route.clear()
                self.drunks.pop(0) # Remove drunk who has gone home from the list
                return
            
            for i in range(8):  # To accelerate the simulation
            
                if len(self.police_drunk_route) != 0:  
                    next_step = self.police_drunk_route[0]
                    # print("The next step is: " + str(next_step))
                    
                    # The route is planned in advance and the coordinates of 
                    # the route already passed need to be deleted
                    self.police_drunk_route.pop(0) 
                    # Update drunk and police's location
                    current_drunk.row, current_drunk.col = next_step[0], next_step[1]
                    self.police.row, self.police.col = next_step[0], next_step[1]
                    # Update game map
                    self.game_map[next_step[0]][next_step[1]].current_color = DRUNK_POLICE_MIX_COLOR
                    self.game_map[next_step[0]][next_step[1]].agents[0] = current_drunk
                    self.game_map[next_step[0]][next_step[1]].agents[1] = self.police
                    # Plot the route the police took the drunk home on the density map
                    self.density_map[current_drunk.row][current_drunk.col].add(current_drunk.drunk_id)  

        else:
            last_row, last_col = current_drunk.row, current_drunk.col
            # The drunk always starts from the top left corner of the bar
            if current_drunk.row == -1 and current_drunk.col == -1:  
                current_drunk.row = self.major_place[BAR_ID].up_left_row - 1
                current_drunk.col = self.major_place[BAR_ID].up_left_col
            
            # Reset the pixel the drunk has passed
            else:
                self.game_map[current_drunk.row][current_drunk.col].current_color = \
                self.game_map[current_drunk.row][current_drunk.col].color  
                self.game_map[current_drunk.row][current_drunk.col].agents[0] = None  
                current_drunk.choose_dir()
                
            # Drunk finds his own home without encountering the police (odds are almost zero)
            if self.game_map[current_drunk.row][current_drunk.col].val == str(current_drunk.drunk_id * 10):  
                self.police_meet_drunk = False
                self.drunks.pop(0)
            
            # Plot the road the drunk has passed on the density map
            elif self.game_map[current_drunk.row][current_drunk.row].val == '0':
                self.game_map[current_drunk.row][current_drunk.col].current_color = DRUNK_COLOR
                self.game_map[current_drunk.row][current_drunk.col].agents[0] = current_drunk
                self.density_map[current_drunk.row][current_drunk.col].add(current_drunk.drunk_id)  
            
            # Prevent drunks from entering other people's house and bar
            else:  
                # print("No Entrance! " + str(current_drunk.row, current_drunk.col))
                current_drunk.row, current_drunk.col = last_row, last_col # Stop the drunk 
                self.game_map[current_drunk.row][current_drunk.col].current_color = DRUNK_COLOR
                self.game_map[current_drunk.row][current_drunk.col].agents[0] = current_drunk
                self.density_map[current_drunk.row][current_drunk.col].add(current_drunk.drunk_id)  

            self.game_map[self.police.row][self.police.col].agents[1] = None
            self.game_map[self.police.row][self.police.col].current_color = \
            self.game_map[self.police.row][self.police.col].color  
            self.police.do_patrol()  # call do_patrol function
            
            # The police can't enter the house either
            if not self.game_map[self.police.row][self.police.col].val in [str(i*10) for i in range(1, 26)]:  
                self.game_map[self.police.row][self.police.col].agents[1] = self.police
                self.game_map[self.police.row][self.police.col].current_color = POLICE_COLOR

            # Determine if the drunk is in the view of the police
            if current_drunk.row in list(range(self.police.row-POLICE_VIEWS, self.police.row+POLICE_VIEWS)) and \
                current_drunk.col in list(range(self.police.col-POLICE_VIEWS, self.police.col+POLICE_VIEWS)):  
                self.game_map[self.police.row][self.police.col].current_color = \
                self.game_map[self.police.row][self.police.col].color 
                self.game_map[self.police.row][self.police.col].agents[1] = None
                # Policeman show up at the drunk's location
                self.police.row, self.police.col = current_drunk.row, current_drunk.col  
                self.game_map[self.police.row][self.police.col].current_color = DRUNK_POLICE_MIX_COLOR
                self.game_map[self.police.row][self.police.col].agents[0] = current_drunk
                self.game_map[self.police.row][self.police.col].agents[1] = self.police
               
                house_id = str(current_drunk.drunk_id * 10)
                row = current_drunk.row
                
                """
                In order to plan the path to take the drunk home, it is necessary to make two judgments: 
                first, judge whether the drunk's home is above or below the current position, 
                and then judge whether it is on the left or right of the current position.
                """
                # The drunk was under his house when the police found him
                if current_drunk.row > self.major_place[house_id].up_left_row + self.major_place[house_id].height:  
                    for i in range(current_drunk.row - 1,
                                   self.major_place[house_id].up_left_row + self.major_place[house_id].height-1,
                                   -1):
                        self.police_drunk_route.append([i, current_drunk.col])
                        row = i
                        
                # The drunk was on top of his house when the police found him
                elif current_drunk.row < self.major_place[house_id].up_left_row:  
                    for i in range(current_drunk.row + 1,
                                   self.major_place[house_id].up_left_row + 1):
                        self.police_drunk_route.append([i, current_drunk.col])
                        row = i
                
                # The drunk was on the right side of his house when the police found him
                if current_drunk.col > self.major_place[house_id].up_left_col + self.major_place[house_id].width:  
                    for j in range(current_drunk.col - 1,
                                   self.major_place[house_id].up_left_col + self.major_place[house_id].width - 1,
                                   -1):
                        self.police_drunk_route.append([row, j])
                        
                # The drunk was on the left side of his house when the police found him
                elif current_drunk.col < self.major_place[house_id].up_left_col:  
                    for j in range(current_drunk.col + 1,
                                   self.major_place[house_id].up_left_col + 1):
                        self.police_drunk_route.append([row, j])
                        
                self.police_meet_drunk = True
                # print("The route to take the drunk home is: " + str(self.police_drunk_route))
        self.label_map.update()

    def slot_btn_start(self):
        
        # Begin to simulate
        self.on_work = True
        self.drunks = [Drunk(i+1) for i in range(DRUNK_PEOPLE)]
        # print(self.drunks)
        self.timer.start(50)  # Run every 50ms

    def slot_btn_draw(self):
        
    # Draw density map and save it as a text file
        main_window = QtWidgets.QDialog()
        # Save the density map with the current time as its file name
        # Reference: https://www.cnblogs.com/Army-Knife/p/10689599.html
        with open(f"{datetime.datetime.now().strftime('%y_%m_%d_%H_%M')}_density_map.txt", 'w') as f:
            for line in self.density_map:
                f.write(",".join([str(len(i)) for i in line]) + "\n")
                
        dm = DensityMap.DensityMap(main_window, self.density_map)
        main_window.exec()

