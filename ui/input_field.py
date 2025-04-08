import pygame

class InputField:
    def __init__(self, position, size, bg_color, text_color, placeholder=""):
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.placeholder = placeholder
        
        self.font = pygame.font.SysFont(None, 24)
        self.rect = pygame.Rect(position, size)
        self.text = ""
        self.active = False
        self.warning = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Toggle active state based on if the user clicked on the input box
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                # Only allow characters for time format
                if event.unicode.isdigit() or event.unicode == ":":
                    if len(self.text) < 8:  # Limit to 8 chars (HH:MM:SS)
                        self.text += event.unicode
            
            # Validate time format
            import re
            self.warning = not (self.text == "" or re.match(r'^([0-9]{1,2}:)?([0-9]{1,2}:)?[0-9]{1,2}$', self.text))
    
    def draw(self, surface):
        # Draw the input box
        border_color = (255, 0, 0) if self.warning else (255, 255, 255)
        bg_color = (100, 100, 100) if self.active else self.bg_color
        
        pygame.draw.rect(surface, bg_color, self.rect)
        pygame.draw.rect(surface, border_color, self.rect, 2)
        
        # Render text or placeholder
        if self.text:
            text_surface = self.font.render(self.text, True, self.text_color)
        else:
            text_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        
        # Position text in the input field
        text_rect = text_surface.get_rect(midleft=(self.rect.left + 5, self.rect.centery))
        surface.blit(text_surface, text_rect)
        
        # Draw warning icon if needed
        if self.warning:
            warning_font = pygame.font.SysFont(None, 24)
            warning_text = warning_font.render("⚠️", True, (255, 255, 0))
            surface.blit(warning_text, (self.rect.right - 20, self.rect.centery - 10))