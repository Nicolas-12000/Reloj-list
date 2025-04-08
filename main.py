import pygame
import sys
import math
import datetime
import re
import os
from pygame import gfxdraw

pygame.init()

WIDTH, HEIGHT = 800, 800
CENTER = (WIDTH // 2, HEIGHT // 2)
CLOCK_RADIUS = 350
ZODIAC_RADIUS = 200
HOUR_FLAME_RADIUS = 300

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GOLD = (255, 215, 0)
FLAME_ON = (90, 180, 255)   
FLAME_OFF = (40, 75, 102)   
TRANSPARENT = (0, 0, 0, 0)
BUTTON_COLOR = (20, 20, 40)
BUTTON_HOVER = (40, 40, 80)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Astrological Clock")
clock = pygame.time.Clock()

try:
    font_large = pygame.font.Font("assets/fonts/gothic.ttf", 36)
    font_small = pygame.font.Font("assets/fonts/gothic.ttf", 24)
    font_tiny = pygame.font.Font("assets/fonts/gothic.ttf", 18)
except:
    font_large = pygame.font.SysFont("serif", 36)
    font_small = pygame.font.SysFont("serif", 24)
    font_tiny = pygame.font.SysFont("serif", 18)

# Implementación de lista doblemente enlazada circular para los signos zodiacales
class ZodiacSign:
    def __init__(self, name, image_path, angle):
        self.name = name
        self.image = None
        self.image_path = image_path
        self.angle = angle
        # Referencias para la lista doblemente enlazada
        self.prev = None  # Referencia al nodo anterior
        self.next = None  # Referencia al nodo siguiente
        
        try:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (50, 50))
        except:
            self.image = self.create_placeholder_image()
    
    def create_placeholder_image(self):
        surface = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.circle(surface, WHITE, (25, 25), 20, 2)
        text = font_small.render(self.name[:3], True, WHITE)
        text_rect = text.get_rect(center=(25, 25))
        surface.blit(text, text_rect)
        return surface

# Función para crear la rueda del zodíaco como una lista doblemente enlazada circular
def create_zodiac_wheel():
    zodiac_data = [
        ("Aries", "assets/zodiac/aries.png", 0),
        ("Taurus", "assets/zodiac/taurus.png", 30),
        ("Gemini", "assets/zodiac/gemini.png", 60),
        ("Cancer", "assets/zodiac/cancer.png", 90),
        ("Leo", "assets/zodiac/leo.png", 120),
        ("Virgo", "assets/zodiac/virgo.png", 150),
        ("Libra", "assets/zodiac/libra.png", 180),
        ("Scorpio", "assets/zodiac/scorpio.png", 210),
        ("Sagittarius", "assets/zodiac/sagittarius.png", 240),
        ("Capricorn", "assets/zodiac/capricorn.png", 270),
        ("Aquarius", "assets/zodiac/aquarius.png", 300),
        ("Pisces", "assets/zodiac/pisces.png", 330),
    ]
    
    # Inicialización de la lista doblemente enlazada
    first_sign = None
    prev_sign = None
    
    # Creación de los nodos y enlaces
    for name, image_path, angle in zodiac_data:
        sign = ZodiacSign(name, image_path, angle)
        
        if first_sign is None:
            first_sign = sign
        
        # Establecimiento de enlaces dobles entre nodos
        if prev_sign is not None:
            prev_sign.next = sign
            sign.prev = prev_sign
        
        prev_sign = sign
    
    # Cerrar el círculo conectando el último con el primero
    if prev_sign and first_sign:
        prev_sign.next = first_sign
        first_sign.prev = prev_sign
    
    return first_sign

# Flame class for the hour indicators
class Flame:
    def __init__(self, hour, radius):
        self.hour = hour
        self.radius = radius
        self.angle = (hour * 30) - 90  # Convert hour to angle (0 at 3 o'clock, -90 to adjust)
        self.is_on = True
        self.alpha = 255
        self.fade_direction = 1
        self.glow_intensity = 0
        self.glow_direction = 1
    
    def update(self, current_hour):
        # Update flame state based on current hour
        self.is_on = self.hour >= current_hour
        
        # Update glow animation effect
        self.glow_intensity += self.glow_direction * 2
        if self.glow_intensity >= 50 or self.glow_intensity <= 0:
            self.glow_direction *= -1
        
        # Update alpha for fade effect
        if self.is_on:
            self.alpha += self.fade_direction * 3
            if self.alpha >= 255 or self.alpha <= 180:
                self.fade_direction *= -1
    
    def draw(self, surface):
        x = CENTER[0] + self.radius * math.cos(math.radians(self.angle))
        y = CENTER[1] + self.radius * math.sin(math.radians(self.angle))
        
        # Draw flame shape
        color = FLAME_ON if self.is_on else FLAME_OFF
        
        # Create flame shape points
        flame_points = [
            (x, y),
            (x - 20, y - 15),
            (x, y - 40 - (self.glow_intensity if self.is_on else 0)),
            (x + 20, y - 15)
        ]
        
        # Draw main flame
        pygame.draw.polygon(surface, color, flame_points)
        
        # Draw glow effect for active flames
        if self.is_on:
            glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.polygon(glow_surface, (*color[:3], 100), [
                (50, 50),
                (30, 35),
                (50, 10 - self.glow_intensity // 2),
                (70, 35)
            ])
            surface.blit(glow_surface, (x - 50, y - 50))
        
        # Draw the hour number (Roman numeral)
        roman_numerals = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII"]
        num_text = font_large.render(roman_numerals[self.hour - 1], True, WHITE)
        text_rect = num_text.get_rect(center=(x, y))
        surface.blit(num_text, text_rect)

# Function to validate time input
def validate_time(time_str):
    pattern = r'^([01]?[0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])$'
    return re.match(pattern, time_str) is not None

# Button class for UI interaction
class Button:
    def __init__(self, x, y, width, height, text, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.color = BUTTON_COLOR
        self.hover_color = BUTTON_HOVER
        self.text_color = WHITE
        self.is_hovered = False
        self.alpha = 200  # Semi-transparent
        self.clicked = False
    
    def update(self, mouse_pos):
        # Check if mouse is hovering over button
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def draw(self, surface):
        # Draw button with rounded corners
        color = self.hover_color if self.is_hovered else self.color
        
        # Create a surface for the semi-transparent button
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, (*color, self.alpha), (0, 0, self.rect.width, self.rect.height), border_radius=10)
        surface.blit(button_surface, self.rect)
        
        # Draw border
        pygame.draw.rect(surface, WHITE, self.rect, 1, border_radius=10)
        
        # Draw text
        text_surface = font_small.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

# Time input modal dialog
class TimeInputModal:
    def __init__(self):
        self.visible = False
        self.width = 400
        self.height = 200
        self.rect = pygame.Rect(WIDTH//2 - self.width//2, HEIGHT//2 - self.height//2, self.width, self.height)
        self.text = ''
        self.invalid = False
        self.time_result = None
        self.submitted = False
        self.close_button = Button(WIDTH//2 + self.width//2 - 30, HEIGHT//2 - self.height//2 + 10, 20, 20, "✕")
        self.submit_button = Button(WIDTH//2 - 50, HEIGHT//2 + self.height//2 - 50, 100, 30, "Aplicar")
    
    def toggle_visibility(self):
        self.visible = not self.visible
        if self.visible:
            self.text = ''
            self.invalid = False
    
    def handle_event(self, event):
        if not self.visible:
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if close button is clicked
            if self.close_button.rect.collidepoint(event.pos):
                self.visible = False
                return
            
            # Check if submit button is clicked
            if self.submit_button.rect.collidepoint(event.pos):
                self.submit_time()
                return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.submit_time()
            elif event.key == pygame.K_ESCAPE:
                self.visible = False
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
                self.invalid = False
            else:
                # Only allow digits and colons
                if event.unicode.isdigit() or event.unicode == ':':
                    self.text += event.unicode
    
    def submit_time(self):
        if validate_time(self.text):
            try:
                h, m, s = map(int, self.text.split(':'))
                self.time_result = (h, m, s)
                self.submitted = True
                self.visible = False
                self.text = ''
                self.invalid = False
            except:
                self.invalid = True
        else:
            self.invalid = True
    
    def update(self, mouse_pos):
        if self.visible:
            self.close_button.update(mouse_pos)
            self.submit_button.update(mouse_pos)
    
    def draw(self, surface):
        if not self.visible:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        surface.blit(overlay, (0, 0))
        
        # Draw modal background
        pygame.draw.rect(surface, (20, 20, 30), self.rect, border_radius=15)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=15)
        
        # Draw title
        title_text = font_large.render("Cambiar Hora", True, WHITE)
        title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - self.height//2 + 30))
        surface.blit(title_text, title_rect)
        
        # Draw input field
        input_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 20, 300, 40)
        pygame.draw.rect(surface, (40, 40, 60), input_rect, border_radius=5)
        pygame.draw.rect(surface, WHITE, input_rect, 2, border_radius=5)
        
        # Draw input text
        input_text = font_small.render(self.text, True, WHITE)
        input_text_rect = input_text.get_rect(center=input_rect.center)
        surface.blit(input_text, input_text_rect)
        
        # Draw placeholder text if empty
        if not self.text:
            placeholder = font_small.render("HH:MM:SS", True, (150, 150, 150))
            placeholder_rect = placeholder.get_rect(center=input_rect.center)
            surface.blit(placeholder, placeholder_rect)
        
        # Draw error message if invalid
        if self.invalid:
            error_text = font_tiny.render("⚠️ Formato inválido! Use HH:MM:SS", True, (255, 100, 100))
            error_rect = error_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 30))
            surface.blit(error_text, error_rect)
        
        # Draw close button
        self.close_button.draw(surface)
        
        # Draw submit button
        self.submit_button.draw(surface)
    
    def get_time(self):
        if self.submitted:
            self.submitted = False
            return self.time_result
        return None

class CentralDecoration:
    def __init__(self):
        self.rotation = 0
        self.scale_factor = 1.0
        self.scale_direction = 1
        self.particles = []
        self.generate_particles()
    
    def generate_particles(self):
        self.particles = []
        for i in range(12):
            angle = i * 30
            distance = 50 + (i % 3) * 20
            self.particles.append({
                'angle': angle,
                'distance': distance,
                'size': 5 + (i % 4),
                'color': GOLD if i % 3 == 0 else WHITE,
                'speed': 0.5 + (i % 5) * 0.2
            })
    
    def update(self):
        self.rotation += 0.2
        
        self.scale_factor += 0.005 * self.scale_direction
        if self.scale_factor > 1.1 or self.scale_factor < 0.9:
            self.scale_direction *= -1
        
        for particle in self.particles:
            particle['angle'] += particle['speed']
            if particle['angle'] >= 360:
                particle['angle'] -= 360
    
    def draw(self, surface):
        for i in range(3):
            radius = 40 + i * 20
            pygame.draw.circle(surface, WHITE, CENTER, int(radius * self.scale_factor), 1)
        
        for i in range(8):
            angle = self.rotation + i * 45
            x = CENTER[0] + 80 * math.cos(math.radians(angle))
            y = CENTER[1] + 80 * math.sin(math.radians(angle))
            pygame.draw.circle(surface, GOLD, (int(x), int(y)), 3)
        
        for particle in self.particles:
            angle = particle['angle']
            distance = particle['distance'] * self.scale_factor
            x = CENTER[0] + distance * math.cos(math.radians(angle))
            y = CENTER[1] + distance * math.sin(math.radians(angle))
            pygame.draw.circle(surface, particle['color'], (int(x), int(y)), particle['size'])

class AstrologicalClock:
    def __init__(self):
        self.current_time = datetime.datetime.now()
        self.custom_time_set = False
        self.clock_start_time = datetime.datetime.now()
        self.real_start_time = datetime.datetime.now()
        
        self.flames = [Flame(h, HOUR_FLAME_RADIUS) for h in range(1, 13)]
        self.zodiac_wheel = create_zodiac_wheel()
        self.central_decoration = CentralDecoration()
        
        self.time_modal = TimeInputModal()
        self.change_time_button = Button(WIDTH - 140, 20, 120, 40, "Cambiar Hora")
        
        self.leo_effect_active = False
        self.leo_glow = 0
        self.leo_glow_direction = 1
    
    def set_custom_time(self, hours, minutes, seconds):
        self.real_start_time = datetime.datetime.now()
        
        now = datetime.datetime.now()
        self.clock_start_time = now.replace(hour=hours, minute=minutes, second=seconds)
        self.custom_time_set = True
    
    def update(self, mouse_pos):
        elapsed = datetime.datetime.now() - self.real_start_time
        
        if self.custom_time_set:
            self.current_time = self.clock_start_time + elapsed
        else:
            self.current_time = datetime.datetime.now()
        
        self.change_time_button.update(mouse_pos)
        self.time_modal.update(mouse_pos)
        
        custom_time = self.time_modal.get_time()
        if custom_time:
            self.set_custom_time(*custom_time)

        current_hour = self.current_time.hour % 12
        if current_hour == 0:
            current_hour = 12
            
        for flame in self.flames:
            flame.update(current_hour)
        
        self.central_decoration.update()
        
        hour_angle = (self.current_time.hour % 12) * 30 + self.current_time.minute / 2 - 90
        if 142 <= hour_angle % 360 <= 158:
            self.leo_effect_active = True
            self.leo_glow += self.leo_glow_direction * 5
            if self.leo_glow >= 200 or self.leo_glow <= 50:
                self.leo_glow_direction *= -1
        else:
            self.leo_effect_active = False
            self.leo_glow = 0
    
    def draw(self, surface):
        
        surface.fill(BLACK)
        
       
        pygame.draw.circle(surface, WHITE, CENTER, CLOCK_RADIUS, 3)
        
       
        for i in range(60):
            angle = i * 6 - 90
            start_pos = (
                CENTER[0] + (CLOCK_RADIUS - 10) * math.cos(math.radians(angle)),
                CENTER[1] + (CLOCK_RADIUS - 10) * math.sin(math.radians(angle))
            )
            if i % 5 == 0:
                end_pos = (
                    CENTER[0] + (CLOCK_RADIUS - 30) * math.cos(math.radians(angle)),
                    CENTER[1] + (CLOCK_RADIUS - 30) * math.sin(math.radians(angle))
                )
                width = 3
            else:  # Minute marks
                end_pos = (
                    CENTER[0] + (CLOCK_RADIUS - 20) * math.cos(math.radians(angle)),
                    CENTER[1] + (CLOCK_RADIUS - 20) * math.sin(math.radians(angle))
                )
                width = 1
            pygame.draw.line(surface, WHITE, start_pos, end_pos, width)
        
        # Draw flames (hour indicators)
        for flame in self.flames:
            flame.draw(surface)
        
        # Draw inner zodiac circle
        pygame.draw.circle(surface, WHITE, CENTER, ZODIAC_RADIUS, 2)
        
        # Draw zodiac signs
        current_sign = self.zodiac_wheel
        for _ in range(12):
            angle_rad = math.radians(current_sign.angle - 90)  # Adjust to start from top
            x = CENTER[0] + ZODIAC_RADIUS * math.cos(angle_rad)
            y = CENTER[1] + ZODIAC_RADIUS * math.sin(angle_rad)
            
            sign_rect = current_sign.image.get_rect(center=(x, y))
            
            # Special Leo effect
            if current_sign.name == "Leo" and self.leo_effect_active:
                # Create glow effect
                glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (GOLD[0], GOLD[1], GOLD[2], self.leo_glow), (50, 50), 40)
                surface.blit(glow_surface, (x - 50, y - 50))
                
                # Draw highlighted border
                pygame.draw.circle(surface, GOLD, (int(x), int(y)), 30, 2)
            
            surface.blit(current_sign.image, sign_rect)
            current_sign = current_sign.next
        
        # Draw central decoration
        self.central_decoration.draw(surface)
        
        # Draw inner zodiac symbols circle
        pygame.draw.circle(surface, WHITE, CENTER, 100, 1)
        
        # Draw clock hands
        self.draw_clock_hands(surface)
        
        # Display current time elegantly in the top left
        time_str = self.current_time.strftime("%H:%M:%S")
        
        # Create a semi-transparent background for the time display
        time_surface = font_small.render(time_str, True, WHITE)
        time_bg_rect = pygame.Rect(20, 20, time_surface.get_width() + 20, 40)
        time_bg = pygame.Surface((time_bg_rect.width, time_bg_rect.height), pygame.SRCALPHA)
        time_bg.fill((20, 20, 30, 150))
        surface.blit(time_bg, time_bg_rect)
        pygame.draw.rect(surface, WHITE, time_bg_rect, 1, border_radius=5)
        
        # Draw the time text
        surface.blit(time_surface, (time_bg_rect.x + 10, time_bg_rect.y + 10))
        
        # Draw change time button in the top right
        self.change_time_button.draw(surface)
        
        # Draw time modal dialog if active
        self.time_modal.draw(surface)
    
    def draw_clock_hands(self, surface):
        hour = self.current_time.hour % 12
        minute = self.current_time.minute
        second = self.current_time.second
        millisecond = self.current_time.microsecond / 1000000
        
        # Hour hand - smooth movement
        hour_angle = (hour * 30 + minute / 2) - 90  # Each hour is 30 degrees, -90 to start from top
        hour_x = CENTER[0] + 150 * math.cos(math.radians(hour_angle))
        hour_y = CENTER[1] + 150 * math.sin(math.radians(hour_angle))
        pygame.draw.line(surface, WHITE, CENTER, (hour_x, hour_y), 6)
        
        # Minute hand - smooth movement
        minute_angle = (minute * 6 + second / 10) - 90  # Each minute is 6 degrees, with smooth movement from seconds
        minute_x = CENTER[0] + 200 * math.cos(math.radians(minute_angle))
        minute_y = CENTER[1] + 200 * math.sin(math.radians(minute_angle))
        pygame.draw.line(surface, WHITE, CENTER, (minute_x, minute_y), 4)
        
        # Second hand - smooth movement
        second_angle = (second * 6 + millisecond * 6) - 90  # Each second is 6 degrees, with smooth movement
        second_x = CENTER[0] + 220 * math.cos(math.radians(second_angle))
        second_y = CENTER[1] + 220 * math.sin(math.radians(second_angle))
        pygame.draw.line(surface, GOLD, CENTER, (second_x, second_y), 2)
        
        # Center circle
        pygame.draw.circle(surface, WHITE, CENTER, 10)
        pygame.draw.circle(surface, GOLD, CENTER, 5)
    
    def handle_event(self, event):
        # Handle button clicks
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.change_time_button.rect.collidepoint(event.pos):
                self.time_modal.toggle_visibility()
        
        # Pass events to the time modal
        self.time_modal.handle_event(event)

# Main function
def main():
    # Create assets directory structure if it doesn't exist
    os.makedirs("assets/zodiac", exist_ok=True)
    os.makedirs("assets/fonts", exist_ok=True)
    
    # Initialize clock - it starts with system time by default
    astrological_clock = AstrologicalClock()
    
    pygame.display.set_caption("Reloj Astrológico Interactivo")
    
    # Main game loop
    running = True
    while running:
        # Get current mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Pass events to the clock for UI handling
            astrological_clock.handle_event(event)
        
        # Update clock state
        astrological_clock.update(mouse_pos)
        
        # Draw everything
        astrological_clock.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
    pygame.quit()
    sys.exit()