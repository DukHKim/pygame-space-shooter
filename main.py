import pygame
from os.path import join
from random import randint

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

surface = pygame.Surface((100, 200))
surface.fill('blue')

# Important to convert for performance
player_surface = pygame.image.load(join('images', 'player.png')).convert_alpha()
player_rect = player_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
# Move right
player_direction = pygame.math.Vector2()
player_speed = 300

star_surface = pygame.image.load(join('images', 'star.png')).convert_alpha()
star_coordinates = [(randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)) for _ in range(50)]

meteor_surface = pygame.image.load(join('images', 'meteor.png')).convert_alpha()
meteor_rect = meteor_surface.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

laser_surface = pygame.image.load(join('images', 'laser.png')).convert_alpha()
laser_rect = laser_surface.get_frect(bottomleft = (20, WINDOW_HEIGHT - 20))

while running:
    # Divide to get seconds
    dt = clock.tick() / 1000
    # Event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos
    keys = pygame.key.get_pressed()

    recent_keys = pygame.key.get_just_pressed()
    if recent_keys[pygame.K_SPACE]:
        print('Fire Laser')
    
    player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # Normalized, with zero vector check
    player_direction = player_direction.normalize() if player_direction else player_direction
    player_rect.center += player_direction * player_speed * dt

    # # Player Movement bouncing
    # if player_rect.right >= WINDOW_WIDTH or player_rect.left < 0:
    #     player_direction.x *= -1

    # if player_rect.bottom >= WINDOW_HEIGHT or player_rect.top < 0:
    #     player_direction.y *= -1


    # Draw star bg
    display_surface.fill('darkgray')
    for coord in star_coordinates:
        display_surface.blit(star_surface, coord)
    # Multiply by delta time to even out

    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(laser_surface, laser_rect)
    display_surface.blit(player_surface, player_rect)

    pygame.display.update()

pygame.quit()