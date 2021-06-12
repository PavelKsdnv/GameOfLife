# Make Conway's Game of Life and visualize it using pygame module
#TODO:
#1) Cell class
#   -Function for next state ~X~
#2) Board class
#   - Create board list ~X~
#   - Function for randomization of initial cells ~X~
#   - Function for advancing the whole board ~X~
#   - Function for connecting all the neighbours in the start of the game ~X~
#3) Create a main loop, where the game will take place, visualize it in the console for the start
#4) Make the game look better using pygame, still unsure how that's gonna happen lol 
import random
import time
import pygame
import sys

CELLSIZE = 40
WIDTH = 800
HEIGHT = 600
ROWS = int(HEIGHT / CELLSIZE)
COLUMNS = int(WIDTH / CELLSIZE)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (88, 168, 118)
ORANGE = (242, 199, 138)
GRAY_GREEN = (125, 138, 130)


class Cell():
    isPointed = False
    isAlive = False
    neighbours : list[int]
    isAliveNext : bool

    def DetermineNextState(self):
        """ Deterimines if in the next frame of the simulation
            The cell will be alive or not. The rules are:
            Alive cells with more than 3 neighbours die
            Alive cells with less than 2 neighbours die
            Dead cells with 3 neighbours become alive """
        
        aliveNeighbours = 0
        for x in range(len(self.neighbours)):
            if self.neighbours[x].isAlive : aliveNeighbours += 1

        if self.isAlive:
            self.isAliveNext = aliveNeighbours == 2 or aliveNeighbours == 3
        else:
            self.isAliveNext = aliveNeighbours == 3

    def Advance(self):
        self.isAlive = self.isAliveNext

class Board():
    rows : int
    columns : int
    cells =[[]]

    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x].append(Cell())
            self.cells.append([])
        self.ConnectCells()
    
    def RandomizeCells(self, randomChance):
        r = random
        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x][y].isAlive = r.randint(0, 100) < randomChance
                

    def ConnectCells(self):
        for x in range(self.columns):
            for y in range(self.rows):
                # xL - left, xR - right, yT - top, yB - bottom
                # determining the coordinates of the neghbours and wrapping around the board if they are on the edge
                xL = x - 1 if x > 0 else self.columns - 1
                xR = x + 1 if x < self.columns - 1 else 0

                yT = y - 1 if y > 0 else self.rows - 1
                yB = y + 1 if y < self.rows - 1 else 0
                # Adding all the neighbours to the list of every cell
                self.cells[x][y].neighbours = [
                    self.cells[xL][y],
                    self.cells[xR][y],
                    self.cells[x][yT],
                    self.cells[x][yB],
                    self.cells[xL][yT],
                    self.cells[xR][yT],
                    self.cells[xR][yB],
                    self.cells[xL][yB]
                ]
    
    def Advance(self):
        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x][y].DetermineNextState()

        for x in range(self.columns):
            for y in range(self.rows):
                self.cells[x][y].Advance()

    def Visualize(self):
        for x in range(self.columns):
            for y in range(self.rows):
                rectangle = pygame.Rect(x * CELLSIZE, y * CELLSIZE, CELLSIZE, CELLSIZE)
                if self.cells[x][y].isAlive : SCREEN.fill(GREEN, rectangle) 
                else : SCREEN.fill(ORANGE, rectangle)
                pygame.draw.rect(SCREEN, BLACK, rectangle, 1)

        pygame.display.update()

def main():
    Paused = False

    while True:
        board.Visualize()
        # Main game Loop
        if not Paused:
            board.Advance()
            time.sleep(0.5)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ChangeCellState(event.pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                Paused = not Paused
    

def ChangeCellState(mouse: tuple):
    mouseX = int(mouse[0]/CELLSIZE)
    mouseY = int(mouse[1]/CELLSIZE)
    board.cells[mouseX][mouseY].isAlive = not board.cells[mouseX][mouseY].isAlive

            
    

if __name__ == '__main__':
    global SCREEN
    
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

    board = Board(ROWS, COLUMNS)
    main()