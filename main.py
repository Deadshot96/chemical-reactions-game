import pygame
import numpy as np
from settings import *
from colors import *
from blob import BlobBox
import random

class ChemicalReaction:
    
    color_store = [RED, GREEN, BLUE, SKYBLUE, MINT_CREAM, SALMON]
    
    def __init__(self, players=2):
        self.width = WIDTH
        self.height = HEIGHT
        self.xoff = X_OFF
        self.yoff = Y_OFF
        self.gameWinWidth = GAMEWIN_WIDTH
        self.gameWinHeight = GAMEWIN_HEIGHT
        self.rows = ROWS
        self.cols = COLS
        self.row = 0
        self.col = 0
        self.players = players
        self.player = 0
        self.player_colors = ChemicalReaction.color_store[:min(self.players, MAX_PLAYERS)]
        self.fps = FPS
        self.clock = None
        self.titleFont = None
        self.grid = None
        self.win = None
        self.gameWin = None
        self.gameWinRect = None
        self.outerGrid = []
        self.innerGrid = []
        self.scaleDown = 0.96
        

    def grid_init(self):
        pygame.init()
        pygame.font.init()
        
        self.win = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(TITLE)
        
        self.gameWinRect = pygame.Rect(self.xoff, self.yoff, self.gameWinWidth, self.gameWinHeight)
        self.gameWin = self.win.subsurface(self.gameWinRect)
        
        self.win.fill(MID_BLACK)
        self.gameWin.fill(BLACK)
        
        self.titleFont = pygame.font.SysFont(TITLE_FONT, FONT_SIZE)
        title = self.titleFont.render(TITLE, 1, GOLD)
        w, h = title.get_size()
        blitX = (self.width - w) // 2
        blitY = (self.yoff - h) // 2
        self.win.blit(title, (blitX, blitY))
        
        self.clock = pygame.time.Clock()
        
        x_size = self.gameWinWidth // self.cols
        y_size = self.gameWinHeight // self.rows
        
        for row in range(self.rows + 1):
            self.outerGrid.append([])
            for col in range(self.cols + 1):
                self.outerGrid[row].append((col * y_size, row * x_size))
        
        self.outerGrid = np.array(self.outerGrid, dtype=np.uint32)
        self.innerGrid = self.outerGrid - np.array([self.gameWinWidth // 2, self.gameWinHeight // 2], dtype=np.int32)
        self.innerGrid = self.innerGrid * [self.scaleDown, self.scaleDown]
        self.innerGrid = self.innerGrid + np.array([self.gameWinWidth // 2, self.gameWinHeight // 2], dtype=np.uint32)

        pygame.display.update()


    def close(self):
        pygame.font.quit()
        pygame.quit()


    def draw(self):
        self.gameWin.fill(BLACK)
        self.draw_grid_lines()
        pygame.display.update()
        
    def draw_grid_lines(self):
        linewidth = 1
        color = self.player_colors[self.player]
        
        for row in self.outerGrid:
            pygame.draw.line(self.gameWin, color, row[0], row[-1])
            
        for colIndex in range(len(self.outerGrid[0])):
            pygame.draw.line(self.gameWin, color, self.outerGrid[0][colIndex], self.outerGrid[-1][colIndex])
            
            
        for row in self.innerGrid:
            pygame.draw.line(self.gameWin, color, row[0], row[-1])
            
        for colIndex in range(len(self.innerGrid[0])):
            pygame.draw.line(self.gameWin, color, self.innerGrid[0][colIndex], self.innerGrid[-1][colIndex])
            
            
        rows, cols = self.outerGrid.shape[:2]
        for row in range(rows):
            for col in range(cols):
                pygame.draw.line(self.gameWin, color, self.outerGrid[row][col], self.innerGrid[row][col])
                
                

        select_box_color = YELLOW
        offsets = ((0, 0), (0, 1), (1, 1), (1, 0), (0, 0))
        for grid in (self.outerGrid, self.innerGrid):
            for index in range(len(offsets) - 1):
                rSrc, cSrc = self.row + offsets[index][0], self.col + offsets[index][1]
                rDst, cDst = self.row + offsets[index + 1][0], self.col + offsets[index + 1][1]
                pygame.draw.line(self.gameWin, select_box_color, grid[rSrc][cSrc], grid[rDst][cDst], 2)
        
        
        for rdiff, cdiff in offsets[:-1]:
            r = self.row + rdiff
            c = self.col + cdiff
            pygame.draw.line(self.gameWin, select_box_color, self.outerGrid[r][c], self.innerGrid[r][c], 2)
        

        # x_size = self.gameWinWidth // self.cols
        # y_size = self.gameWinHeight // self.rows

        # for row in range(self.rows + 1):
        #     pygame.draw.line(self.gameWin, color, (0, row * y_size), (self.gameWinWidth, row * y_size))

        # for col in range(self.cols + 1):
        #     pygame.draw.line(self.gameWin, color, (col * x_size, 0), (col * x_size, self.gameWinHeight))
            
    def isValid(self, row: int, col: int) -> bool:
        return row in range(self.rows) and col in range(self.cols)
    
    def hopBlock(self, xdiff: int, ydiff: int) -> None:
        if self.isValid(self.row + xdiff, self.col + ydiff):
            self.row += xdiff
            self.col += ydiff

    def run(self):
        if not pygame.display.init():
            self.grid_init()
            
        run = True
        while run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                if event.type == pygame.KEYDOWN:
                    keys = pygame.key.get_pressed()
                    
                    if keys[pygame.K_DOWN]:
                        self.hopBlock(1, 0)

                    if keys[pygame.K_UP]:
                        self.hopBlock(-1, 0)
                        
                    if keys[pygame.K_RIGHT]:
                        self.hopBlock(0, 1)
                        
                    if keys[pygame.K_LEFT]:
                        self.hopBlock(0, -1)
                    
            self.draw()            
        self.close()
        


if __name__ == "__main__":
    print("Hello, World!")
    X = ChemicalReaction()
    X.run()