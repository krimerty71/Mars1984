import pygame
import random
import noise
import numpy as np
from settings import MAP_WIDTH, MAP_HEIGHT, CELL_SIZE, MARS_RED, GRAY, BLACK

class Map:
    def __init__(self):
        self.width = MAP_WIDTH
        self.height = MAP_HEIGHT
        self.cell_size = CELL_SIZE
        self.grid = []
        self.resources = []  # Ресурсы на карте
        self.generate_map()
        
    def generate_map(self):
        """Генерирует карту с использованием шума Перлина"""
        self.grid = []
        scale = 10.0
        
        for y in range(self.height):
            row = []
            for x in range(self.width):
                # Генерируем шум для разных типов местности
                elevation = noise.pnoise2(x/scale, y/scale, octaves=6)
                moisture = noise.pnoise2(x/scale + 100, y/scale + 100, octaves=4)
                
                if elevation < -0.3:
                    terrain = 'CRATER'  # Кратер
                elif elevation < 0.1:
                    terrain = 'PLAIN'   # Равнина
                elif elevation < 0.4:
                    terrain = 'HILL'    # Холм
                else:
                    terrain = 'MOUNTAIN' # Гора
                
                # Добавляем случайные ресурсы
                resource = None
                if terrain == 'PLAIN' and random.random() < 0.05:
                    resource = 'IRON'
                elif terrain == 'HILL' and random.random() < 0.08:
                    resource = 'SILICON'
                elif terrain == 'MOUNTAIN' and random.random() < 0.03:
                    resource = 'RARE_METAL'
                
                row.append({
                    'terrain': terrain,
                    'resource': resource,
                    'building': None,
                    'explored': False,
                    'x': x,
                    'y': y
                })
            self.grid.append(row)
    
    def draw(self, screen, camera_x, camera_y):
        """Отрисовка карты"""
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                screen_x = x * self.cell_size - camera_x
                screen_y = y * self.cell_size - camera_y
                
                # Цвет в зависимости от типа местности
                if cell['terrain'] == 'CRATER':
                    color = (100, 50, 50)
                elif cell['terrain'] == 'PLAIN':
                    color = MARS_RED
                elif cell['terrain'] == 'HILL':
                    color = (150, 70, 30)
                elif cell['terrain'] == 'MOUNTAIN':
                    color = (120, 60, 40)
                else:
                    color = GRAY
                
                # Рисуем клетку
                pygame.draw.rect(screen, color, 
                               (screen_x, screen_y, self.cell_size-1, self.cell_size-1))
                
                # Рисуем ресурсы
                if cell['resource'] == 'IRON':
                    pygame.draw.circle(screen, (150, 150, 150), 
                                     (screen_x + 16, screen_y + 16), 5)
                elif cell['resource'] == 'SILICON':
                    pygame.draw.circle(screen, (200, 200, 100), 
                                     (screen_x + 16, screen_y + 16), 5)
                
                # Рисуем постройки
                if cell['building']:
                    if cell['building'] == 'BASE':
                        pygame.draw.rect(screen, GREEN, 
                                       (screen_x + 4, screen_y + 4, 24, 24))
                    elif cell['building'] == 'MINER':
                        pygame.draw.polygon(screen, YELLOW, 
                                          [(screen_x + 16, screen_y + 4),
                                           (screen_x + 28, screen_y + 24),
                                           (screen_x + 4, screen_y + 24)])
