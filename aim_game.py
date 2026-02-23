# aim_game.py (full updated)
import pygame
import random
import os
from game_stats import calculate_accuracy, calculate_reaction_stats, get_rank
from economy import SKILLS, check_skill  # hooks only

pygame.init()

# -------- SCREEN SETTINGS --------
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# -------- COLORS --------
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLACK = (0,0,0)
YELLOW = (255,255,0)

# -------- FONT --------
font = pygame.font.SysFont("arial",40)
big = pygame.font.SysFont("arial",80)

# -------- GAME SETTINGS --------
RADIUS = 70
speed_delay_default = {"Easy":500, "Normal":250, "Hard":150, "Hell":70}
fall_speed_default = {"Easy":4, "Normal":7, "Hard":11, "Hell":18}

# -------- GAME VARIABLES --------
targets = []
booms = []
score = 0
reaction_list = []
last_reaction = 0
hits = 0
clicks = 0
hearts = 3
spawn_timer = 0
paused = False

# -------- ASSETS PATH --------
ASSETS_DIR = "assets"

def load_avatar():
    avatar_path = os.path.join(ASSETS_DIR, "avatars", "default.jpg")
    try:
        img = pygame.image.load(avatar_path)
        img = pygame.transform.scale(img, (150,150))
        return img
    except Exception as e:
        print(f"Error loading avatar: {e}")
        return None

def load_banner():
    banner_path = os.path.join(ASSETS_DIR, "banners", "default01.jpg")
    try:
        img = pygame.image.load(banner_path)
        img = pygame.transform.scale(img, (WIDTH, 200))
        return img
    except Exception as e:
        print(f"Error loading banner: {e}")
        return None

# -------- FUNCTIONS --------
def text(msg,f,color,x,y):
    screen.blit(f.render(msg,True,color),(x,y))

def reset_game():
    global targets, booms, score, hits, clicks, hearts, reaction_list, last_reaction
    targets.clear()
    booms.clear()
    score = hits = clicks = 0
    hearts = 3
    reaction_list.clear()
    last_reaction = 0

def spawn_target():
    global targets, booms
    x = random.randint(RADIUS, WIDTH-RADIUS)
    for t in targets:
        if abs(x-t["x"]) < RADIUS*2:
            return
    targets.append({"x":x, "y":-100, "spawn_time":pygame.time.get_ticks()})
    if random.randint(1,4)==1:
        bx = random.randint(RADIUS, WIDTH-RADIUS)
        booms.append({"x":bx, "y":-100})

# -------- MAIN GAME LOOP --------
def start_game(user_profile, difficulty="Hard"):
    global paused, targets, booms, score, hits, clicks, hearts, reaction_list, last_reaction, spawn_timer
    reset_game()
    state = "game"

    speed_delay = speed_delay_default.get(difficulty,150)
    fall_speed = fall_speed_default.get(difficulty,11)
    avatar = load_avatar()
    banner = load_banner()
    t0 = pygame.time.get_ticks()  # Timer start

    while state:
        screen.fill(BLACK)
        spawn_timer += clock.get_time()
        if spawn_timer > speed_delay:
            spawn_target()
            spawn_timer = 0

        # Pause button
        pygame.draw.rect(screen,YELLOW,(20,20,120,50))
        text("PAUSE",font,BLACK,30,30)

        # Avatar & Banner
        if banner:
            screen.blit(banner,(0,0))
        if avatar:
            screen.blit(avatar,(WIDTH-200,20))

        # Hearts
        for i in range(hearts):
            pygame.draw.circle(screen,RED,(40,150+i*60),20)

        # Targets
        for t in targets[:]:
            t["y"] += fall_speed
            pygame.draw.circle(screen,GREEN,(t["x"],t["y"]),RADIUS)
            if t["y"]>HEIGHT:
                targets.remove(t)
                hearts -=1

        # Booms
        for b in booms[:]:
            b["y"] += fall_speed
            pygame.draw.circle(screen,WHITE,(b["x"],b["y"]),RADIUS)
            pygame.draw.circle(screen,RED,(b["x"],b["y"]),RADIUS-25)
            if b["y"]>HEIGHT:
                booms.remove(b)

        # HUD
        text(f"Score:{score}",font,WHITE,WIDTH-300,20)
        text(f"Acc:{calculate_accuracy(hits, clicks)}%",font,WHITE,WIDTH-300,80)
        text(f"Reaction:{last_reaction}ms",font,WHITE,WIDTH-300,140)
        rank = get_rank(score)
        text(f"Rank:{rank}",font,YELLOW,WIDTH-300,200)

        pygame.display.update()

        # EVENTS
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                mx,my=pygame.mouse.get_pos()
                clicks += 1

                # Pause clicked
                if 20<mx<140 and 20<my<70:
                    paused = True
                    while paused:
                        screen.fill(BLACK)
                        text("PAUSED",big,RED,WIDTH//2-100,HEIGHT//2-200)
                        text("1. New Game",font,WHITE,WIDTH//2-100,HEIGHT//2-50)
                        text("2. Continue",font,WHITE,WIDTH//2-100,HEIGHT//2+50)
                        text("3. Back to Lobby",font,WHITE,WIDTH//2-100,HEIGHT//2+150)
                        pygame.display.update()
                        for pe in pygame.event.get():
                            if pe.type == pygame.MOUSEBUTTONDOWN:
                                px,py=pygame.mouse.get_pos()
                                # Simple coordinate checks, adjust as needed
                                if HEIGHT//2-50<py<HEIGHT//2+10:
                                    paused = False
                                    reset_game()
                                    t0 = pygame.time.get_ticks()
                                elif HEIGHT//2+50<py<HEIGHT//2+110:
                                    paused=False
                                elif HEIGHT//2+150<py<HEIGHT//2+210:
                                    paused=False
                                    return  # back to lobby

                # Target hit
                for t in targets[:]:
                    if ((mx-t["x"])**2 + (my-t["y"])**2)**0.5 < RADIUS:
                        hits+=1
                        score+=10
                        reaction = pygame.time.get_ticks()-t["spawn_time"]
                        reaction_list.append(reaction)
                        last_reaction = reaction
                        targets.remove(t)

                # Boom hit
                for b in booms[:]:
                    if ((mx-b["x"])**2 + (my-b["y"])**2)**0.5 < RADIUS:
                        state=None

        if hearts<=0:
            state=None

        clock.tick(60)

    # End timer
    survive_time = pygame.time.get_ticks()-t0

    # Game over stats
    screen.fill(BLACK)
    avg,best,worst = calculate_reaction_stats(reaction_list)
    acc = calculate_accuracy(hits, clicks)
    text("GAME OVER",big,RED,WIDTH//2-200,200)
    text(f"Score:{score}",font,WHITE,WIDTH//2-100,400)
    text(f"Accuracy:{acc}%",font,WHITE,WIDTH//2-100,450)
    text(f"Avg Reaction:{avg}ms",font,WHITE,WIDTH//2-150,500)
    text(f"Best Reaction:{best}ms",font,WHITE,WIDTH//2-150,550)
    text(f"Worst Reaction:{worst}ms",font,WHITE,WIDTH//2-150,600)
    text(f"Rank:{get_rank(score)}",font,YELLOW,WIDTH//2-100,650)
    text("Tap to return",font,WHITE,WIDTH//2-150,700)
    pygame.display.update()

    # Return survive_time for rewards integration
    waiting=True
    while waiting:
        for e in pygame.event.get():
            if e.type==pygame.MOUSEBUTTONDOWN:
                waiting=False
    return survive_time