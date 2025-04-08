import pygame
import sys
from datetime import datetime
import math
from engine.clock_logic import ClockLogic
from engine.render_engine import RenderEngine
from engine.timezone_manager import TimezoneManager
from ui.button import Button
from ui.input_field import InputField
from config import SCREEN_WIDTH, SCREEN_HEIGHT, COLORS, FONTS, CLOCK_PARAMS

class ZodiacApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Zodiac Clock")
        self.clock = pygame.time.Clock()
        
        # Initialize components
        self.timezone_manager = TimezoneManager()
        self.clock_logic = ClockLogic(self.timezone_manager)
        self.render_engine = RenderEngine(self.screen)
        
        # UI elements
        button_width, button_height = 30, 30
        self.prev_tz_button = Button("<", (50, 50), (button_width, button_height), 
                                    COLORS["WHITE"], COLORS["BLACK"], self.prev_timezone)
        self.next_tz_button = Button(">", (90, 50), (button_width, button_height), 
                                    COLORS["WHITE"], COLORS["BLACK"], self.next_timezone)
        
        self.time_input = InputField((150, 50), (150, 30), COLORS["WHITE"], 
                                    COLORS["BLACK"], "HH:MM:SS")
        self.apply_time_button = Button("Apply", (310, 50), (70, 30), 
                                       COLORS["WHITE"], COLORS["BLACK"], self.apply_custom_time)
        
        self.running = True
        
    def prev_timezone(self):
        self.timezone_manager.prev_timezone()
    
    def next_timezone(self):
        self.timezone_manager.next_timezone()
    
    def apply_custom_time(self):
        time_str = self.time_input.text
        self.clock_logic.set_custom_time(time_str)
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            self.prev_tz_button.handle_event(event)
            self.next_tz_button.handle_event(event)
            self.time_input.handle_event(event)
            self.apply_time_button.handle_event(event)
    
    def update(self):
        self.clock_logic.update()
    
    def render(self):
        # Clear screen
        self.screen.fill(COLORS["BLACK"])
        
        # Render clock elements
        self.render_engine.render_clock_face(CLOCK_PARAMS["clock_center"], 
                                           CLOCK_PARAMS["outer_radius"])
        self.render_engine.render_zodiac_signs(CLOCK_PARAMS["clock_center"], 
                                             CLOCK_PARAMS["zodiac_radius"], 
                                             self.clock_logic.get_current_time())
        self.render_engine.render_flames(CLOCK_PARAMS["clock_center"], 
                                       CLOCK_PARAMS["flames_radius"], 
                                       self.clock_logic.get_active_flames())
        self.render_engine.render_clock_hands(CLOCK_PARAMS["clock_center"], 
                                            self.clock_logic.get_hour_angle(), 
                                            self.clock_logic.get_minute_angle(), 
                                            self.clock_logic.get_second_angle())
        self.render_engine.render_center_decoration(CLOCK_PARAMS["clock_center"], 
                                                 self.clock_logic.get_current_time())
        
        # Apply Leo effect if applicable
        if self.clock_logic.is_leo_active():
            self.render_engine.apply_leo_effect(CLOCK_PARAMS["clock_center"], 
                                              CLOCK_PARAMS["zodiac_radius"])
        
        # Render UI elements
        self.prev_tz_button.draw(self.screen)
        self.next_tz_button.draw(self.screen)
        self.time_input.draw(self.screen)
        self.apply_time_button.draw(self.screen)
        
        # Display current timezone
        font = pygame.font.SysFont(FONTS["main"], 20)
        tz_text = font.render(f"Timezone: {self.timezone_manager.get_current_timezone()}", 
                             True, COLORS["WHITE"])
        self.screen.blit(tz_text, (400, 55))
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    app = ZodiacApp()
    app.run()
