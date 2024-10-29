import pygame
import os

def scale_img(img, scale):
  """Scales an image by a specified factor."""
  return pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))

def load_animation(char_type, scale):
  actions = ["Idle", "Walk", "Shoot", "Death", "Hurt"]
  
  # Add additional actions for Main_Char
  if char_type == "Main_char":
    actions += ["Jump", "Throw", "Reload"]

  # Create a dictionary to hold the animations for each action
  animation_list = {action.lower(): [] for action in actions}

  # Load and scale images for each action
  for action in actions:
    action_path = f"assets/{char_type}/{action}"
    if os.path.exists(action_path):  # Check if the directory exists
      for filename in sorted(os.listdir(action_path)):
        if filename.endswith(".png"):  # Ensure it's a PNG file
          img = pygame.image.load(os.path.join(action_path, filename)).convert_alpha()
          img = scale_img(img, scale)
          animation_list[action.lower()].append(img)

  return animation_list

def load_sound():    
  # Initialize Pygame's mixer for audio
  pygame.mixer.init()
  
  # Load background music
  pygame.mixer.music.load('assets/audio/background_music.mp3')
  pygame.mixer.music.set_volume(0.3)  # Set the music volume (0.0 to 1.0)
  pygame.mixer.music.play(-1)  # Play background music on a loop

  # Load sound effects
  shoot_sound = pygame.mixer.Sound('assets/audio/shot.wav')
  jump_sound = pygame.mixer.Sound('assets/audio/jumppp22.ogg')
  explode_sound = pygame.mixer.Sound('assets/audio/grenade.wav')

  # Adjust sound effect volumes
  shoot_sound.set_volume(0.5)
  jump_sound.set_volume(0.5)
  explode_sound.set_volume(0.5)

  return [shoot_sound, jump_sound, explode_sound]

def get_sound(sound_type):
  # Load sound effects
  shoot_sound = pygame.mixer.Sound('assets/audio/shot.wav')
  jump_sound = pygame.mixer.Sound('assets/audio/jumppp22.ogg')
  explode_sound = pygame.mixer.Sound('assets/audio/grenade.wav')
  
  # Adjust sound effect volumes
  shoot_sound.set_volume(0.5)
  jump_sound.set_volume(0.5)
  explode_sound.set_volume(0.5)
  
  # Return the requested sound effect
  if sound_type == "shoot":
    return shoot_sound
  elif sound_type == "jump":
    return jump_sound
  else:
    return explode_sound
