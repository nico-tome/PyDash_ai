'''
Engine from https://github.com/AcruxGD/PyDash.git by AcruxGD
Modified in 10/02/2024 by Tomyo_ (Nicolas Tome): https://github.com/nico-tome
Brain idea from CodeBh: https://youtu.be/MTcXW94V838?si=N8MnTdbSw0VEYCZi
'''
import pandas as pd
import pygame, time, random, copy
from pygame import mixer

#initialize pygame
pygame.init()

#set window
window_size = (1600, 900)
screen = pygame.display.set_mode(window_size)

lvl = pygame.image.load('PyDash/level_2.png')
pygame.mixer.music.load('PyDash/explode.mp3')

pygame.display.set_caption('Test')
mixer.music.set_volume(0.05)
pygame.mixer.music.play()

#color
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLACK2 = (1, 0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GREY = (54, 54, 54, 255)

colliders = []
level = []
placeholder = pygame.draw.rect(screen, BLACK, (0, 0, 0, 0))

#read the level
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
        elif color == (0, 255, 0, 255):
            color = 13
            colliders.append(placeholder)
        else:
            color = 0
        row.append(color)
    level.append(row)


#game variables
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
best_score = 0
game_paused = False

#visuale variable
draw_line = True
draw_sensore = True
draw_neurone = True
slow_time = False
draw_debugg = True

def get_generation():
    df = pd.read_csv('PyDash/best.csv', sep=";")
    return(len(df['generation']))

def save_in_best(best_brain):
    df = pd.read_csv('PyDash/best.csv', sep=";")
    
    data = {'generation': [], 'brain': []}
    data['generation'] = list(df['generation'])
    data['brain'] = list(df['brain'])
    
    data['brain'].append(best_brain)
    data['generation'].append(len(data['brain']) - 1)
    
    new_df = pd.DataFrame(data)
    new_df.to_csv('PyDash/best.csv', index=False, sep=";")

def creat_brain(iteration):
    all_brains = []
    for i in range(iteration):
        new_brain = [[] for _ in range(random.randint(2,4))]
        
        for i in range(len(new_brain)):
            for j in range(random.randint(2,4)):
                new_brain[i].append([random.randint(600, screen.get_width() - 200), random.randint(-100, 300), random.randint(1,6)])
        
        all_brains.append(new_brain)
    
    return all_brains

def save_brain(data):
    all_data = {}
    all_agents = []
    all_id = []
    id = 0

    for agent in data:
        all_agents.append(agent)
        all_id.append(id)
        id += 1
    
    all_data['id'] = all_id
    all_data['brain'] = all_agents

    df = pd.DataFrame(all_data)
    df.to_csv('PyDash/agents.csv', index=False, sep=";")

def load_brain(id):
    
    df = pd.read_csv('PyDash/agents.csv', sep=';')
    row = df[df['id'] == id]
    if len(row) > 0:
        brain_list = eval(row['brain'].iloc[0])
        return brain_list
    else:
        print(id)
        print("L'ID spécifié n'existe pas dans le fichier CSV.")
        return None

def creat_brain_state():
    empty_brain = [[] for _ in range(len(brain))]

    for i in range(len(brain)):
        for j in range(len(brain[i])):
            empty_brain[i].append([False])

    return empty_brain

def generate_new_agents(brain):
    #print("brain", brain)
    all_brain = []
    all_brain.append(brain)
    for i in range(49):
        new_brain = copy.deepcopy(brain)
        neurone = random.randint(0, len(new_brain)-1)
        if len(new_brain[neurone]) > 1:
            sensor = random.randint(0, len(new_brain[neurone])-1)
        else:
            sensor = 0
        choice = []
        if len(new_brain) < 5:
            choice.append(1)
        if len(new_brain) > 1:
            choice.append(2)
        if len(new_brain[neurone]) > 1:
            choice.append(4)
        if len(new_brain[neurone]) < 5:
            choice.append(5)
        change = random.choice(choice)
        if change == 1: #ajouter un neurone
            new_sensor = []
            for _ in range(random.randint(1,5)):
                new_sensor.append([random.randint(600, screen.get_width() - 200), random.randint(-100, 300), random.randint(1,6)])
            new_brain.append(new_sensor)
        elif change == 2: #suprimmer un neurone
            del new_brain[random.randint(0, len(new_brain) - 1)]
        elif change == 3: #changer un sensor
            new_brain[neurone][sensor] = [random.randint(600, screen.get_width() - 200), random.randint(-100, 300), random.randint(1,6)]
        elif change == 4: #suprimmer un sensor
            del new_brain[neurone][sensor]
        elif change == 5: #ajouter un sensor
            new_brain[neurone][sensor].append([random.randint(600, screen.get_width() - 200), random.randint(-100, 300), random.randint(1,6)])
        all_brain.append(new_brain)
    return all_brain


def reset_player():
    global player_y, vel_y, screen_y, gravity, block_ofs, score, id, brain, brain_state, best_score, by_id, generation
    #print(id, score, best_score, generation)
    player_y = 560
    vel_y = 0
    screen_y = 0
    gravity = 1
    block_ofs = 0
    if score > best_score:
        best_score = score
        by_id = id
    score = 0
    if id == 49:
        #print(by_id)
        save_in_best(load_brain(by_id))
        save_brain(generate_new_agents(load_brain(by_id)))
        generation += 1
        id = 0
        best_score = 0
        brain = load_brain(id)
        brain_state = creat_brain_state()
    else:
        id += 1
        brain = load_brain(id)
        brain_state = creat_brain_state()


def get_neurone_pos(neurone):
    sum_x = sum(point[0] for point in neurone)
    sum_y = sum(point[1] for point in neurone)
    number_of_point = len(neurone)
    moy_x = sum_x / number_of_point
    moy_y = sum_y / number_of_point
    return (int(moy_x), int(moy_y) + int(player_y + screen_y))

def check_sensor(x, y, need, rid, id):
    if y > 900:
        y = 900
    try:
        color_detector = screen.get_at((x, y))
    except Exception as e:
        color_detector = "none"
    if need == 1:
        brain_state[rid][id] = color_detector == BLACK
    elif need == 2:
        brain_state[rid][id] = color_detector == GREY
    elif need == 3:
        brain_state[rid][id] = color_detector != BLACK
    elif need == 4:
        brain_state[rid][id] = color_detector != GREY
    elif need == 5:
        brain_state[rid][id] = color_detector != BLACK and color_detector != GREY
    elif need == 6:
        brain_state[rid][id] = color_detector == BLACK or color_detector == GREY

def draw_brain():
    rid = 0
    for neurones in brain:

        neurone = list(neurones)

        if len(neurone) > 1:
            neurone_pos = get_neurone_pos(neurone)

        l_id = 0
        for info in neurone:
            check_sensor(info[0], int(player_y + screen_y)+info[1], info[2], rid, l_id)

            if draw_line:
                if brain_state[rid][l_id]: #check the color of the line
                    color = GREEN
                else:
                    color = RED

                if len(neurone) == 1: #draw the linde
                    pygame.draw.line(screen, color, (info[0], int(player_y + screen_y)+info[1]), (600, (player_y + screen_y) + 40), 3)
                else:
                    pygame.draw.line(screen, color, (info[0], int(player_y + screen_y)+info[1]), neurone_pos, 3)

            if draw_sensore:
                if info[2] == 1: #draw the sensor
                    pygame.draw.circle(screen, BLACK2, (info[0], int(player_y + screen_y) + info[1]), 16)
                elif info[2] == 2:
                    pygame.draw.circle(screen, GREY, (info[0], int(player_y + screen_y) + info[1]), 16)
                elif info[2] == 3:
                    pygame.draw.circle(screen, BLACK2, (info[0], int(player_y + screen_y) + info[1]), 16)
                    pygame.draw.circle(screen, WHITE, (info[0], int(player_y + screen_y) + info[1]), 10)
                elif info[2] == 4:
                    pygame.draw.circle(screen, GREY, (info[0], int(player_y + screen_y) + info[1]), 16)
                    pygame.draw.circle(screen, WHITE, (info[0], int(player_y + screen_y) + info[1]), 10)
                elif info[2] == 5:
                    pygame.draw.circle(screen, WHITE, (info[0], int(player_y + screen_y) + info[1]), 16)
                elif info[2] == 6:
                    pygame.draw.circle(screen, WHITE, (info[0], int(player_y + screen_y) + info[1]), 16)
                    pygame.draw.circle(screen, BLACK2, (info[0], int(player_y + screen_y) + info[1]), 10)

            l_id += 1

        if draw_neurone and len(neurone) > 1:

            if False in brain_state[rid]:
                neurone_color = RED
            else:
                neurone_color = GREEN

            pygame.draw.circle(screen, neurone_color, neurone_pos, 16)
        
        rid += 1

''' use this to restart process'''

#(generate_new_agents([[[600, 100, 3], [800, 50, 2]], [[900, 40, 1], [640, -100, 3]], [[700, 50, 2]], [[800, 10, 1]]]))
#save = creat_brain(100)
#save_brain(brain)

''''''

#brain variable
generation = get_generation()
score = 0
by_id = 0
brain = load_brain(0)
brain_state = creat_brain_state()
id = 0

save_in_best(load_brain(by_id))
#use a while loop to  repeat the game until the window is closed
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]: #stop the game
        pygame.quit()
        exit()

    if keys[pygame.K_a]: #draw all brain
        draw_line = True
        draw_sensore = True
        draw_neurone = True

    if keys[pygame.K_z]: #draw sensors
        draw_sensore = True
        draw_line = False
        draw_neurone = False
    
    if keys[pygame.K_e]: #draw neurone
        draw_neurone = True
        draw_line = False
        draw_sensore = False

    if keys[pygame.K_r]: #draw nothing
        draw_neurone = False
        draw_line = False
        draw_sensore = False

    if keys[pygame.K_q]: #slow time
        slow_time = slow_time == False
        time.sleep(0.1)

    if keys[pygame.K_d]: #draw debugg
        draw_debugg = True
    
    if keys[pygame.K_f]: #hide debugg
        draw_debugg = False

    if keys[pygame.K_p]:
        game_paused = game_paused == False
        time.sleep(0.3)

    screen.fill((35, 100, 205))
    floor = pygame.draw.rect(screen, (0, 70, 200), (0, 640 + screen_y, screen.get_width(), 260))

    def need_to_jump_check():
        rid = 0
        for neurone in brain:
            if False not in brain_state[rid]:
                return True
            rid += 1
        return 

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
                elif id == 13 and (block_x * 80) - block_ofs < 1600 and (block_x * 80) - block_ofs > -80:
                    del colliders[0]
                    left_tri()
                elif id > 0:
                    del colliders[0]
                    colliders.append(placeholder)
                else:
                    pass

    def tri(): #basic spike
        pygame.draw.polygon(screen, GREY, (((block_x * 80) - block_ofs, ((block_y + 1) * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), (block_y * 80) + screen_y), (((block_x + 1) * 80) - block_ofs, ((block_y + 1) * 80) + screen_y)))
        spike = pygame.draw.rect(screen, GREY, (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 25) + screen_y, 20, 35))
        colliders.append(spike)
    
    def left_tri(): # Spike oriented towards left
        pygame.draw.polygon(screen, GREY, (((block_x * 80) - block_ofs, ((block_y + 1) * 80)-40 + screen_y), (((block_x + 1) * 80) - block_ofs, (block_y * 80) + screen_y), (((block_x + 1) * 80) - block_ofs, ((block_y + 1) * 80) + screen_y)))
        spike = pygame.draw.rect(screen, GREY, (((block_x * 80) - block_ofs + 40), ((block_y * 80) + 25) + screen_y, 20, 35))
        colliders.append(spike)

    def usd_tri(): #spike down
        pygame.draw.polygon(screen, GREY, (((block_x * 80) - block_ofs, (block_y * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), ((block_y + 1) * 80) + screen_y), (((block_x + 1) * 80) - block_ofs, (block_y * 80) + screen_y)))
        spike = pygame.draw.rect(screen, GREY, (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 20) + screen_y, 20, 35))
        colliders.append(spike)

    def small_tri(): #small spike
        pygame.draw.polygon(screen, GREY, (((block_x * 80) - block_ofs, ((block_y + 1) * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), ((block_y * 80) + 40) + screen_y), (((block_x + 1) * 80) - block_ofs, ((block_y + 1) * 80) + screen_y)))
        small_spike = pygame.draw.rect(screen, GREY, (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 55) + screen_y, 20, 15))
        colliders.append(small_spike)

    def usd_small_tri(): #small spike down
        pygame.draw.polygon(screen, GREY, (((block_x * 80) - block_ofs, (block_y * 80) + screen_y), ((((block_x * 80) - block_ofs) + 40), ((block_y * 80) + 40) + screen_y), (((block_x + 1) * 80) - block_ofs, (block_y * 80) + screen_y)))
        small_spike = pygame.draw.rect(screen, GREY, (((block_x * 80) - block_ofs) + 30, ((block_y * 80) + 10) + screen_y, 20, 15))
        colliders.append(small_spike)

    def handle_player(): #draw and check collision with the player
        global vel_y, player_y, jump, phas, timer, screen_y, gravity, orb_timer
        pygame.draw.rect(screen, (255, 255, 255), (0, (screen.get_height() - 260) + screen_y, screen.get_width(), 3))
        player = pygame.draw.rect(screen, (255, 220, 0), (560, player_y + screen_y, 80, 80))
        if not game_paused:
            player_y += vel_y
            vel_y += gravity
            if player.colliderect(floor) or player_y - screen_y > floor.y:
                jump = 1
                phas = 1
                vel_y = 0
                player_y = (floor.top - 80) - screen_y
            leftclk = pygame.mouse.get_pressed()
            
            jumping = keys[pygame.K_SPACE] or leftclk[0] or need_to_jump_check()
            timer += 1
            orb_timer += 1
            if jumping and jump == 1 or jumping and jump == 1:
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
                    print("dead")
                    reset_player()
                elif player.colliderect(hitbox) and hitbox.width == 60:
                    if jumping:
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
                    if (jumping) and (jump == 0 or jump == 1) and orb_timer > 7:
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
                    print("dead")
                    reset_player()


    if not game_paused:
        block_ofs += 9.2


    draw_level()
    handle_player()

    draw_brain()


    if not game_paused:
        score += 1


    if draw_debugg: 
        font = pygame.font.Font(None, 36)
        text = font.render(f"score: {score} | id: {id} | best score: {best_score} by {by_id} | génération: {generation}", True, WHITE)
        text_rect = text.get_rect()
        text_rect.center = (600, screen.get_height() - 30)
        log_text = [
            "DEBUGG:",
            f"Gravity: {gravity}",
            f"Block_x: {block_x}",
            f"Block_y: {block_y}",
            f"Block_ofs: {block_ofs}",
            f"Vel_y: {vel_y}",
            f"Jump: {need_to_jump_check() == True}",
            f"Screen_y: {screen_y}",
        ]
        y_pos = 50
        for line in log_text:
            text_surface = font.render(line, True, WHITE)
            screen.blit(text_surface,(50, y_pos))
            y_pos += 30
        screen.blit(text, text_rect)
    
    if slow_time:
        time.sleep(0.0071)
    pygame.display.flip()