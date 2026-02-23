import pygame

class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = pygame.Color('lightskyblue3')
        self.color_active = pygame.Color('dodgerblue2')
        self.color = self.color_inactive
        self.text = text
        # Screen ke mutabiq font size
        self.font = pygame.font.SysFont("arial", 32)
        self.txt_surface = self.font.render(text, True, (255, 255, 255))
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Agar box par click ho
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                # Android keyboard show karne ke liye
                if self.active:
                    pygame.key.start_text_input()
            else:
                self.active = False
                pygame.key.stop_text_input()
            
            self.color = self.color_active if self.active else self.color_inactive
            
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.active = False
                    pygame.key.stop_text_input()
                else:
                    self.text += event.unicode
                # Text ko dubara render karein
                self.txt_surface = self.font.render(self.text, True, (255, 255, 255))

    def draw(self, screen):
        # Box ke andar text draw karein
        screen.blit(self.txt_surface, (self.rect.x + 10, self.rect.y + 10))
        # Box ki boundary draw karein
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_text(self):
        return self.text
