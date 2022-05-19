# -*- coding: utf-8 -*-
"""
Student Id: 201581226
"""

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QColor, QPen
from PyQt5.QtWidgets import QWidget, QVBoxLayout

import SubWindow
from agents import *

"""
Attributes for each pixel on the density map.

    val -- represents the number of times a drunk walks by
    
    color -- the more times the drunk walks past the pixel, the redder the color
"""
class DensityMapUnit:
    
    def __init__(self, _color, _val):
        self.color = _color
        self.val = _val
        
        
"""
Draw each pixel as a 4*4 rectangel label on the map and update the map after agents moving. 

Inherit standard QLabel class.  

Reference: https://blog.csdn.net/zzzzjh/article/details/82985209
""" 
class LabelDensityMap(QtWidgets.QLabel):
    
    def __init__(self, parent, _map: DensityMapUnit):
        
        # Call superclass's __init__ function
        super().__init__(parent=parent)
        # Set the map size corresponding to the drawRect in the paintEvent event
        # Because the original size is 300 * 300 and area of label is 4*4，
        # the label map size is 300*4.
        self.setFixedSize(QSize(1200, 1200))
        self.map = _map

    def paintEvent(self, event):
        
        super().paintEvent(event)
        qp = QtGui.QPainter(self)
        # Set Qpen color and width
        qp.setPen(QPen(QColor(0, 0, 0), 1))
        qp.begin(self)
        for row in range(MAP_SIZE):
            for col in range(MAP_SIZE):
                # Fill the rectangle with current color
                br = QtGui.QBrush(QtGui.QColor(self.map[row][col].color))
                qp.setBrush(br)
                qp.drawRect(QtCore.QRect(row*4, col*4, 4, 4))
        qp.end()

    def update_map(self, _map):
        self.map = _map
        self.update()

"""
Inherit Ui_Dialog class from SubWindow.py
"""
class DensityMap(SubWindow.Ui_Dialog):
    
    def __init__(self, dialog, _map: set()):
        
        super().setupUi(dialog)  # Call setupUi of the parent class
        self.density_map: DensityMapUnit = list()  # Initialize the DensityMapUnit
        
        # Fill the list
        for i in range(len(_map)):
            dm_list = list()
            for j in _map[i]:
                val = len(j)
                dm = DensityMapUnit(Density_Color[val], val)
                dm_list.append(dm)
            self.density_map.append(dm_list)
        
        # Create custom Label objects and add them to the UI's scrollArea control using QVBoxLayout
        self.density_map_label: LabelDensityMap = LabelDensityMap(None, self.density_map)
        widget = QWidget()
        la = QVBoxLayout()
        widget.setLayout(la)
        la.addWidget(self.density_map_label)
        self.scrollArea.setWidget(widget)
        
        # Creat legend for density map
        for i, color in enumerate(Density_Color):
            label = QtWidgets.QLabel()
            label.setFixedSize(QSize(160, 25))
            label.setText(f"{i}")
            label.setStyleSheet(f"background-color:{color};color:black")
            self.verticalLayout_legend.addWidget(label)

