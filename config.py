import pygame
import pygame.gfxdraw

class Config:
    def __init__(self):
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 60
        self.player_count = 2
        self.player_speed = 3
        self.grid_size = 10
        self.player_colors = [
            (0, 255, 255),    # Cyan (Player 1)
            (255, 50, 50),    # Red (Player 2)
            (50, 255, 50),    # Green (Player 3)
            (255, 255, 0)     # Yellow (Player 4)
        ]
        self.bg_color = (0, 0, 30)
        self.grid_color = (20, 20, 50)

class Button:
    def __init__(self, x, y, width, height, text, color=(100, 100, 255), hover_color=(150, 150, 255)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.is_hovered = False
        
    def draw(self, surface, font):
        pygame.draw.rect(surface, self.current_color, self.rect, border_radius=5)
        pygame.draw.rect(surface, (255, 255, 255), self.rect, 2, border_radius=5)
        
        text_surf = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.current_color = self.hover_color if self.is_hovered else self.color
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = initial_val
        self.label = label
        self.dragging = False
        self.handle_radius = 10
        self.handle_pos = self._value_to_pos(initial_val)
        
    def _value_to_pos(self, value):
        return int(((value - self.min_val) / (self.max_val - self.min_val)) * self.rect.width) + self.rect.x
    
    def _pos_to_value(self, pos):
        relative_pos = max(0, min(pos - self.rect.x, self.rect.width))
        return self.min_val + (relative_pos / self.rect.width) * (self.max_val - self.min_val)
    
    def draw(self, surface, font):

        pygame.draw.rect(surface, (80, 80, 100), self.rect, border_radius=3)
        
        pygame.gfxdraw.filled_circle(surface, self.handle_pos, self.rect.centery, 
                                    self.handle_radius, (150, 150, 255))
        pygame.gfxdraw.aacircle(surface, self.handle_pos, self.rect.centery, 
                               self.handle_radius, (255, 255, 255))
        
        label_surf = font.render(f"{self.label}: {int(self.value)}", True, (255, 255, 255))
        label_rect = label_surf.get_rect(bottomleft=(self.rect.x, self.rect.y - 5))
        surface.blit(label_surf, label_rect)
    
    def update(self, events, mouse_pos):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                handle_rect = pygame.Rect(self.handle_pos - self.handle_radius, 
                                         self.rect.centery - self.handle_radius,
                                         self.handle_radius * 2, self.handle_radius * 2)
                if handle_rect.collidepoint(mouse_pos):
                    self.dragging = True
            
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.dragging = False
                
        if self.dragging:
            self.handle_pos = max(self.rect.x, min(mouse_pos[0], self.rect.x + self.rect.width))
            self.value = self._pos_to_value(self.handle_pos)

class ConfigWindow:
    def __init__(self):
        self.config = Config()
        self.width = 600
        self.height = 500
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Tron - Configuration")
        self.font = pygame.font.SysFont("Arial", 20)
        self.title_font = pygame.font.SysFont("Arial", 32, bold=True)
        
        self.player_count_slider = Slider(150, 150, 300, 10, 2, 4, self.config.player_count, "Players")
        self.speed_slider = Slider(150, 200, 300, 10, 1, 10, self.config.player_speed, "Speed")
        self.grid_size_slider = Slider(150, 250, 300, 10, 5, 20, self.config.grid_size, "Grid Size")
        
        self.start_button = Button(200, 350, 200, 50, "Start Game", (0, 150, 0), (0, 200, 0))
        self.quit_button = Button(200, 420, 200, 50, "Quit", (150, 0, 0), (200, 0, 0))
        
    def show(self):
        clock = pygame.time.Clock()
        running = True
        
        while running:
            events = pygame.event.get()
            mouse_pos = pygame.mouse.get_pos()
            
            for event in events:
                if event.type == pygame.QUIT:
                    return None
                
                if self.start_button.is_clicked(event):

                    self.config.player_count = int(self.player_count_slider.value)
                    self.config.player_speed = int(self.speed_slider.value)
                    self.config.grid_size = int(self.grid_size_slider.value)
                    return self.config
                
                if self.quit_button.is_clicked(event):
                    return None
            
            self.player_count_slider.update(events, mouse_pos)
            self.speed_slider.update(events, mouse_pos)
            self.grid_size_slider.update(events, mouse_pos)
            self.start_button.update(mouse_pos)
            self.quit_button.update(mouse_pos)
            
            self.screen.fill((20, 20, 40))
            
            title_surf = self.title_font.render("TRON GAME CONFIGURATION", True, (0, 200, 255))
            title_rect = title_surf.get_rect(center=(self.width // 2, 70))
            self.screen.blit(title_surf, title_rect)
            
            self.player_count_slider.draw(self.screen, self.font)
            self.speed_slider.draw(self.screen, self.font)
            self.grid_size_slider.draw(self.screen, self.font)
            self.start_button.draw(self.screen, self.font)
            self.quit_button.draw(self.screen, self.font)
            
            pygame.display.flip()
            clock.tick(60)
        
        return None