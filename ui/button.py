import pygame

class Button:
    def __init__(self, text, position, size, bg_color, text_color, action=None):
        self.text = text
        self.position = position
        self.size = size
        self.bg_color = bg_color
        self.text_color = text_color
        self.action = action
        
        self.font = pygame.font.SysFont(None, 24)
        self.rect = pygame.Rect(position, size)
        self.is_hovered = False
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()
    
    def draw(self, surface):
        # Change color slightly when hovered
        color = (min(self.bg_color[0] + 20, 255), 
                min(self.bg_color[1] + 20, 255), 
                min(self.bg_color[2] + 20, 255)) if self.is_hovered else self.bg_color
        
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.text_color, self.rect, 2)
        
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)