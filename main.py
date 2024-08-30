import pygame
from os.path import join
from random import randint

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # Important to convert for performance
        self.image = pygame.image.load(join('images', 'player.png')).convert_alpha()
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

        # Move right
        self.player_direction = pygame.math.Vector2()
        self.player_speed = 300

    def update(self):
        keys = pygame.key.get_pressed()
        self.player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        # # Normalized, with zero vector check
        self.player_direction = self.player_direction.normalize() if self.player_direction else self.player_direction
        # Multiply by delta time to even out
        self.rect.center += self.player_direction * self.player_speed * dt

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Shooter')
running = True
clock = pygame.time.Clock()

surface = pygame.Surface((100, 200))
surface.fill('blue')

all_sprites = pygame.sprite.Group()
player = Player(all_sprites)


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

    all_sprites.update()

    # Draw star bg
    display_surface.fill('darkgray')
    for coord in star_coordinates:
        display_surface.blit(star_surface, coord)

    display_surface.blit(meteor_surface, meteor_rect)
    display_surface.blit(laser_surface, laser_rect)

    all_sprites.draw(display_surface)

    pygame.display.update()

pygame.quit()