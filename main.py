import pygame
import sys
import random
from settings import *
from modules.map import Map
from modules.player import Player
from modules.enemy import Enemy

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Инициализация игры
        self.game_map = Map()
        self.player = Player(10 * CELL_SIZE, 10 * CELL_SIZE)
        self.camera_x = 0
        self.camera_y = 0
        self.enemies = []
        
        # Шрифты
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
        # Таймеры
        self.enemy_spawn_timer = 0
        self.damage_timer = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.gather_resource(self.game_map)
                elif event.key == pygame.K_b:
                    self.player.build('MINER', self.game_map)
                elif event.key == pygame.K_v:
                    self.player.build('BASE', self.game_map)
        
        # Непрерывное движение
        keys = pygame.key.get_pressed()
        dx = keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        dy = keys[pygame.K_DOWN] - keys[pygame.K_UP]
        if dx != 0 or dy != 0:
            self.player.move(dx, dy, self.game_map)
    
    def update_camera(self):
        # Камера следует за игроком
        self.camera_x = self.player.x - WINDOW_WIDTH // 2
        self.camera_y = self.player.y - WINDOW_HEIGHT // 2
        
        # Ограничиваем камеру
        self.camera_x = max(0, min(self.camera_x, 
                                  self.game_map.width * CELL_SIZE - WINDOW_WIDTH))
        self.camera_y = max(0, min(self.camera_y, 
                                  self.game_map.height * CELL_SIZE - WINDOW_HEIGHT))
    
    def spawn_enemy(self):
        """Спавн врагов на краю карты"""
        if random.random() < 0.02:  # 2% шанс каждый кадр
            side = random.randint(0, 3)
            if side == 0:  # Сверху
                x = random.randint(0, self.game_map.width - 1)
                y = 0
            elif side == 1:  # Справа
                x = self.game_map.width - 1
                y = random.randint(0, self.game_map.height - 1)
            elif side == 2:  # Снизу
                x = random.randint(0, self.game_map.width - 1)
                y = self.game_map.height - 1
            else:  # Слева
                x = 0
                y = random.randint(0, self.game_map.height - 1)
            
            # Выбираем тип врага
            enemy_type = random.choices(['SCOUT', 'WARRIOR', 'BOSS'], 
                                      weights=[70, 25, 5])[0]
            self.enemies.append(Enemy(x, y, enemy_type))
    
    def update(self):
        self.spawn_enemy()
        
        # Обновляем врагов
        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y, self.enemies, self.game_map)
            
            # Проверка на попадание в игрока
            if (abs(enemy.x - self.player.x) < 20 and 
                abs(enemy.y - self.player.y) < 20):
                if pygame.time.get_ticks() - self.damage_timer > 1000:
                    self.player.health -= 10
                    self.damage_timer = pygame.time.get_ticks()
            
            # Проверка на смерть врага
            if enemy.health <= 0:
                self.enemies.remove(enemy)
        
        self.update_camera()
    
    def draw_ui(self):
        """Рисуем интерфейс"""
        # Ресурсы
        resources_text = f"Iron: {self.player.resources['iron']}  Silicon: {self.player.resources['silicon']}  Rare: {self.player.resources['rare_metal']}"
        res_surface = self.small_font.render(resources_text, True, WHITE)
        self.screen.blit(res_surface, (10, 10))
        
        # Здоровье
        health_text = f"Health: {self.player.health}/{self.player.max_health}"
        health_surface = self.small_font.render(health_text, True, WHITE)
        self.screen.blit(health_surface, (10, 40))
        
        # Энергия
        energy_text = f"Energy: {self.player.energy}/{self.player.max_energy}"
        energy_surface = self.small_font.render(energy_text, True, WHITE)
        self.screen.blit(energy_surface, (10, 70))
        
        # Количество врагов
        enemy_text = f"Enemies: {len(self.enemies)}"
        enemy_surface = self.small_font.render(enemy_text, True, RED)
        self.screen.blit(enemy_surface, (WINDOW_WIDTH - 150, 10))
        
        # Подсказки
        hint1 = "[SPACE] Собрать ресурс"
        hint2 = "[B] Построить шахту"
        hint3 = "[V] Построить базу"
        self.screen.blit(self.small_font.render(hint1, True, GRAY), (10, WINDOW_HEIGHT - 60))
        self.screen.blit(self.small_font.render(hint2, True, GRAY), (10, WINDOW_HEIGHT - 40))
        self.screen.blit(self.small_font.render(hint3, True, GRAY), (10, WINDOW_HEIGHT - 20))
    
    def draw(self):
        # Небо (фон)
        self.screen.fill(MARS_SKY)
        
        # Рисуем карту
        self.game_map.draw(self.screen, self.camera_x, self.camera_y)
        
        # Рисуем врагов
        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)
        
        # Рисуем игрока
        self.player.draw(self.screen, self.camera_x, self.camera_y)
        
        # Рисуем интерфейс
        self.draw_ui()
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
