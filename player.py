import pygame
import pygame.gfxdraw
import math

class Player:
    def __init__(self, x, y, color, direction, controls, speed, grid_size, player_id):
        self.x = x
        self.y = y
        self.color = color
        self.direction = direction
        self.controls = controls
        self.speed = speed
        self.grid_size = grid_size
        self.id = player_id
        self.alive = True
        self.trail = [(x, y)]  
        self.size = max(grid_size // 2, 3)  
        
        self.head_color = tuple(min(c + 50, 255) for c in color)
    
    def handle_input(self, key):

        if key == self.controls["up"] and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == self.controls["down"] and self.direction != (0, -1):
            self.direction = (0, 1)
        elif key == self.controls["left"] and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == self.controls["right"] and self.direction != (-1, 0):
            self.direction = (1, 0)
    
    def update(self):

        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        
        self.trail.append((self.x, self.y))
        
        if len(self.trail) > 1000:
            self.trail = self.trail[-1000:]
    
    def draw(self, surface):

        pygame.gfxdraw.filled_circle(surface, int(self.x), int(self.y), self.size, self.head_color)
        pygame.gfxdraw.aacircle(surface, int(self.x), int(self.y), self.size, self.head_color)
    
    def draw_trail(self, surface):

        if len(self.trail) > 1:

            points = [(int(x), int(y)) for x, y in self.trail]
            

            if len(points) >= 2:
                p1 = points[-2]
                p2 = points[-1]
                
                dist = math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2)
                
                if dist > self.speed:
                    steps = int(dist / 2) + 1
                    for i in range(1, steps):
                        t = i / steps
                        ix = int(p1[0] + (p2[0] - p1[0]) * t)
                        iy = int(p1[1] + (p2[1] - p1[1]) * t)
                        pygame.gfxdraw.filled_circle(surface, ix, iy, self.size, self.color)
                
                pygame.draw.line(surface, self.color, p1, p2, self.size * 2)
                
                pygame.gfxdraw.filled_circle(surface, p2[0], p2[1], self.size, self.color)