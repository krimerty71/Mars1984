import pygame
import random
import math

class Enemy:
    def __init__(self, x, y, enemy_type='SCOUT'):
        self.x = x * 32
        self.y = y * 32
        self.type = enemy_type
        self.health = 20
        self.speed = 2
        
        if enemy_type == 'SCOUT':
            self.health = 15
            self.speed = 3
            self.color = (255, 100, 100)
        elif enemy_type == 'WARRIOR':
            self.health = 40
            self.speed = 1.5
            self.color = (200, 50, 50)
        elif enemy_type == 'BOSS':
            self.health = 100
            self.speed = 1
            self.color = (150, 0, 0)
    
    def update(self, player_x, player_y, enemies, game_map):
        """Движение к игроку"""
        dx = player_x - self.x
        dy = player_y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0
    
    def draw(self, screen, camera_x, camera_y):
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Рисуем врага
        pygame.draw.circle(screen, self.color, 
                         (int(screen_x + 16), int(screen_y + 16)), 14)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (int(screen_x + 16), int(screen_y + 16)), 14, 2)
        
        # Глаза
        eye_color = (255, 255, 255) if self.type == 'SCOUT' else (255, 0, 0)
        pygame.draw.circle(screen, eye_color, 
                         (int(screen_x + 10), int(screen_y + 12)), 4)
        pygame.draw.circle(screen, eye_color, 
                         (int(screen_x + 22), int(screen_y + 12)), 4)
