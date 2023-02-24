import pygame
import random
from typing import Tuple

class BlobBox:
    
    def __init__(self, row: int, col: int, size: int, color: Tuple[int], maxBlobs: int):
        self.row: int = row
        self.col: int = col
        self.size: int = size
        self.blob: int = 0
        self.theta: int = 0
        self.color: Tuple[int] = color
        self.maxBlobs: int = maxBlobs
        
    def draw(self, win: pygame.Surface):

        if self.blob == 1:
            pass
        elif self.blob == 2:
            pass
        elif self.blob == 3:
            pass
    
    def addBlob(self, color: Tuple[int]) -> bool:
        self.color = color
        self.blob += 1
        
        return self.isFull()
    
    def isFull(self) -> bool:
        return self.blob > self.maxBlobs
    
    def getColor(self) -> Tuple[int]:
        return self.color
    
    def getPosition(self) -> Tuple[int]:
        return self.row, self.col
    
    def setBlobs(self, blob: int) -> None:
        self.blob = blob
        
    def getBlob(self) -> int:
        return self.blob

    def __del__(self):
        pass

