import os
from os import path

img_dir = path.join(path.dirname(__file__), 'Obrazy')
snd_dir = path.join(path.dirname(__file__), 'Sounds')
import pygame
import random
import math

WIDTH = 1000
HEIGHT = 580
FPS = 120

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SCORE = 0
LIVES = 3
SELECTED_SHIP = 0

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(32)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space attack")
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()
difficulty_level = 1
points_for_new_live = 0

def draw_text(surface, text, color, x, y, size):
    font = pygame.font.Font("Fonts/Lato/Lato-Light.ttf", size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def choose_ship():
    global SELECTED_SHIP
    choosing = True
    selected = 0
    ships = [ship1_img, ship2_img, ship3_img]
    ship_descriptions = ["Szybki statek, niska wytrzymałość", "Powolny statek, wysoka wytrzymałość", "Średnia prędkość, za pomocą lewego alta możliwa teleportacja na bliską odległość"]

    while choosing:
        screen.fill(BLACK)
        draw_text(screen, "Wybierz statek", WHITE, WIDTH // 2, HEIGHT // 6, 50)

        for i, ship in enumerate(ships):
            img = pygame.transform.scale(ship, (100, 75))
            img.set_colorkey(BLACK)
            rect = img.get_rect()
            rect.center = (WIDTH // 4 * (i + 1), HEIGHT // 2)
            screen.blit(img, rect)

            if i == selected:
                pygame.draw.rect(screen, GREEN, rect.inflate(20, 20), 3)
                draw_text(screen, ship_descriptions[selected], WHITE, WIDTH // 2, HEIGHT // 2 + 100, 24)


        draw_text(screen, "Użyj strzałek do wyboru, Enter by potwierdzić", WHITE, WIDTH // 2, HEIGHT - 60, 24)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    selected = (selected + 1) % len(ships)
                elif event.key == pygame.K_LEFT:
                    selected = (selected - 1) % len(ships)
                elif event.key == pygame.K_RETURN:
                    SELECTED_SHIP = selected
                    choosing = False

def show_menu():
    menu = True
    selected = 0
    options = ["Start", "Wyjście"]
    while menu:
        screen.fill(BLACK)
        draw_text(screen, "SPACE ATTACK", WHITE, WIDTH // 2, HEIGHT // 4, 64)

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            draw_text(screen, option, color, WIDTH // 2, HEIGHT // 2 + i * 60, 40)

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Start":
                        choose_ship()
                        menu = False

                    elif options[selected] == "Wyjście":
                        pygame.quit()
                        quit()

def show_game_over_screen():
    global SCORE, LIVES, difficulty_level, start_time
    game_over = True
    selected = 0
    options = ["Zagraj ponownie", "Wyjście"]
    while game_over:
        screen.fill(BLACK)
        draw_text(screen, "KONIEC GRY", RED, WIDTH // 2, HEIGHT // 4, 64)
        draw_text(screen, f"Wynik końcowy: {SCORE}", WHITE, WIDTH // 2, HEIGHT // 2 - 40, 36)

        for i, option in enumerate(options):
            color = GREEN if i == selected else WHITE
            draw_text(screen, option, color, WIDTH // 2, HEIGHT // 2 + i * 60, 40)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Zagraj ponownie":
                        game_over = False
                        SCORE = 0
                        LIVES = 3
                        difficulty_level = 1
                        start_time = pygame.time.get_ticks()
                    elif options[selected] == "Wyjście":
                        pygame.quit()
                        quit()

def newmob():
    m = Mob()
    all_sprites.add(m)
    mobs.add(m)

def draw_shield_bar(surface, x, y, procent):
    if procent < 0:
        procent = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 30
    fill = (procent / 100) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surface, BLUE, fill_rect)
    pygame.draw.rect(surface, WHITE, outline_rect, 2)

def drawlives(surface, x, y, img):
    for i in range(LIVES):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surface.blit(img, img_rect)


class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        if SELECTED_SHIP == 0:
            self.image = pygame.transform.scale(ship1_img, (50,38))
            self.shield = 100
        elif SELECTED_SHIP == 1:
            self.image = pygame.transform.scale(ship2_img, (50,38))
            self.shield = 200
        elif SELECTED_SHIP == 2:
            self.image = pygame.transform.scale(ship3_img, (50,38))
            self.shield = 100
            self.teleport_cooldown = 500
            self.last_teleport_time = pygame.time.get_ticks() - self.teleport_cooldown
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centery = HEIGHT / 2
        self.rect.left = 10
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 200
        self.last_shoot = pygame.time.get_ticks()
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.laser_level = 1
        self.max_laser_level = 3
        self.laser_shoot_delays = {
            1: 200,
            2: 150,
            3: 100
        }

    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 3000:
            self.hidden = False
            self.rect.center = (30, HEIGHT / 2)
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        now = pygame.time.get_ticks()
        if SELECTED_SHIP == 0:
            if keystate[pygame.K_LEFT]:
                self.speedx = -6
            if keystate[pygame.K_RIGHT]:
                self.speedx = 6
            if keystate[pygame.K_UP]:
                self.speedy = -10
            if keystate[pygame.K_DOWN]:
                self.speedy = 10
        elif SELECTED_SHIP == 1:
            if keystate[pygame.K_LEFT]:
                self.speedx = -3
            if keystate[pygame.K_RIGHT]:
                self.speedx = 3
            if keystate[pygame.K_UP]:
                self.speedy = -5
            if keystate[pygame.K_DOWN]:
                self.speedy = 5
        elif SELECTED_SHIP == 2:
            if keystate[pygame.K_LEFT]:
                self.speedx = -4.5
            if keystate[pygame.K_RIGHT]:
                self.speedx = 4.5
            if keystate[pygame.K_UP]:
                self.speedy = -7.5
            if keystate[pygame.K_DOWN]:
                self.speedy = 7.5
            teleport_distance = 150
            if now - self.last_teleport_time > self.teleport_cooldown:
                if keystate[pygame.K_LALT]:
                    teleported = False
                    if keystate[pygame.K_UP]:
                        self.rect.centery -= teleport_distance
                        teleported = True
                    if keystate[pygame.K_DOWN]:
                        self.rect.centery += teleport_distance
                        teleported = True
                    if keystate[pygame.K_LEFT]:
                        self.rect.centerx -= teleport_distance
                        teleported = True
                    if keystate[pygame.K_RIGHT]:
                        self.rect.centerx += teleport_distance
                        teleported = True

                    if teleported:
                        self.last_teleport_time = now

        self.shoot_delay = self.laser_shoot_delays.get(self.laser_level, 200)
        if keystate[pygame.K_SPACE]:
            self.shoot()
            shoot_sound.play()
            shoot_sound.set_volume(0.1)

        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            if self.laser_level == 1:
                bullet = Bullet(self.rect.centerx, self.rect.centery)
                all_sprites.add(bullet)
                bullets.add(bullet)
            elif self.laser_level == 2:
                bullet1 = Bullet(self.rect.centerx, self.rect.centery - 10)
                bullet2 = Bullet(self.rect.centerx, self.rect.centery + 10)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)
            elif self.laser_level == 3:
                bullet1 = Bullet(self.rect.centerx, self.rect.centery - 10)
                bullet2 = Bullet(self.rect.centerx, self.rect.centery + 10)
                bullet3 = Bullet(self.rect.centerx, self.rect.centery, angle_offset=-15)
                bullet4 = Bullet(self.rect.centerx, self.rect.centery, angle_offset=15)

                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                all_sprites.add(bullet3)
                all_sprites.add(bullet4)
                bullets.add(bullet1)
                bullets.add(bullet2)
                bullets.add(bullet3)
                bullets.add(bullet4)
    def hide(self):
        self.hidden = True
        self_hide_timer = pygame.time.get_ticks()
        self.laser_level = 1
        self.rect.center = (30, HEIGHT / 2)
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(skala_images )
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .95 / 2)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.rect.x = random.randrange(1040,1100)
        self.speedx = random.randrange(-5,-1)
        self.speedy = random.randrange(-2, 2)
        self.rot = 0
        self.rot_speed = random.randrange(-8,8)
        self.las_update = pygame.time.get_ticks()
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.las_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = random.randrange(1040, 1100)
            self.speedx = random.randrange(-5, -1)
            self.speedy = random.randrange(-2, 2)

class ShooterMob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = pygame.transform.scale(robot_img, (50, 38))
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.y = random.randrange(HEIGHT - self.rect.height)
        self.rect.x = random.randrange(1040, 1100)
        self.speedx = random.randrange(-4, -2)
        self.speedy = random.randrange(-1, 2)
        self.last_update = pygame.time.get_ticks()
        self.last_shoot = pygame.time.get_ticks()
        self.shoot_delay = random.randint(1000, 2500)
        self.rot = 0
        self.rot_speed = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx

        if self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.rect.y = random.randrange(HEIGHT - self.rect.height)
            self.rect.x = random.randrange(1040, 1100)

        now = pygame.time.get_ticks()
        if now - self.last_shoot > self.shoot_delay:
            self.last_shoot = now
            bullet = EnemyBullet(self.rect.left, self.rect.centery)
            all_sprites.add(bullet)
            enemy_bullets.add(bullet)

class EnemyBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (15, 5))
        self.image = pygame.transform.rotate(self.image, 180)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedx = -7

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle_offset=0):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = pygame.transform.scale(bullet_img, (20, 5))
        self.original_image.set_colorkey(BLACK)
        self.image = self.original_image.copy()

        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.centery = y
        self.speed = 10
        self.angle = angle_offset

        self.speedx = self.speed * math.cos(math.radians(self.angle))
        self.speedy = self.speed * math.sin(math.radians(self.angle))

        if self.angle != 0:
            self.image = pygame.transform.rotate(self.original_image, -self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)


    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right < 0 or self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 60

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(powerup_img, (25, 25))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedx = -2

    def update(self):
        self.rect.x += self.speedx
        if self.rect.right < 0:
            self.kill()

background = pygame.image.load(path.join(img_dir, 'Tlo.png')).convert()
background_rect = background.get_rect()
ship1_img = pygame.image.load(path.join(img_dir, 'statek.png')).convert()
ship1_mini_img = pygame.transform.scale(ship1_img, (25, 19))
ship1_mini_img.set_colorkey(BLACK)
ship2_img = pygame.image.load(path.join(img_dir, 'statek2.png')).convert()
ship2_mini_img = pygame.transform.scale(ship2_img, (25, 19))
ship2_mini_img.set_colorkey(BLACK)
ship3_img = pygame.image.load(path.join(img_dir, 'statek3.png')).convert()
ship3_mini_img = pygame.transform.scale(ship3_img, (25, 19))
ship3_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, 'pocisk.png')).convert()
powerup_img = pygame.image.load(path.join(img_dir, 'powerup.png')).convert()
skala_images = []
enemy_bullets = pygame.sprite.Group()
skala_list = ['skala.png', 'skala2.png', 'skala3.png', 'skala4.png']
robot_img = pygame.image.load(path.join(img_dir, 'wrog.png')).convert()
robot_img.set_colorkey(BLACK)
powerups = pygame.sprite.Group()

for img in skala_list:
    skala_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
for i in range(9):
    filename = 'explosion{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (60, 60))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (20, 20))
    explosion_anim['sm'].append(img_sm)

shoot_sound = pygame.mixer.Sound(path.join(snd_dir, '344310__musiclegends__laser-shoot.wav'))
expl_sounds = []
for snd in ['explosion_04.wav', 'explosion-8-bit-01.wav', '8-bit-explosion.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
die_sound = pygame.mixer.Sound(path.join(snd_dir, '560577__theplax__explosion-2.wav'))
pygame.mixer.music.load(path.join(snd_dir, 'arcade-music-loop.wav'))
pygame.mixer.music.set_volume(0.3)
all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = None

for i in range(8):
    newmob()

show_menu()

pygame.mixer.music.play(loops= -1)
running = True
paused = False
while running:
    clock.tick(FPS)
    elapsed_time = (pygame.time.get_ticks() - start_time) // 1000

    if player is None:
        player = PlayerShip()
        all_sprites.add(player)

    if elapsed_time > difficulty_level * 20:
        difficulty_level += 1
        for mob in mobs:
            mob.speedx -= 2
        newmob()
    if difficulty_level >= 3 and len([m for m in mobs if isinstance(m, ShooterMob)]) < 5:
        smob = ShooterMob()
        all_sprites.add(smob)
        mobs.add(smob)

    if not paused:
        all_sprites.update()
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
    for hit in hits:
        random.choice(expl_sounds).play()
        points = 50 - hit.radius
        SCORE += points
        points_for_new_live += points
        if points_for_new_live >= 20000:
            LIVES += 1
            points_for_new_live -= 20000

        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newmob()

        if random.random() < 0.05:
            powerup = PowerUp(hit.rect.center)
            all_sprites.add(powerup)
            powerups.add(powerup)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused

    hits = pygame.sprite.spritecollide(player, mobs, True, pygame.sprite.collide_circle)
    death = None
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newmob()
        if player.shield <= 0:
            die_sound.play()
            death = Explosion(player.rect.center, 'lg')
            all_sprites.add(death)
            player.hide()
            LIVES -= 1
            player.shield = 100


        enemy_hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        for hit in enemy_hits:
            player.shield -= 10
            expl = Explosion(hit.rect.center, 'sm')
            all_sprites.add(expl)
            if player.shield <= 0:
                die_sound.play()
                death = Explosion(player.rect.center, 'lg')
                all_sprites.add(death)
                player.hide()
                LIVES -= 1

                if SELECTED_SHIP == 0 or SELECTED_SHIP == 2:
                    player.shield = 100
                else:
                    player.shield = 200

    powerup_hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in powerup_hits:
        if player.laser_level < player.max_laser_level:
            player.laser_level += 1

    if LIVES == 0 and (death is None or not death.alive()):
        show_game_over_screen()
        SCORE = 0
        LIVES = 3
        player.shield = 100
        for mob in mobs:
            mob.kill()
        for bullet in bullets:
            bullet.kill()
        for i in range(8):
            newmob()
        player.rect.center = (30, HEIGHT / 2)
        player.hidden = False
        all_sprites.add(player)

    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, "Wynik", WHITE, WIDTH / 15, 10, 30)
    draw_text(screen, str(SCORE), WHITE, WIDTH / 15, 50, 30)
    if SELECTED_SHIP == 0 or SELECTED_SHIP == 2:
        draw_shield_bar(screen, WIDTH - 110, 5, player.shield)
    else:
        draw_shield_bar(screen, WIDTH - 210, 5, player.shield)
    if SELECTED_SHIP == 0:
        drawlives(screen, WIDTH / 2, 5, ship1_mini_img)
    elif SELECTED_SHIP == 1:
        drawlives(screen, WIDTH / 2, 5, ship2_mini_img)
    elif SELECTED_SHIP == 2:
        drawlives(screen, WIDTH / 2, 5, ship3_mini_img)
    draw_text(screen, "Poziom: ", WHITE, 70, HEIGHT - 50, 30)
    draw_text(screen, str(difficulty_level), WHITE, 130, HEIGHT - 50, 30)

    if paused:
        draw_text(screen, "PAUZA", RED, WIDTH // 2, HEIGHT // 2, 64)

    pygame.display.flip()

pygame.quit()