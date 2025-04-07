import pygame
import sys
from player import Player
import math

class Game:
    def __init__(self, config):
        self.config = config
        self.screen = pygame.display.set_mode((config.screen_width, config.screen_height))
        pygame.display.set_caption("Tron")
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_over = False
        self.winner = None
        
        self.trail_surface = pygame.Surface((config.screen_width, config.screen_height), pygame.SRCALPHA)
        self.trail_surface.fill((0, 0, 0, 0))  
        
        self.players = []
        self.create_players()
        
        self.font = pygame.font.SysFont("Arial", 36, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 24)
        
        self.grace_period = 60 
        self.frame_count = 0
        
        self.trail_segments = []
        
    def create_players(self):

        grid = self.config.grid_size
        positions = [
            (self.config.screen_width // 4 // grid * grid, self.config.screen_height // 2 // grid * grid),
            (3 * self.config.screen_width // 4 // grid * grid, self.config.screen_height // 2 // grid * grid),
            (self.config.screen_width // 2 // grid * grid, self.config.screen_height // 4 // grid * grid),
            (self.config.screen_width // 2 // grid * grid, 3 * self.config.screen_height // 4 // grid * grid)
        ]
        
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        
        controls = [
            {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d},
            {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT},
            {"up": pygame.K_i, "down": pygame.K_k, "left": pygame.K_j, "right": pygame.K_l},
            {"up": pygame.K_t, "down": pygame.K_g, "left": pygame.K_f, "right": pygame.K_h}
        ]
        
        for i in range(self.config.player_count):
            self.players.append(
                Player(
                    positions[i][0], positions[i][1],
                    self.config.player_colors[i],
                    directions[i],
                    controls[i],
                    self.config.player_speed,
                    self.config.grid_size,
                    i + 1
                )
            )
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                
                for player in self.players:
                    if player.alive:
                        player.handle_input(event.key)
    
    def update(self):
        if self.game_over:
            return
            
        self.frame_count += 1
        
        for player in self.players:
            if player.alive:

                prev_x, prev_y = player.x, player.y
                
                player.update()
                
                if len(player.trail) >= 2:
                    segment = (player.trail[-2], player.trail[-1], player.id, player.size)
                    self.trail_segments.append(segment)
                
                player.draw_trail(self.trail_surface)
                
                if (player.x < 0 or player.x >= self.config.screen_width or
                    player.y < 0 or player.y >= self.config.screen_height):
                    player.alive = False
                
                if self.frame_count > self.grace_period:
                    if self.check_collision(player):
                        player.alive = False
        
        alive_players = [p for p in self.players if p.alive]
        if len(alive_players) <= 1:
            self.game_over = True
            if alive_players:
                self.winner = alive_players[0]
    
    def check_collision(self, player):

        try:

            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    check_x = int(player.x + dx)
                    check_y = int(player.y + dy)
                    
                    if (check_x < 0 or check_x >= self.config.screen_width or
                        check_y < 0 or check_y >= self.config.screen_height):
                        continue
                    
                    color = self.trail_surface.get_at((check_x, check_y))
                    if color[3] > 50:
                        head_dist = math.sqrt((check_x - player.x)**2 + (check_y - player.y)**2)
                        if head_dist > player.size:
                            return True
        except IndexError:

            return True
        
        p1 = player.trail[-2] if len(player.trail) >= 2 else (player.x - player.direction[0] * 10, 
                                                             player.y - player.direction[1] * 10)
        p2 = (player.x, player.y)
        
        for segment in self.trail_segments:
            q1, q2, segment_player_id, _ = segment
            
            if segment_player_id == player.id and segment[1] in player.trail[-3:]:
                continue
                
            if self.line_segments_intersect(p1, p2, q1, q2):
                return True
                
        return False
    
    def line_segments_intersect(self, p1, p2, q1, q2):

        def ccw(a, b, c):
            return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])
        
        return ccw(p1, q1, q2) != ccw(p2, q1, q2) and ccw(p1, p2, q1) != ccw(p1, p2, q2)
    
    def draw(self):
        self.screen.fill(self.config.bg_color)
        
        self.draw_grid()
        
        self.screen.blit(self.trail_surface, (0, 0))
        
        for player in self.players:
            if player.alive:
                player.draw(self.screen)
        
        if self.game_over:
            self.draw_game_over()
        
        if self.frame_count <= self.grace_period:
            self.draw_grace_period()
        
        pygame.display.flip()
    
    def draw_grid(self):
        grid_size = self.config.grid_size
        for x in range(0, self.config.screen_width, grid_size):
            pygame.draw.line(self.screen, self.config.grid_color, (x, 0), (x, self.config.screen_height))
        for y in range(0, self.config.screen_height, grid_size):
            pygame.draw.line(self.screen, self.config.grid_color, (0, y), (self.config.screen_width, y))
    
    def draw_grace_period(self):

        text = f"Starting in: {(self.grace_period - self.frame_count) // 10 + 1}"
        text_surf = self.small_font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(self.config.screen_width // 2, 30))
        self.screen.blit(text_surf, text_rect)
    
    def draw_game_over(self):
        overlay = pygame.Surface((self.config.screen_width, self.config.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))
        
        if self.winner:
            text = f"Player {self.winner.id} Wins!"
            color = self.winner.color
        else:
            text = "Game Over - Draw!"
            color = (255, 255, 255)
        
        text_surf = self.font.render(text, True, color)
        text_rect = text_surf.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2 - 30))
        self.screen.blit(text_surf, text_rect)
        
        restart_text = self.small_font.render("Press R to Restart or ESC to Quit", True, (200, 200, 200))
        restart_rect = restart_text.get_rect(center=(self.config.screen_width // 2, self.config.screen_height // 2 + 30))
        self.screen.blit(restart_text, restart_rect)
    
    def reset_game(self):
        self.game_over = False
        self.winner = None
        self.trail_surface.fill((0, 0, 0, 0))  
        self.trail_segments = []  
        self.players = []
        self.create_players()
        self.frame_count = 0  
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.config.fps)