#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 19:49:06 2020

@author: sebastiendevilliers
"""

import tkinter as tk
from minesweeper import MineSweeperGame

class MineSweeperUI:
    def __init__(self):
        self.tkWindow = None
        self.curGame = None
        self.frame = None
        self.buttons = {}
        self.newGameBtn = None
        self.scaleValues = list()
    
    def setupGame(self, tkWindow, game):
        _,rows,cols = game.grid.shape
        mineCount = game.mineCount
        
        self.tkWindow = tkWindow
        self.curGame = game
        self.buttons = MineSweeperUI.addButtons(self.tkWindow, game, (0,0))
        self.newGameBtn = self.addNewGameBtn(self.tkWindow, (rows,0), cols)
        self.scaleValues = MineSweeperUI.addScales(self.tkWindow, rows, cols, mineCount)
        
        self.redrawTitle()
    
    
    def newGame(self):
        [rows, cols, mineCount] = self.readScales()
        MineSweeperUI.clear(self.tkWindow)
        self.setupGame(self.tkWindow, MineSweeperGame((rows,cols),mineCount,self.curGame.key+1))
        
        
    def redrawTitle(self):
        self.tkWindow.title("MineSweeper - Game {}".format(self.curGame.key))
    
    def readScales(self):
        return [val.get() for val in self.scaleValues]
        
    def clear(window):
        list = window.grid_slaves()
        for l in list:
            l.destroy()
    
    def addNewGameBtn(self, toWindow, gridLocation, columnSpan):
        newGameBtn = tk.Button(toWindow, text="New Game", command=self.newGame)
        newGameBtn.grid(row=gridLocation[0], column=gridLocation[1], columnspan=columnSpan)
        return newGameBtn
    
    def addScales(toWindow, rows, cols, mineCount):
        # rows
        rowVal = tk.IntVar()
        rowVal.set(rows)
        rowLabel = tk.Label(toWindow, text="Rows")
        rowLabel.grid(row=rows+1, column=0, columnspan=3)
        rowScale = tk.Scale(toWindow, variable = rowVal, from_ = 1, to = 50, orient = tk.HORIZONTAL )
        rowScale.grid(row=rows+1, column=3, columnspan=cols-4) 
        
        # cols
        colVal = tk.IntVar()
        colVal.set(cols)
        colLabel = tk.Label(toWindow, text="Columns")
        colLabel.grid(row=rows+2, column=0, columnspan=3)
        colScale = tk.Scale(toWindow, variable = colVal, from_ = 1, to = 50, orient = tk.HORIZONTAL )
        colScale.grid(row=rows+2, column=3, columnspan=cols-4) 
        
        # mineCount
        mineCountVal = tk.IntVar()
        mineCountVal.set(mineCount)
        mineCoundLabel = tk.Label(toWindow, text="Mines")
        mineCoundLabel.grid(row=rows+3, column=0, columnspan=3)
        mineCountScale = tk.Scale(toWindow, variable = mineCountVal, from_ = 1, to = 50, orient = tk.HORIZONTAL )
        mineCountScale.grid(row=rows+3, column=3, columnspan=cols-4) 
        
        return [rowVal, colVal, mineCountVal]
        
    def addButtons(toWindow, fromGame, startCell):
        """
        Adds all buttons fromGame toWindow in a grid the same shape as
        fromGame.grid.shape[1:2]
        
        Parameters
        ----------
        startCell : (int,int)
            The (row,col) of the cell in the grid where the top left button should go.
            
        Returns
        -------
        buttons : dict
            buttons[i,j] contains the button at row i and column j.

        """
        buttons = {}
        _,rows,cols = fromGame.grid.shape
        for row in range(rows):
            for col in range(cols):
                # set text
                btnText = fromGame.toChar(*fromGame.grid[:,row,col])
                btn = tk.Label(toWindow, text=btnText)
                # bind actions
                release = lambda event, row=row, col=col: MineSweeperUI.buttonReleased(event,fromGame,buttons,row,col)
                btn.bind("<ButtonPress>", MineSweeperUI.buttonPressed)
                btn.bind("<ButtonRelease>", release)
                # layout in grid
                btn.grid(row=row+startCell[0], column=col+startCell[1])
                buttons[row,col] = btn
        return buttons
    
    def buttonReleased(event, game, buttons, row, col):
        event.widget.configure(bg="#E7E7E7")
        if event.num == 1:
            game.reveal(row,col)
        else:
            game.mark(row,col)
        MineSweeperUI.redrawButtons(buttons, game)
    
    def buttonPressed(event):
        if event.num == 1:
            event.widget.configure(bg="white")
        else:
            event.widget.configure(bg="#777777")
    
    def redrawButtons(buttons, game):
        """
        Updates the text of all buttons. 
        We expect the buttons dictionary to have rows*cols buttons
        """
        _,rows,cols = game.grid.shape
        for row in range(rows):
            for col in range(cols):
                btnText = game.toChar(*game.grid[:,row,col])
                buttons[row,col].configure(text=btnText, bg="#E7E7E7")
