import pygame
from economy import add_rewards, update_leaderboard, start_timer, end_timer, SKILLS, check_skill

def teleportation_lobby(current_user, start_game_func):
    screen = pygame.display.get_surface()
    font = pygame.font.SysFont("arial",40)
    header_font = pygame.font.SysFont("arial",60)
    running = True
    difficulties = ["Easy", "Normal", "Hard", "Hell"]

    while running:
        screen.fill((0,0,0))
        header = header_font.render("Teleportation Mode", True, (255,255,255))
        screen.blit(header, (screen.get_width()//2 - header.get_width()//2, 50))

        y = 200
        difficulty_rects = []
        for d in difficulties:
            rect = pygame.Rect(screen.get_width()//2 - 200, y, 400, 80)
            pygame.draw.rect(screen, (0,150,255), rect)
            screen.blit(font.render(d, True, (255,255,255)), (rect.x + 120, rect.y + 20))
            difficulty_rects.append((d, rect))
            y += 120

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for d, rect in difficulty_rects:
                    if rect.collidepoint(mx,my):
                        print(f"Teleportation started for {current_user} at {d}")
                        t0 = start_timer()
                        # Call actual game function
                        # start_game_func(current_user, mode="Teleportation", difficulty=d)
                        survive_time = end_timer(t0)
                        xp, gold = add_rewards(current_user,"Teleportation",d,survive_time,accuracy=100)
                        update_leaderboard(current_user,"Teleportation",survive_time)
                        print(f"XP: {xp} | Gold: {gold}")

                        for skill_name in SKILLS.keys():
                            if check_skill(current_user, skill_name):
                                print(f"Skill active: {skill_name}")

                        paused = True
                        while paused:
                            screen.fill((0,0,0))
                            pause_items = ["Continue", "Restart Game", "Back to Lobby"]
                            py = 200
                            pause_rects = []
                            for item in pause_items:
                                rect = pygame.Rect(screen.get_width()//2 - 200, py, 400, 80)
                                color = (0,150,255) if item!="Back to Lobby" else (255,0,0)
                                pygame.draw.rect(screen, color, rect)
                                screen.blit(font.render(item, True, (255,255,255)), (rect.x + 80, rect.y + 20))
                                pause_rects.append((item, rect))
                                py += 120
                            pygame.display.update()

                            for pevent in pygame.event.get():
                                if pevent.type == pygame.QUIT:
                                    pygame.quit()
                                    return
                                if pevent.type == pygame.MOUSEBUTTONDOWN:
                                    pmx, pmy = pygame.mouse.get_pos()
                                    for item, rect in pause_rects:
                                        if rect.collidepoint(pmx,pmy):
                                            if item=="Continue":
                                                paused = False
                                            elif item=="Restart Game":
                                                paused = False
                                                t0 = start_timer()
                                                survive_time = end_timer(t0)
                                                xp, gold = add_rewards(current_user,"Teleportation",d,survive_time,accuracy=100)
                                                update_leaderboard(current_user,"Teleportation",survive_time)
                                            elif item=="Back to Lobby":
                                                paused = False
                                                running = False
                                                break
                        break