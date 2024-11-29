import pygame
from random import randint

import time

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score = score_font.render(f"score:  {current_time}", False, 'Orange')
    score_rectangle = score.get_rect(center=(675, 100))
    screen.blit(score, score_rectangle)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= randint(11, 19)
            if obstacle_rect.midbottom[1] == 370:
                screen.blit(kunai, obstacle_rect)
            else:
                screen.blit(shuriken, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    else:
        return []

def collisions(player, obstacles, player_mask, obstacle_masks):
    if obstacles:
        for i, obstacle_rect in enumerate(obstacles):
            obstacle_mask = obstacle_masks[i]
            offset = (obstacle_rect.x - player.x, obstacle_rect.y - player.y)
            if player_mask.overlap(obstacle_mask, offset):
                return False
    return True

def character_animation():
    global current_character, current_index, kakashi_frame_rate

    if character_rectangle.bottom < 438:  # Jump animation
        character_image = current_jump
    else:  # Running animation
        if current_character == "Naruto":
            current_index += 0.2  # Naruto's frame rate
        else:  # Kakashi's slower frame rate
            kakashi_frame_rate += 0.18  # Adjust rate for Kakashi
            if kakashi_frame_rate >= len(current_run):
                kakashi_frame_rate = 0
            current_index = kakashi_frame_rate
        
        if current_index >= len(current_run):
            current_index = 0
        
        character_image = current_run[int(current_index)]
    return character_image

pygame.init()
screen = pygame.display.set_mode((1350, 480))
pygame.display.set_caption('shippuden')
clock = pygame.time.Clock()
background_surface = pygame.image.load('graphics/forest_background.png').convert_alpha()
score_font = pygame.font.Font('font/Pixeltype.ttf', 50)
start_time = 0
background_music = pygame.mixer.Sound('audio/music.mp3')
background_music.play(loops=-1)

game_name = score_font.render('shippuden', False, 'Orange')
game_name_rectangle = game_name.get_rect(center=(680, 55))
game_message = score_font.render("press space to start", False, 'Orange')
game_message_rectangle = game_message.get_rect(center=(680, 434))
game_running = False

# Obstacles
kunai = pygame.image.load('graphics/kunai.png').convert_alpha()
kunai = pygame.transform.scale(kunai, (90, 23))
kunai_mask = pygame.mask.from_surface(kunai)

shuriken1 = pygame.image.load('graphics/shuriken1.png').convert_alpha()
shuriken1 = pygame.transform.scale(shuriken1, (45, 45))
shuriken2 = pygame.image.load('graphics/shuriken2.png').convert_alpha()
shuriken2 = pygame.transform.scale(shuriken2, (45, 45))
shuriken_frames = [shuriken1, shuriken2]
shuriken_frame_index = 0
shuriken = shuriken_frames[shuriken_frame_index]

shuriken_mask = pygame.mask.from_surface(shuriken)

obstacle_rect_list = []

# Naruto images
naruto_run = [pygame.image.load(f'graphics/naruto{i}.png').convert_alpha() for i in range(1, 5)]
naruto_run = [pygame.transform.scale(img, (210, 297)) for img in naruto_run]
naruto_jump = pygame.transform.scale(pygame.image.load('graphics/naruto1.png').convert_alpha(), (210, 297))

# Kakashi images
kakashi_run = [pygame.image.load(f'graphics/kakashi{i}.png').convert_alpha() for i in range(1, 7)]
kakashi_run = [pygame.transform.scale(img, (450, 310)) for img in kakashi_run]
kakashi_jump = pygame.transform.scale(pygame.image.load('graphics/kakashi6.png').convert_alpha(), (450, 310))

# Naruto Head for Start Page
naruto_head = pygame.image.load('graphics/naruto_head.png').convert_alpha()
naruto_head = pygame.transform.scale(naruto_head, (290, 295))
naruto_head_rectangle = naruto_head.get_rect(center=(675, 240))

# Initialize Character
current_run = naruto_run
current_jump = naruto_jump
current_character = "Naruto"
current_index = 0
kakashi_frame_rate = 0  # Kakashi's animation frame rate

character_image = current_run[current_index]
if current_character == "Naruto":
    character_rectangle = character_image.get_rect(midbottom=(175, 438))  # Naruto's starting position
elif current_character == "Kakashi":
    character_rectangle = character_image.get_rect(midbottom=(175, 438))  # Same x position as Naruto
character_mask = pygame.mask.from_surface(character_image)
character_gravity = 0

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)
shuriken_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(shuriken_animation_timer, 500)

def move_to_center():
    if character_rectangle.centerx < 675:
        character_rectangle.x += 5  # Move towards the center of the screen
    if character_rectangle.centery < 240:
        character_rectangle.y += 5  # Move towards the vertical center

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_running:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_character == 'Naruto' and character_rectangle.bottom >= 438:
                        character_gravity = -21  # Naruto's jump strength
                    elif current_character == 'Kakashi' and character_rectangle.bottom >= 460:
                        character_gravity = -21  # Kakashi's jump strength
                        
                if event.key == pygame.K_c:  # Toggle character
                    if current_character == "Naruto":
                        current_run = kakashi_run
                        current_jump = kakashi_jump
                        current_character = "Kakashi"
                        # Set Kakashi's starting position to Naruto's current position
                        character_rectangle = kakashi_run[0].get_rect(midbottom=(character_rectangle.midbottom))  # Use Naruto's position
                        character_mask = pygame.mask.from_surface(kakashi_run[0]) # Update the mask
                    else:
                        current_run = naruto_run
                        current_jump = naruto_jump
                        current_character = "Naruto"
                        # Set Naruto's starting position to Kakashi's current position
                        character_rectangle = naruto_run[0].get_rect(midbottom=(character_rectangle.midbottom))  # Use Kakashi's position
                        character_mask = pygame.mask.from_surface(naruto_run[0])  # Update the mask
 # Adjust Y as needed
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_running = True
                start_time = int(pygame.time.get_ticks() / 1000)
        if game_running:
            if event.type == obstacle_timer:
                if randint(0, 2):
                    obstacle_rect_list.append(kunai.get_rect(midbottom=(randint(1450, 1800), 370)))
                else:
                    obstacle_rect_list.append(shuriken.get_rect(midbottom=(randint(1450, 1800), 250)))
            if event.type == shuriken_animation_timer:
                shuriken_frame_index = (shuriken_frame_index + 1) % len(shuriken_frames)

    if game_running:
        screen.blit(background_surface, (0, 0))
        current_time = display_score()

        # Character movement to center
        if character_rectangle.centerx != 675 or character_rectangle.centery != 240:
            move_to_center()

        character_gravity += 1
        character_rectangle.y += character_gravity

        # Prevent character from going below ground
        if current_character == 'Naruto' and character_rectangle.bottom >= 438:
            character_rectangle.bottom = 438
        elif current_character == 'Kakashi' and character_rectangle.bottom >= 460:
            character_rectangle.bottom = 460

        character_image = character_animation()
        screen.blit(character_image, character_rectangle)

        # Obstacle movement
        obstacle_rect_list = obstacle_movement(obstacle_rect_list)

        # Update shuriken animation
        shuriken = shuriken_frames[shuriken_frame_index]

        # Collision
        game_running = collisions(character_rectangle, obstacle_rect_list,
                                  character_mask, [kunai_mask, shuriken_mask])

        if not game_running:
            game_message = score_font.render(f"latest score: {current_time}", False, 'Orange')
            game_message_rectangle = game_message.get_rect(center=(680, 434))
    else:
        screen.fill((23, 23, 40))
        screen.blit(game_name, game_name_rectangle)
        screen.blit(naruto_head, naruto_head_rectangle)
        screen.blit(game_message, game_message_rectangle)
        obstacle_rect_list.clear()
        character_rectangle.midbottom = (175, 438)
        character_gravity = 0

    pygame.display.update()
    clock.tick(60)
