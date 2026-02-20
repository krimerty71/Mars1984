import pygame
from settings import CELL_SIZE

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.energy = 50
        self.max_energy = 100
        self.resources = {
            'iron': 0,
            'silicon': 0,
            'rare_metal': 0,
            'food': 20
        }
        self.buildings = []
        
    def move(self, dx, dy, game_map):
        """Движение с проверкой коллизий"""
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        # Проверяем границы карты
        if 0 <= new_x < game_map.width * CELL_SIZE:
            self.x = new_x
        if 0 <= new_y < game_map.height * CELL_SIZE:
            self.y = new_y
    
    def gather_resource(self, game_map):
        """Сбор ресурса с текущей клетки"""
        cell_x = int(self.x // CELL_SIZE)
        cell_y = int(self.y // CELL_SIZE)
        
        if 0 <= cell_x < game_map.width and 0 <= cell_y < game_map.height:
            cell = game_map.grid[cell_y][cell_x]
            if cell['resource'] and self.energy > 0:
                # Добавляем ресурс игроку
                if cell['resource'] == 'IRON':
                    self.resources['iron'] += 1
                elif cell['resource'] == 'SILICON':
                    self.resources['silicon'] += 1
                elif cell['resource'] == 'RARE_METAL':
                    self.resources['rare_metal'] += 1
                
                cell['resource'] = None  # Ресурс собран
                self.energy -= 5
                return True
        return False
    
    def build(self, building_type, game_map):
        """Строительство здания"""
        cell_x = int(self.x // CELL_SIZE)
        cell_y = int(self.y // CELL_SIZE)
        
        if 0 <= cell_x < game_map.width and 0 <= cell_y < game_map.height:
            cell = game_map.grid[cell_y][cell_x]
            
            # Проверяем ресурсы для постройки
            if building_type == 'MINER' and self.resources['iron'] >= 3:
                if not cell['building']:
                    cell['building'] = 'MINER'
                    self.resources['iron'] -= 3
                    return True
            elif building_type == 'BASE' and self.resources['iron'] >= 5 and self.resources['silicon'] >= 2:
                if not cell['building']:
                    cell['building'] = 'BASE'
                    self.resources['iron'] -= 5
                    self.resources['silicon'] -= 2
                    return True
        return False
    
    def draw(self, screen, camera_x, camera_y):
        """Отрисовка игрока"""
        screen_x = self.x - camera_x
        screen_y = self.y - camera_y
        
        # Рисуем игрока (круг)
        pygame.draw.circle(screen, (255, 255, 255), 
                         (int(screen_x + 16), int(screen_y + 16)), 12)
        # Глаза
        pygame.draw.circle(screen, (0, 0, 0), 
                         (int(screen_x + 10), int(screen_y + 12)), 3)
        pygame.draw.circle(screen, (0, 0, 0), 
                         (int(screen_x + 22), int(screen_y + 12)), 3)
        
        # Полоска здоровья
        pygame.draw.rect(screen, (255, 0, 0), 
                       (screen_x, screen_y - 10, 32, 5))
        pygame.draw.rect(screen, (0, 255, 0), 
                       (screen_x, screen_y - 10, 32 * (self.health/self.max_health), 5))
