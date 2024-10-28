import pygame
import utils
import const

class Bullet(pygame.sprite.Sprite):
  def __init__(self, x, y, direction, bullet_type, scale=0.05):
    super().__init__()
    bullet_image = pygame.image.load(f"assets/Icons/{bullet_type}.png").convert_alpha()
    self.image = utils.scale_img(bullet_image, scale)
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)
    self.speed = 10 * (1 if direction == 0 else -1)  # Bullet moves in the direction of the player (left or right)

  def update(self, player, enemy_group, tiles_rect):
    # Move the bullet
    self.rect.x += self.speed

    # Check if the bullet has moved off the screen and remove it
    if self.rect.right < 0 or self.rect.left > const.SCREEN_WIDTH:
      self.kill()  # This removes the bullet from all sprite groups

    for tile in tiles_rect:
      if tile[1].colliderect(self.rect):
        self.kill()

    # Check collision with characters
    hit_enemies = pygame.sprite.spritecollide(self, enemy_group, False)
    for enemy in hit_enemies:
      if enemy.alive:
        enemy.health -= 25  # Decrease health
        enemy.update_action('hurt')  # Change action to hurt
        self.kill()  # Remove the bullet from the game
        break  # Exit the loop to prevent multiple hits

    if pygame.sprite.collide_rect(self, player):
      if player.alive:
        player.health -= 25  # Decrease health
        player.update_action('hurt')  # Change action to hurt
        self.kill()  # Remove the bullet from the game
