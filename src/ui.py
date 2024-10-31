import pygame
from utils import scale_img

class HealthBar:
  def __init__(self, max_health, scale=0.2):
    self.max_health = max_health
    self.current_health = max_health

    # Load and scale the health indicator image
    self.health_image = pygame.image.load('assets/icons/health_bar.png').convert_alpha()
    self.health_image = scale_img(self.health_image, scale)

  def draw(self, screen):
    # Calculate the width of the foreground based on current health
    health_ratio = self.current_health / self.max_health
    current_width = int(185 * health_ratio)
    # Draw the background (red rectangle)
    pygame.draw.rect(screen, (255, 0, 0), (30, 20, current_width, 30))
    # Draw the health bar image
    screen.blit(self.health_image, (10, 10))

  def update_health(self, health):
    # Update current health, clamping it between 0 and max_health
    self.current_health = max(0, min(health, self.max_health))

  # Uncomment to add reset functionality
  # def reset(self):
  #   # Reset health to maximum
  #   self.current_health = self.max_health

def draw_equipment(screen, player, scale=0.08):
  # Initialize font for text
  font = pygame.font.SysFont('Futura', 30)

  # Load and scale equipment images
  bullet_image = pygame.image.load('assets/icons/bulletimg1.png')
  bullet_image = scale_img(bullet_image, scale)
  grenade_image = pygame.image.load('assets/icons/grenadeimage.png')
  grenade_image = scale_img(grenade_image, 0.2)

  # Draw equipment icons
  screen.blit(bullet_image, (20, 60))
  screen.blit(grenade_image, (13, 100))

  # Prepare ammo and grenade text
  WHITE = (0, 0, 0)
  ammo_text = f": {player.magazine}/{player.ammo}"
  nade_text = f": x {player.grenades}"

  # Render text surfaces
  ammo_text_surface = font.render(ammo_text, True, WHITE)
  nade_text_surface = font.render(nade_text, True, WHITE)

  # Calculate positions for text, aligned next to equipment images
  text_x = 20 + bullet_image.get_width() + 10  # Right of the bullet image with padding
  ammo_text_y = 70  # Aligned with bullet image y-position
  nade_text_y = 110  # Aligned with grenade image y-position

  # Draw text surfaces on screen
  screen.blit(ammo_text_surface, (text_x, ammo_text_y))
  screen.blit(nade_text_surface, (text_x, nade_text_y))
