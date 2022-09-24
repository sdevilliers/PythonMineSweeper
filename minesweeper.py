#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 11:45:27 2020

@author: sebastiendevilliers
"""

import random
import numpy as np

class MineSweeperGame:
    
    def __init__(self, dims, mineCount, key):
        self.key = key
        self.mineCount = mineCount
        mask = np.ones(dims, 'int')
        mineMap = self.generate_mineMap(dims, mineCount)
        self.grid = np.array([mask,mineMap]) # shape = (2, dims[0], dims[1])
    
    def generate_mineMap(self, dims, mineCount):
        n = dims[0]*dims[1]
        mineIdxs = random.choices(range(n),k=mineCount)
       
        # set the mines
        mineMap = np.zeros(n, 'int')
        mineMap[mineIdxs] = -1
        mineMap = mineMap.reshape(dims)
        
        # loop mine locations
        for i,j in toIJIndxs(mineIdxs,dims,True):
            # loop mine neighbors that haven't yet been assigned a count
            notCounted = lambda a,b: mineMap[a,b] == 0
            for row,col in list(neighbors(i,j,mineMap,filterfn=notCounted)):
                # assign a count
                mineMap[row,col] = self.countMines(row,col,mineMap)
            
        return mineMap
        
    def countMines(self,i,j,mineMap):
        """ Counts the number of mines next to index (i,j) """
        mineCount = 0
        for row,col in list(neighbors(i,j,mineMap)):
            if mineMap[row,col] == -1:
                mineCount += 1
        return mineCount
    
    def toChar(self, maskNum, mineMapNum):
        # ⬜⬛☼💣💥⚐
        if maskNum == 1:
            return '⬛'
        elif maskNum == 2:
            return '⚐'
        elif maskNum == 3:
            return '?'
        else:
            if mineMapNum == -1:
                return '💥'
            elif mineMapNum == 0:
                return '⬜'
            else:
                return str(mineMapNum)+' '
    
    def getDisp(self):
        dims = (self.grid.shape[1],self.grid.shape[2])
        n = self.grid.shape[1]*self.grid.shape[2]
        gridIdxs = range(n)
        return np.array([self.toChar(*self.grid[:,i,j]) for i,j in toIJIndxs(gridIdxs, dims, True)]).reshape(dims)
        
    def reveal(self, i, j):
        mask = self.grid[0]
        mineMap = self.grid[1]
        
        # print('unmasking a',mineMap[i,j], 'at ({},{})'.format(i,j))
        mask[i,j] = 0
        if mineMap[i,j] == 0:
            # print('recursiveReveal')
            self.recursiveReveal(i,j)
        
        if mineMap[i,j] == -1:
            mask[mineMap == -1] = 0
            print("GAME OVER")
        elif (mineMap[mask != 0] == -1).all():
            mask[mineMap == -1] = 2
            print("YOU WON")
        
        # print(self.getDisp())
    
    def recursiveReveal(self, i, j):
        mask = self.grid[0]
        mineMap = self.grid[1]
        # print(i,j)
        # reveal all neghbors not yet revealed
        hidden = lambda a,b: mask[a,b] != 0
        hiddenNeighborsOfIJ = neighbors(i,j,mineMap,filterfn=hidden)
        for row,col in hiddenNeighborsOfIJ:
            # print('unmasking a',mineMap[row,col], 'at ({},{})'.format(row,col))
            mask[row,col] = 0
        
        isZero = lambda a,b: mineMap[a,b] == 0
        revealedZeros = np.array([idx for idx in list(hiddenNeighborsOfIJ) if isZero(*idx)])
        # for each element revealed that is a zero
        for row,col in revealedZeros:
            self.recursiveReveal(row, col)
    
    def mark(self,i,j):
        self.grid[0,i,j] += 1
        if self.grid[0,i,j] == 4:
            self.grid[0,i,j] = 1
        # print(self.getDisp())
        
# ------ end class MineSweepersGame ------------------------------------------

def neighbors(i,j,mineMap,forLooping = True, filterfn = lambda row,col: True):
    """ Finds neighboring indices/elements of index (i,j) in mineMap 
        - forLooping: returns [[row1,col1],[row2,col2]...] if True
                      returns [row1,row2,...] , [col1,col2,...] if False
                      the latter can be used to directly index 2D array
        - filterfn: allows you to filter out neighbors that were already counted
            input: [row,col] 
            output: False to exclude this index, True to include
    """
    # are we on an edge or corner?
    left = j   if j == 0                    else j-1
    right = j  if j == mineMap.shape[1] - 1 else j+1
    top = i    if i == 0                    else i-1
    bottom = i if i == mineMap.shape[0] - 1 else i+1
    
    # all the indexes including (i,j)
    neighboring = np.array([[(row,col) for row in range(top,bottom+1)] for col in range(left,right+1)])
    # flatten
    neighboring = neighboring.reshape((neighboring.shape[0]*neighboring.shape[1], 2))
    # filter out (i,j) ... and whatever filterfn wants us to filter
    valid = lambda idx: list(idx) != [i,j] and filterfn(*idx)
    neighboring = np.array([idx for idx in list(neighboring) if valid(idx)])
    
    if forLooping:
        return neighboring
    else:
        rowIdxs = neighboring[:,0]
        colIdxs = neighboring[:,1]
        return rowIdxs, colIdxs

def toIJIndxs(linearIdxs, dims, forLooping = False):
    ijIndxs = np.array([(int(mineIdx / dims[1]), mineIdx % dims[1]) for mineIdx in linearIdxs])
    if forLooping:
        return ijIndxs
    else:
        rowIdxs = ijIndxs[:,0]
        colIdxs = ijIndxs[:,1]
        return rowIdxs, colIdxs
    
