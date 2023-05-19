import pygame, time
from pygame import mixer

#initialize pygame
pygame.init()

#set variables
window_size = (1600, 900)
screen = pygame.display.set_mode(window_size)

lvl = pygame.image.load('Downloads\\PyDash\\level_1.png')
pygame.mixer.music.load('Downloads\\PyDash\\BaseAfterBase.mp3')

pygame.display.set_caption('Test')
mixer.music.set_volume(0.05)
pygame.mixer.music.play()

colliders = []
level = []
placeholder = pygame.draw.rect(screen, (0, 0, 0), (0, 0, 0, 0))

for y in range(lvl.get_height()):
    row = []
    for x in range(lvl.get_width()):
        color = lvl.get_at((x, y))
        if color == (0, 0, 0, 255): #full block
            color = 1
            colliders.append(placeholder)
        elif color == (255, 0, 0, 255): #spike
            color = 2
            colliders.append(placeholder)
        elif color == (127, 0, 0, 255): #small spike
            color = 3
            colliders.append(placeholder)
        elif color == (70, 0, 0, 255): #half-block spike
            color = 4
            colliders.append(placeholder)
        elif color == (0, 0, 255, 255): #half block
            color = 5
            colliders.append(placeholder)
        elif color == (255, 255, 0, 255): #yellow orb
            color = 6
            colliders.append(placeholder)
        elif color == (0, 200, 255, 255):
            color = 7
            colliders.append(placeholder)
        elif color == (150, 150, 0, 255):
            color = 8
            colliders.append(placeholder)
        elif color == (155, 50, 155, 255):
            color = 9
            colliders.append(placeholder)
        elif color == (255, 127, 255, 255):
            color = 10
            colliders.append(placeholder)
        elif color == (255, 255, 255, 255):
            color = 11
            colliders.append(placeholder)
        elif color == (127, 127, 127, 255):
            color = 12
            colliders.append(placeholder)
        else:
            color = 0
        row.append(color)
    level.append(row)

#variables
block_y = -1
block_ofs = 0
player_y = 560
vel_y = 0
jump = 1
phas = 1
timer = 0
screen_y = 0
player_upt = 0
gravity = 1
orb_timer = 0

#use a while loop to  repeat the game until the window is closed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((35, 100, 205))
    floor = pygame.draw.rect(screen, (0, 70, 200), (0, 640 + screen_y, screen.get_width(), 260))

    def draw_level():
        global block_x, block_y
        block_y = -abs(lvl.get_height() - 7)
        block_x = 4
        for rows in level:
            block_y += 1
            block_x = 4
            for id in rows:
                block_x += 1
                if id == 1 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    block = pygame.draw.rect(screen, (0, 0, 0), (((block_x * 80)) - block_ofs, (block_y * 80) + screen_y, 80, 80))
                    del colliders[0]
                    colliders.append(block)
                elif id == 2 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    del colliders[0]
                    tri()
                elif id == 3 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    del colliders[0]
                    small_tri()
                elif id == 4 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    grnd_spike = pygame.draw.rect(screen, (255, 0, 0), (((block_x * 80)) - block_ofs, ((block_y * 80) + 55) + screen_y, 80, 25))
                    del colliders[0]
                    colliders.append(grnd_spike)
                elif id == 5 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    slab = pygame.draw.rect(screen, (0, 0, 0), (((block_x * 80)) - block_ofs, (block_y * 80) + screen_y, 80, 40))
                    del colliders[0]
                    colliders.append(slab)
                elif id == 6 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    y_orb = pygame.draw.rect(screen, (255, 235, 70), ((((block_x * 80)) - block_ofs) + 10, ((block_y * 80) + 10) + screen_y, 60, 60), border_radius=80)
                    del colliders[0]
                    colliders.append(y_orb)
                elif id == 7 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    b_orb = pygame.draw.rect(screen, (0, 255, 255), ((((block_x * 80)) - block_ofs) + 10, ((block_y * 80) + 10) + screen_y, 61, 61), border_radius=80)
                    del colliders[0]
                    colliders.append(b_orb)
                elif id == 8 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    y_pad = pygame.draw.rect(screen, (255, 235, 0), (((block_x * 80)) - block_ofs, ((block_y * 80) + screen_y) + 50, 80, 30))
                    del colliders[0]
                    colliders.append(y_pad)
                elif id == 9 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    p_pad = pygame.draw.rect(screen, (255, 100, 255), (((block_x * 80)) - block_ofs, ((block_y * 80) + screen_y) + 49, 80, 31))
                    del colliders[0]
                    colliders.append(p_pad)
                elif id == 11 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    del colliders[0]
                    usd_tri()
                elif id == 12 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    del colliders[0]
                    usd_small_tri()
                elif id > 0:
                    del colliders[0]
                    colliders.append(placeholder)
                else:
                    pass

    def tri():
        pygame.draw.polygon(screen, (0, 0, 0), (((block_x * 80) - block_ofs, ((block_y + 1) * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), (block_y * 80) + screen_y), (((block_x + 1) * 80) - block_ofs, ((block_y + 1) * 80) + screen_y)))
        spike = pygame.draw.rect(screen, (0, 0, 0), (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 25) + screen_y, 20, 35))
        colliders.append(spike)
    
    def usd_tri():
        pygame.draw.polygon(screen, (0, 0, 0), (((block_x * 80) - block_ofs, (block_y * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), ((block_y + 1) * 80) + screen_y), (((block_x + 1) * 80) - block_ofs, (block_y * 80) + screen_y)))
        spike = pygame.draw.rect(screen, (0, 0, 0), (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 20) + screen_y, 20, 35))
        colliders.append(spike)

    def small_tri():
        pygame.draw.polygon(screen, (0, 0, 0), (((block_x * 80) - block_ofs, ((block_y + 1) * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), ((block_y * 80) + 40) + screen_y), (((block_x + 1) * 80) - block_ofs, ((block_y + 1) * 80) + screen_y)))
        small_spike = pygame.draw.rect(screen, (0, 0, 0), (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 55) + screen_y, 20, 15))
        colliders.append(small_spike)

    def usd_small_tri():
        pygame.draw.polygon(screen, (0, 0, 0), (((block_x * 80) - block_ofs, (block_y * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), ((block_y * 80) + 40) + screen_y), (((block_x + 1) * 80) - block_ofs, (block_y * 80) + screen_y)))
        small_spike = pygame.draw.rect(screen, (0, 0, 0), (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 10) + screen_y, 20, 15))
        colliders.append(small_spike)

    def handle_player():
        global vel_y, player_y, jump, phas, timer, screen_y, gravity, orb_timer
        pygame.draw.rect(screen, (255, 255, 255), (0, (screen.get_height() - 260) + screen_y, screen.get_width(), 3))
        player = pygame.draw.rect(screen, (255, 220, 0), (560, player_y + screen_y, 80, 80))
        player_y += vel_y
        vel_y += gravity
        if player.colliderect(floor) or player_y - screen_y > floor.y:
            jump = 1
            phas = 1
            vel_y = 0
            player_y = (floor.top - 80) - screen_y
        leftclk = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        timer += 1
        orb_timer += 1
        if keys[pygame.K_SPACE] and jump == 1 or leftclk[0] and jump == 1:
            jump = 0
            phas = 0
            if gravity == 1:
                vel_y = -18.75
            else:
                vel_y = 18.75
        if timer > 1:
            jump = 0
        if player.y < 200:
            screen_y += 8
        elif player.y > 580:
            screen_y -= 8
        for hitbox in colliders:
            if player.colliderect(hitbox) and (hitbox.width == 20 or hitbox.height == 25):
                pygame.display.flip()
                pygame.mixer.music.load('Downloads\\PyDash\\explode.mp3')
                pygame.mixer.music.play()
                time.sleep(1)
                pygame.quit()
                exit()
            elif player.colliderect(hitbox) and hitbox.width == 60:
                if keys[pygame.K_SPACE] or leftclk[0]:
                    jump = 0
                    phas = 0
                    if gravity == 1:
                        vel_y = -17.75
                    else:
                        vel_y = 17.75
            elif player.colliderect(hitbox) and hitbox.height == 30:
                if gravity == 1:
                    vel_y = -26.75
                else:
                    vel_y = 26.75
            elif player.colliderect(hitbox) and hitbox.height == 31:
                if gravity == 1:
                    vel_y = -14.75
                else:
                    vel_y = 14.75
            elif player.colliderect(hitbox) and hitbox.width == 61:
                if (keys[pygame.K_SPACE] or leftclk[0]) and (jump == 0 or jump == 1) and orb_timer > 7:
                    orb_timer = 0
                    if gravity == 1:
                        vel_y = -abs(vel_y) + 6
                        gravity = -1
                    else:
                        vel_y = abs(vel_y) - 6
                        gravity = 1
            elif (player.colliderect(hitbox) and player.bottom <= hitbox.top + 15 and gravity == 1) or (player.colliderect(hitbox) and player.top >= hitbox.bottom - 25 and gravity == -1) or player.colliderect(hitbox) and vel_y > 19:
                if vel_y > 10:
                    if gravity == 1:
                        vel_y = 0
                        player_y = (hitbox.top - 80) - screen_y
                    else:
                        vel_y = 0
                        player_y = (hitbox.bottom - screen_y)
                else:
                    timer = 0
                    jump = 1
                    phas = 1
                    vel_y = 0
                    if gravity == 1:
                        player_y = (hitbox.top - 80) - screen_y
                    else:
                        player_y = (hitbox.bottom - screen_y)
            elif player_y + screen_y > hitbox.bottom and player_y + screen_y < hitbox.bottom + 50 and player.left >= hitbox.left and player.left < hitbox.right and hitbox.height == 40 and vel_y > 5:
                timer = 0
                jump = 1
                vel_y = 0
                player_y = (hitbox.top - 80) - screen_y
            elif player.colliderect(hitbox) and (phas == 1 or vel_y < 0):
                pygame.display.flip()
                pygame.mixer.music.load('Downloads\\PyDash\\explode.mp3')
                pygame.mixer.music.play()
                time.sleep(1)
                pygame.quit()
                exit()


    block_ofs += 9.2
    draw_level()
    handle_player()

    time.sleep(0.0071)
    pygame.display.flip()