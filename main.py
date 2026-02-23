import pygame
import sys
import random
import time
import json
import os
import math

# --- 1. INITIALIZATION & DATA SAVE ---
pygame.init()
# Buffer 512 se sound aur animation ka delay khatam ho jata hai
pygame.mixer.pre_init(44100, -16, 2, 512) 
pygame.mixer.init()

INFO = pygame.display.Info()
WIDTH, HEIGHT = INFO.current_w, INFO.current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

SAVE_FILE = "progress.json"

def save_data():
    with open(SAVE_FILE, "w") as f:
        json.dump(player_data, f)

def load_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                return json.load(f)
        except: pass
    return {
        "level": 1, "xp": 0, "gold": 20000, "rank": "Bronze I",
        "base_health": 100, "attack_dmg": 20, "attack_speed": 0.12,
        "purchased": []
    }

player_data = load_data()

# Colors
WHITE, BLACK, GOLD, BLUE = (255, 255, 255), (0, 0, 0), (255, 215, 0), (0, 100, 255)
RED, GREEN, PURPLE = (255, 50, 50), (50, 255, 50), (150, 0, 255)
CYAN, DARK_NAVY = (0, 255, 255), (10, 10, 30)

font_small = pygame.font.SysFont("arial", 35)
font_med = pygame.font.SysFont("arial", 50)
font_big = pygame.font.SysFont("arial", 80)
# --- BGM MUSIC LOOP SYSTEM (45% Volume) ---
BGM_FILES = ["bgm1.mp3", "bgm2.mp3"]
current_bgm_index = 0

def play_bgm():
    global current_bgm_index
    try:
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(BGM_FILES[current_bgm_index])
            pygame.mixer.music.set_volume(0.45) 
            pygame.mixer.music.play()
            current_bgm_index = (current_bgm_index + 1) % len(BGM_FILES)
    except: pass

# --- SOUND SYSTEM (FIXED & SYNCED) ---
def play_sfx(sound_name):
    try:
        if sound_name == "hit": 
            pygame.mixer.Sound("hit.wav").play()
        elif sound_name == "laser": 
            s = pygame.mixer.Sound("laser.wav")
            s.set_volume(1.0)
            ch = pygame.mixer.find_channel()
            if ch:
                ch.play(s)
                # Sound cutting for sync
                s.fadeout(100) 
        elif sound_name == "win": 
            pygame.mixer.music.stop()
            pygame.mixer.stop()
            w = pygame.mixer.Sound("win.mp3")
            w.set_volume(1.0)
            w.play()
        elif sound_name == "sold": pygame.mixer.Sound("Sold1.mp3").play()
        elif sound_name == "click": pygame.mixer.Sound("Fire_watch.mp3").play()
    except: pass

def check_level_up():
    xp, lvl = player_data["xp"], player_data["level"]
    thresholds = {1: 100, 2: 500, 3: 600, 4: 2000, 5: 3500}
    next_xp = thresholds.get(lvl, lvl * 1500)
    if xp >= next_xp and lvl < 100:
        player_data["level"] += 1
        player_data["gold"] += 5000
        save_data()
        return True
    return False

def draw_text(msg, font, color, x, y, center=False):
    img = font.render(msg, True, color)
    if center: x = WIDTH // 2 - img.get_width() // 2
    screen.blit(img, (x, y))

def show_end_screen(session_gold, session_kills):
    pygame.mixer.music.stop() 
    pygame.mixer.stop() 
    time.sleep(0.2) 
    play_sfx("win") 
    waiting = True
    while waiting:
        screen.fill(BLACK)
        draw_text("MISSION OVER", font_big, RED, 0, 150, True)
        res_rect = pygame.Rect(WIDTH//2-300, 300, 600, 420)
        pygame.draw.rect(screen, (20, 20, 40), res_rect, border_radius=20)
        pygame.draw.rect(screen, GOLD, res_rect, 3, border_radius=20)
        draw_text(f"GOLD EARNED: +{session_gold}", font_med, GOLD, 0, 360, True)
        draw_text(f"KILLS: {session_kills}", font_med, WHITE, 0, 460, True)
        draw_text(f"TOTAL LEVEL: {player_data['level']}", font_med, CYAN, 0, 560, True)
        btn_back = pygame.Rect(WIDTH//2-150, 780, 300, 100)
        pygame.draw.rect(screen, GREEN, btn_back, border_radius=15)
        draw_text("CONTINUE", font_med, BLACK, 0, 805, True)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if btn_back.collidepoint(e.pos): play_sfx("click"); waiting = False
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
# --- 3. UNLIMITED STORE ---
def skill_shop():
    running = True
    message = ""
    while running:
        play_bgm()
        screen.fill(DARK_NAVY)
        back_btn = pygame.Rect(50, 50, 200, 90)
        pygame.draw.rect(screen, RED, back_btn, border_radius=15)
        draw_text("BACK", font_small, WHITE, 100, 75)
        draw_text("BLACK MARKET", font_big, GOLD, 0, 160, True)
        draw_text(f"GOLD: {player_data['gold']}", font_med, WHITE, 50, 260)
        draw_text(message, font_small, GREEN, 0, 320, True)

        items = [("Health +10", 10000, "H1", 10), ("Health +50", 50000, "H2", 50),
                 ("Attack DMG +5", 15000, "A1", 5), ("Attack Speed Up", 30000, "S1", 0.08)]

        y_pos, rects = 400, []
        for text, price, code, val in items:
            rect = pygame.Rect(WIDTH//2-300, y_pos, 600, 110)
            pygame.draw.rect(screen, (70, 70, 100), rect, border_radius=15)
            draw_text(f"{text} - {price}G", font_small, WHITE, WIDTH//2-260, y_pos+35)
            rects.append((rect, price, code, val))
            y_pos += 140

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.collidepoint(e.pos): 
                    play_sfx("click"); save_data(); running = False 
                for r, price, code, val in rects:
                    if r.collidepoint(e.pos):
                        if player_data["gold"] >= price:
                            player_data["gold"] -= price
                            play_sfx("sold")
                            if "H" in code: player_data["base_health"] += val
                            if "A" in code: player_data["attack_dmg"] += val
                            if "S" in code: player_data["attack_speed"] = max(0.04, player_data["attack_speed"] - 0.01)
                            message = "UPGRADED!"; save_data()
                        else: 
                            play_sfx("click"); message = "NEED MORE GOLD!"
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()

# --- 4. DIFFICULTY SELECTION MENU ---
def select_difficulty():
    selecting = True
    diff_settings = [("EASY", GREEN, 6, 1.5), ("MEDIUM", BLUE, 10, 1.0), ("HARD", RED, 16, 0.6)]
    while selecting:
        play_bgm()
        screen.fill(DARK_NAVY)
        draw_text("SELECT DIFFICULTY", font_big, GOLD, 0, 150, True)
        rects = []
        y_pos = 350
        for name, color, count, f_rate in diff_settings:
            r = pygame.Rect(WIDTH//2-250, y_pos, 500, 120)
            pygame.draw.rect(screen, color, r, border_radius=20)
            draw_text(name, font_med, WHITE, 0, y_pos+35, True)
            rects.append((r, name, count, f_rate))
            y_pos += 160
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                for r, name, count, f_rate in rects:
                    if r.collidepoint(e.pos): 
                        play_sfx("click"); return name, count, f_rate
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
# --- 5. CORE GAMEPLAY LOGIC ---
def run_actual_game(mode, diff_name, e_count, f_mult):
    start_time = time.time()
    game_running, auto_fire = True, False
    p_x, p_y = WIDTH // 2, HEIGHT - 250
    p_size, p_health = 60, player_data["base_health"]
    p_max_health, session_gold, session_kills = p_health, 0, 0
    enemies = []
    for i in range(e_count):
        enemies.append({"x": random.randint(100, WIDTH-100), "y": random.randint(150, 500),
                        "health": 100, "max_h": 100, "alive": True, "respawn": 0,
                        "is_boss": False, "size": 65, "last_fire": time.time() + random.random(),
                        "angle": random.random() * 6.28})
    p_bullets, e_bullets = [], []
    last_p_fire, bullet_speed = 0, 22 

    while game_running:
        play_bgm()
        screen.fill((5, 5, 15))
        current_time = time.time()
        elapsed_time = int(current_time - start_time)
        check_level_up()

        if auto_fire and current_time - last_p_fire > player_data["attack_speed"]:
            p_bullets.append([p_x, p_y - 60])
            play_sfx("laser")
            last_p_fire = current_time

        pygame.draw.polygon(screen, BLUE, [(p_x, p_y-p_size), (p_x-p_size, p_y+p_size), (p_x+p_size, p_y+p_size)])
        pygame.draw.rect(screen, RED, (p_x-50, p_y+p_size+20, 100, 12))
        pygame.draw.rect(screen, GREEN, (p_x-50, p_y+p_size+20, (max(0, p_health)/p_max_health)*100, 12))

        for en in enemies:
            if en["alive"]:
                if mode == "SPINNER":
                    en["angle"] += 0.05
                    en["x"] += math.sin(en["angle"]) * 8
                elif mode == "TELEPORT" and int(current_time * 2) % 5 == 0:
                    if random.random() < 0.02: en["x"] = random.randint(100, WIDTH-100)
                
                e_color = RED if not en["is_boss"] else GOLD
                pygame.draw.polygon(screen, e_color, [(en["x"], en["y"]+en["size"]), (en["x"]-en["size"], en["y"]-en["size"]), (en["x"]+en["size"], en["y"]-en["size"])])
                pygame.draw.rect(screen, (60,0,0), (en["x"]-50, en["y"]-en["size"]-20, 100, 8))
                pygame.draw.rect(screen, RED, (en["x"]-50, en["y"]-en["size"]-20, (en["health"]/en["max_h"])*100, 8))
                
                fire_delay = (0.4 if en["is_boss"] else 1.2) * f_mult
                if current_time - en["last_fire"] > fire_delay:
                    e_bullets.append([en["x"], en["y"] + en["size"]])
                    en["last_fire"] = current_time
            else:
                if current_time > en["respawn"]: en["alive"], en["health"], en["is_boss"], en["size"] = True, 100, False, 65

        for pb in p_bullets[:]:
            pb[1] -= bullet_speed
            pygame.draw.rect(screen, CYAN, (pb[0]-5, pb[1], 10, 30), border_radius=5)
            pygame.draw.rect(screen, WHITE, (pb[0]-2, pb[1]+5, 4, 20), border_radius=2)
            bullet_hit = False
            for en in enemies:
                if en["alive"] and abs(pb[0]-en["x"]) < en["size"] and abs(pb[1]-en["y"]) < en["size"]:
                    en["health"] -= player_data["attack_dmg"]; play_sfx("hit"); bullet_hit = True
                    if en["health"] <= 0:
                        en["alive"], en["respawn"] = False, current_time + 4
                        player_data["xp"] += 60; player_data["gold"] += 150
                        session_gold += 150; session_kills += 1
                    break
            if bullet_hit or pb[1] < -50:
                if pb in p_bullets: p_bullets.remove(pb)

        for eb in e_bullets[:]:
            eb[1] += bullet_speed - 10
            pygame.draw.circle(screen, (255, 100, 0), (int(eb[0]), int(eb[1])), 10)
            pygame.draw.circle(screen, WHITE, (int(eb[0]), int(eb[1])), 5)
            if abs(eb[0]-p_x) < p_size and abs(eb[1]-p_y) < p_size:
                p_health -= 15; play_sfx("hit")
                if eb in e_bullets: e_bullets.remove(eb)
            elif eb[1] > HEIGHT + 50:
                if eb in e_bullets: e_bullets.remove(eb)

        if p_health <= 0: game_running = False
        draw_text(f"GOLD: {player_data['gold']} | LVL: {player_data['level']}", font_small, GOLD, 30, 30)
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN: auto_fire = True
            if e.type == pygame.MOUSEMOTION and auto_fire: p_x, p_y = e.pos
            if e.type == pygame.QUIT: pygame.quit(); sys.exit()
    
    save_data()
    show_end_screen(session_gold, session_kills)

# --- 6. MAIN LOBBY ---
def lobby():
    while True:
        play_bgm()
        screen.fill((15, 15, 30))
        draw_text(f"G: {player_data['gold']}", font_med, GOLD, 50, 50)
        draw_text(f"LVL: {player_data['level']}", font_med, WHITE, WIDTH-250, 50)
        modes = [("WARZONE (DEFAULT)", GREEN, 400), ("ORBIT (SPINNER)", PURPLE, 550), ("VOID (TELEPORT)", BLUE, 700)]
        m_rects = []
        for n, c, y in modes:
            r = pygame.Rect(100, y, WIDTH-200, 120)
            pygame.draw.rect(screen, c, r, border_radius=25)
            draw_text(n, font_med, WHITE, 0, y+35, True); m_rects.append((r, n))
        
        shop_btn = pygame.Rect(100, 1000, WIDTH-200, 120)
        pygame.draw.rect(screen, (200, 100, 0), shop_btn, border_radius=25)
        draw_text("UPGRADE STORE", font_med, WHITE, 0, 1035, True)

        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                play_sfx("click")
                if shop_btn.collidepoint(e.pos): skill_shop()
                for r, n in m_rects:
                    if r.collidepoint(e.pos): 
                        m_type = "DEFAULT" if "DEFAULT" in n else ("SPINNER" if "SPINNER" in n else "TELEPORT")
                        d_name, d_count, d_f_rate = select_difficulty()
                        run_actual_game(m_type, d_name, d_count, d_f_rate)
            if e.type == pygame.QUIT: save_data(); pygame.quit(); sys.exit()

if __name__ == "__main__":
    lobby()
