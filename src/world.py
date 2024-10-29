import csv
import os
import pygame
from const import MAX_COLS, ROWS, TILE_SIZE
from player import Player
from ui import HealthBar

# Function to load the level data from a CSV file
def load_level(level):
  world_data = [[-1 for _ in range(MAX_COLS)] for _ in range(ROWS)]
  
  # Load the level data from the CSV file
  file_path = os.path.join(f'level{level}_data.csv')
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

class World:
  def __init__(self, world_data):
    self.world_data = world_data
    self.tile_rects = []  # Store the rectangles of tiles for collision detection
    self.items = []       # Store all items (health, ammo, grenade, etc.)
    self.player = None
    self.tile_list = []   # List to store tile images

    # Load and scale tile images
    for x in range(30):  # Assuming 30 unique tile types
      img = pygame.image.load(f'assets/Tile/{x}.png')
      img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
      self.tile_list.append(img)

  def process_data(self, enemy_group):
    """Processes level data, initializes player, enemies, and items."""
    self.tile_rects = []  # Clear any existing tile data

    for y, row in enumerate(self.world_data):
      for x, tile in enumerate(row):
        # Player spawn tile (index 25)
        if tile == 25:
          self.player = Player('Main_char', x * TILE_SIZE, y * TILE_SIZE, 1, 20, 5)
          self.health_bar = HealthBar(self.player.health)

        # Enemy spawn tile (index 26)
        elif tile == 26:
          enemy = Player('Enemy', x * TILE_SIZE, y * TILE_SIZE, 1.8, 30, 5)
          enemy_group.add(enemy)

        # Health box tile (index 29)
        elif tile == 29:
          img = self.tile_list[tile]
          img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
          self.items.append(('health', img, img_rect))

        # Ammo box tile (index 28)
        elif tile == 27:
          img = self.tile_list[tile]
          img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
          self.items.append(('ammo', img, img_rect))

        # Grenade box tile (index 27)
        elif tile == 28:
          img = self.tile_list[tile]
          img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
          self.items.append(('grenade', img, img_rect))

        # Exit tile (index 23)
        elif tile == 23:
          img = self.tile_list[tile]
          img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
          self.items.append(('exit', img, img_rect))
        
        elif tile == 22 or tile == 13 or tile == 15 or tile == 20 or tile == 21:
          img = self.tile_list[tile]
          img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
          self.items.append(('lol', img, img_rect))
        # General tile drawing for collision
        elif tile >= 0 and tile < len(self.tile_list) - 1:
          img = self.tile_list[tile]
          img_rect = img.get_rect(topleft=(x * TILE_SIZE, y * TILE_SIZE))
          self.tile_rects.append((img, img_rect))

    return self.player, self.health_bar

  def draw(self, screen, screen_scroll):
    """Draws tiles and items, adjusted by screen scroll for a dynamic camera."""
    # Draw each tile and adjust position based on screen scroll
    for tile in self.tile_rects:
      tile[1].x += screen_scroll  # Adjust the rect's x-coordinate
      screen.blit(tile[0], tile[1])

    # Draw each item with screen scroll adjustment
    for item in self.items:
      item[2].x += screen_scroll  # Adjust item position
      screen.blit(item[1], item[2])
