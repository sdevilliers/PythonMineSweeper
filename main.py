#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 12:42:50 2022

@author: sebastiendevilliers
"""

import tkinter as tk
from minesweeper import MineSweeperGame
from gui import MineSweeperUI

ui = MineSweeperUI()
root = tk.Tk()

ui.setupGame(root, MineSweeperGame((10,10),10,1))

root.mainloop()