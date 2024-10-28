import csv
import os
import pygame
from const import MAX_COLS, ROWS, TILE_SIZE, level_comple, MAX_LEVEL
from player import Player
from ui import HealthBar

def reset_level():
    from main import enemy_group, bullet_group, grenade_group, explosion_group
    enemy_group.empty()
    bullet_group.empty()
    grenade_group.empty()
    explosion_group.empty()
    data = []
    for row in range(ROWS):
        r = [-1] * MAX_COLS
        data.append(r)
    return data
    
# Function to load the level data from a CSV file
def load_level(level):
    world_data = []
    world_data = [[-1 for _ in range(MAX_COLS)] for _ in range(ROWS)]
    
    # Load the level data from the CSV file
    file_path = os.path.join( f'level{level}_data.csv')  # Adjust the path as needed
    if os.path.exists(file_path):
        with open(file_path, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for y, row in enumerate(reader):
                for x, tile in enumerate(row):
                    world_data[y][x] = int(tile)
        print(f"Level {level} loaded successfully.")
    else:
        print(f"Level {level} data file not found at {file_path}.")
        
    return world_data

def check_comple(level, player, health_bar, enemy_group):
    global level_comple  # Nếu `level_comple` là một cờ toàn cục

    if player.reached_exit:
        level += 1
        world_data = reset_level()
        
        if level <= MAX_LEVEL:
            # Tải dữ liệu màn mới từ tệp CSV
            file_path = os.path.join(f'level{level}_data.csv')
            if os.path.exists(file_path):
                with open(file_path, newline='') as csvfile:
                    reader = csv.reader(csvfile, delimiter=',')
                    for y, row in enumerate(reader):
                        for x, tile in enumerate(row):
                            world_data[y][x] = int(tile)
                
                # Xử lý và cập nhật dữ liệu màn mới
                world = World(world_data)
                player, health_bar = world.process_data(enemy_group)
                
                # Đặt lại `reached_exit` để không chuyển màn lại khi player đang ở màn mới
                player.reached_exit = False
                print(f"Level {level} loaded successfully.")
                
                return player, health_bar, level
            else:
                print(f"Level {level} data file not found.")
                # Kết thúc trò chơi nếu không có tệp CSV cho màn mới
                player.alive = False  
    return player, health_bar, level




class World:
    def __init__(self, world_data):
        self.world_data = world_data
        self.tile_rects = []  # Store the rectangles of tiles for collision detection
        self.items = []       # Single list for all items (health, ammo, grenade)
        self.player = None
        # Initialize an empty list to store tile images
        self.tile_list = []

        # Loop through the range of TILE_TYPES (number of different tiles)
        for x in range(30):
            # Load the image from the specified path using the current index 'x'
            img = pygame.image.load(f'assets/Tile3/{x}.png')

            # Scale the image to match the desired tile size
            img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))

            # Append the scaled image to the list
            self.tile_list.append(img)

    def process_data(self, enemy_group):
      
        self.tile_rects = []  # Clear any existing tile data
        # Loop through each row and column in the world data
        for y, row in enumerate(self.world_data):
            for x, tile in enumerate(row):
                # If the tile is 25, create the player
                if tile == 25:
                    self.player = Player('Main_char', x * TILE_SIZE, y * TILE_SIZE, 1, 20, 5)
                    self.health_bar = HealthBar(self.player.health)
                
                # If the tile is 26, create an enemy and add to the enemy group
                elif tile == 26:
                    enemy = Player('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1.8, 30, 5)
                    enemy_group.add(enemy)
                # Skip empty tiles (assuming TILE_TYPES - 1 is the empty tile)
                # Health box at tile 29
                elif tile == 29:
                    img = self.tile_list[tile]
                    img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                    self.items.append(('health', img, img_rect))  # Add as 'health' type

                # Ammo box at tile 28
                elif tile == 27:
                    img = self.tile_list[tile]
                    img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                    self.items.append(('ammo', img, img_rect))  # Add as 'ammo' type

                # Grenade box at tile 29
                elif tile == 28:
                    img = self.tile_list[tile]
                    img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                    self.items.append(('grenade', img, img_rect))  # Add as 'grenade' type
                elif tile >= 23 and tile <= 24:  # water tile
                    img = self.tile_list[tile]
                    img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                    self.items.append(('water', img, img_rect))  # Add exit as 'water' type
                elif tile == 22:
                    img = self.tile_list[tile]
                    img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                    self.items.append(('exit', img, img_rect))
                elif tile >= 12 and tile <= 21:
                    img = self.tile_list[tile]
                    img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
                    self.items.append(('decaration', img, img_rect))
                elif tile >= 0 and tile < len(self.tile_list) - 1:
                    # Calculate the position where the tile should be drawn
                    img = self.tile_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x * TILE_SIZE
                    img_rect.y = y * TILE_SIZE

                    # Add the tile's rect to the list for collision handling
                    self.tile_rects.append((img, img_rect))

        return self.player, self.health_bar
    def draw(self, screen, screen_scroll):
        for tile in self.tile_rects:
            tile[1][0] += screen_scroll
            screen.blit(tile[0], tile[1])
        
                # Draw items with scrolling
        for item in self.items:
            item[2][0] += screen_scroll  # Adjust position by scroll
            screen.blit(item[1], item[2])  # Draw the item's image