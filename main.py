import pygame
import numpy as np
from settings import *
from colors import *

class ChemicalReaction:
    
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.xoff = X_OFF
        self.yoff = Y_OFF
        self.gameWinWidth = GAMEWIN_WIDTH
        self.gameWinHeight = GAMEWIN_HEIGHT
        self.rows = ROWS
        self.cols = COLS
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
    
        # print(self.innerGrid)
    
        pygame.display.update()


    def close(self):
        pygame.font.quit()
        pygame.quit()


    def draw(self):
        self.draw_grid_lines()
        pygame.display.update()
        
    def draw_grid_lines(self):
        linewidth = 1
        color = SIENNA
        
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

            
            
        
        # x_size = self.gameWinWidth // self.cols
        # y_size = self.gameWinHeight // self.rows

        # for row in range(self.rows + 1):
        #     pygame.draw.line(self.gameWin, color, (0, row * y_size), (self.gameWinWidth, row * y_size))

        # for col in range(self.cols + 1):
        #     pygame.draw.line(self.gameWin, color, (col * x_size, 0), (col * x_size, self.gameWinHeight))
            
            
            

    def run(self):
        if not pygame.display.init():
            self.grid_init()
            
        run = True
        while run:
            self.clock.tick(self.fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    
            self.draw()            
        self.close()
        


if __name__ == "__main__":
    print("Hello, World!")
    X = ChemicalReaction()
    X.run()