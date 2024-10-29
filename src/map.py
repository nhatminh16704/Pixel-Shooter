import pygame
from button import Button
import csv

pygame.init()

clock = pygame.time.Clock()
FPS = 60

#game windown
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.7)
LOWER_MARGIN = 100
SIDE_MARGIN = 300

screen = pygame.display.set_mode((SCREEN_WIDTH + SIDE_MARGIN, SCREEN_HEIGHT + LOWER_MARGIN))
pygame.display.set_caption('map edit')

#define game variable
ROWS = 17
MAX_COLS = 150
TILE_SIZE = SCREEN_HEIGHT // ROWS
TILE_TYPE = 30
level = 0
current_tile = 0
scroll_left = False
scroll_right = False
scroll = 0
scroll_speed = 3

#load image
bg1_img = pygame.image.load('assets/Background/industry/1.png').convert_alpha()
bg2_img = pygame.image.load('assets/Background/industry/2.png').convert_alpha()
bg3_img = pygame.image.load('assets/Background/industry/3.png').convert_alpha()
bg4_img = pygame.image.load('assets/Background/industry/4.png').convert_alpha()
bg5_img = pygame.image.load('assets/Background/industry/5.png').convert_alpha()

#store in list
img_list = []
for x in range(TILE_TYPE):
    img = pygame.image.load(f'assets/Tile/{x}.png').convert_alpha()
    img = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
    img_list.append(img)

save_img = pygame.image.load('assets/Button/save_btn.png').convert_alpha()
load_img = pygame.image.load('assets/Button/load_btn.png').convert_alpha()

#define color
BLACK = (0,0,0)
PASTEL_BLUE = (178,199,212)
WHITE = (255, 255, 255)
RED = (200, 25, 25)

#define font
font = pygame.font.SysFont('Futura', 24)

#create empty tile list
world_data = []
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

#create ground
for tile in range(0, MAX_COLS):
    world_data[ROWS - 1][tile] = 1

#funtion for outputting text onto the screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,  y))

#drawing background
def draw_bg():
    screen.fill(BLACK)
    num_repeats = int(SCREEN_WIDTH / bg1_img.get_width()) + 1  
    extra_repeats = 2 
    
    for x in range(num_repeats * extra_repeats):  
        bg1_scaled = pygame.transform.scale(bg1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg2_scaled = pygame.transform.scale(bg2_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg3_scaled = pygame.transform.scale(bg3_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg4_scaled = pygame.transform.scale(bg4_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        bg5_scaled = pygame.transform.scale(bg5_img, (SCREEN_WIDTH, SCREEN_HEIGHT))


        screen.blit(bg1_scaled, ((x * SCREEN_WIDTH) - scroll * 0.5, 0))
        screen.blit(bg2_scaled, ((x * SCREEN_WIDTH) - scroll * 0.6, 0))
        screen.blit(bg3_scaled, ((x * SCREEN_WIDTH) - scroll * 0.7, 0))
        screen.blit(bg4_scaled, ((x * SCREEN_WIDTH) - scroll * 0.8, 0))
        screen.blit(bg5_scaled, ((x * SCREEN_WIDTH) - scroll * 0.9, 0))



def draw_grip():
    for c in range(MAX_COLS + 1):
        pygame.draw.line(screen, WHITE, (c * TILE_SIZE - scroll, 0), (c * TILE_SIZE - scroll, SCREEN_HEIGHT))
    for c in range(ROWS + 1):
        pygame.draw.line(screen, WHITE, (0, c * TILE_SIZE), (SCREEN_WIDTH, c * TILE_SIZE))

def draw_world():
    for y, row in enumerate(world_data):
        for x, tile in enumerate(row):
            if tile >= 0:
                screen.blit(img_list[tile], (x * TILE_SIZE - scroll, y * TILE_SIZE))

#create button
save_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT + LOWER_MARGIN - 70, save_img, 1)
load_button = Button(SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT + LOWER_MARGIN - 70, load_img, 1)

#button list
button_list = []
button_col = 0
button_row = 0
for i in range(len(img_list)):
    tile_button = Button(SCREEN_WIDTH + (75 * button_col) + 50, 75 * button_row + 50, img_list[i], 1)
    button_list.append(tile_button)
    button_col += 1
    if button_col == 3:
        button_row += 1
        button_col = 0

def main():
    global level, current_tile, scroll_left, scroll_right, scroll, scroll_speed
    run = True
    while run:
        clock.tick(FPS)
        draw_bg()
        draw_grip()
        draw_world()
        draw_text(f'Level: {level}', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 90)
        draw_text('Press UP or DOWN to change level', font, WHITE, 10, SCREEN_HEIGHT + LOWER_MARGIN - 60)

        #save data
        if save_button.draw(screen):
            with open(f'level{level}_data.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=',')
                for row in world_data:
                    writer.writerow(row)
        if load_button.draw(screen):
            scroll = 0
            with open(f'level{level}_data.csv', newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter= ',')
                for x, row in enumerate(reader):
                    for y, tile in enumerate(row):
                        world_data[x][y] = int(tile)

        # draw tile pannel and tiles
        pygame.draw.rect(screen, PASTEL_BLUE, (SCREEN_WIDTH, 0, SIDE_MARGIN, SCREEN_HEIGHT))

        #choose tile
        button_count = 0
        for button_count, i in enumerate(button_list):
            if i.draw(screen):
                current_tile = button_count

        #hightlight
        pygame.draw.rect(screen, RED, button_list[current_tile].rect, 3)

        #scroll map
        if scroll_left == True and scroll > 0:
            scroll -= 5 * scroll_speed
        if scroll_right == True and scroll < (MAX_COLS * TILE_SIZE) - SCREEN_WIDTH:
            scroll += 5 * scroll_speed
            
        #add new tile 
        #get mouse posion
        pos = pygame.mouse.get_pos()
        x = (pos[0] + scroll) // TILE_SIZE
        y = pos[1] // TILE_SIZE

        #check the coordinates
        if pos[0] < SCREEN_WIDTH and pos[1] < SCREEN_HEIGHT:
            #update tile value
            if pygame.mouse.get_pressed()[0] == 1:
                if world_data[y][x] != current_tile:
                    world_data[y][x] = current_tile
            if pygame.mouse.get_pressed()[2] == 1:
                world_data[y][x] = -1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            #keybroad press
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    level += 1
                if event.key == pygame.K_s and level > 0:
                    level -= 1
                if event.key == pygame.K_a:
                    scroll_left = True
                if event.key == pygame.K_d:
                    scroll_right = True
                if event.key == pygame.K_LSHIFT:
                    scroll_speed = 5
                if event.key == pygame.K_ESCAPE:
                    run = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    scroll_left = False
                if event.key == pygame.K_d:
                    scroll_right = False
                if event.key == pygame.K_LSHIFT:
                    scroll_speed = 1


        pygame.display.update()
    pygame.quit()

if __name__ == "__main__":
    main()