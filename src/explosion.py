import pygame

class Explosion(pygame.sprite.Sprite):
  def __init__(self, x, y, scale=1):
    super().__init__()
    self.animation_list = []
    self.frame_index = 0
    self.update_time = pygame.time.get_ticks()

    # Load explosion images into animation_list
    for i in range(5):  # Assume you have 5 frames for the explosion animation
      img = pygame.image.load(f"assets/Explosion/{i}.png").convert_alpha()
      img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
      self.animation_list.append(img)

    self.image = self.animation_list[self.frame_index]
    self.rect = self.image.get_rect()
    self.rect.center = (x, y)

  def update(self):
    # Control the animation speed (e.g., change frames every 100ms)
    ANIMATION_SPEED = 50  # Speed of the animation in milliseconds
    if pygame.time.get_ticks() - self.update_time > ANIMATION_SPEED:
      self.update_time = pygame.time.get_ticks()
      self.frame_index += 1

      # Check if the animation is finished
      if self.frame_index >= len(self.animation_list):
        self.kill()  # Remove the explosion when animation is done
      else:
        self.image = self.animation_list[self.frame_index]

  def draw(self, screen, screen_scroll):
    # Adjust the grenade's position based on screen scroll for drawing
    self.rect.x += screen_scroll
    screen.blit(self.image, self.rect)
