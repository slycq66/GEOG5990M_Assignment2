# -*- coding: utf-8 -*-
"""
Student Id: 201581226
"""

from GameMap import *
import sys

if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QDialog()
    game_map = GameMap(main_window)
    main_window.show()
    sys.exit(app.exec_())
