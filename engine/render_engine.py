import pygame
import math
import time
from config import COLORS, FONTS

class RenderEngine:
    def __init__(self, screen):
        self.screen = screen
        self.leo_glow_alpha = 50  # Starting alpha for Leo glow effect
        self.leo_glow_increasing = True  # Direction of alpha change
        self.rotation_angle = 0  # For rotating central decoration
        self.zodiac_font = pygame.font.SysFont(FONTS["roman"], 36)
        
    def render_clock_face(self, center, radius):
        """Render the outer clock face with Roman numerals"""
        # Draw outer circle
        pygame.draw.circle(self.screen, COLORS["WHITE"], center, radius, 2)
        
        # Draw hour markers and Roman numerals
        roman_numerals = ["XII", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI"]
        for i in range(12):
            angle = math.radians(i * 30)
            # Hour marker position
            marker_start = (
                center[0] + (radius - 20) * math.sin(angle),
                center[1] - (radius - 20) * math.cos(angle)
            )
            marker_end = (
                center[0] + radius * math.sin(angle),
                center[1] - radius * math.cos(angle)
            )
            pygame.draw.line(self.screen, COLORS["WHITE"], marker_start, marker_end, 2)
            
            # Roman numeral position - slightly outside the marker
            text = self.zodiac_font.render(roman_numerals[i], True, COLORS["WHITE"])
            text_rect = text.get_rect(center=(
                center[0] + (radius - 40) * math.sin(angle),
                center[1] - (radius - 40) * math.cos(angle)
            ))
            self.screen.blit(text, text_rect)
    
    def render_zodiac_signs(self, center, radius, current_time):
        """Render the zodiac signs in a circle"""
        # This would normally use the linked list structure of ZodiacSign objects
        # But for simplicity, we're using placeholder circles
        for i in range(12):
            angle = math.radians(i * 30)
            pos = (
                int(center[0] + radius * math.sin(angle)),
                int(center[1] - radius * math.cos(angle))
            )
            # Placeholder for zodiac sign images
            pygame.draw.circle(self.screen, COLORS["WHITE"], pos, 15, 1)
            # In the actual implementation, you'd blit the ZodiacSign's image here
            
    def render_flames(self, center, radius, active_flames):
        """Render the flame indicators"""
        for i in range(12):
            angle = math.radians(i * 30)
            flame_pos = (
                int(center[0] + radius * math.sin(angle)),
                int(center[1] - radius * math.cos(angle))
            )
            
            # Draw flame with appropriate color
            color = COLORS["FLAME_ACTIVE"] if active_flames[i] else COLORS["FLAME_INACTIVE"]
            
            # Create a flame shape - a simple triangular shape for demonstration
            flame_points = [
                (flame_pos[0], flame_pos[1] - 20),  # Top point
                (flame_pos[0] - 10, flame_pos[1] + 5),  # Bottom left
                (flame_pos[0] + 10, flame_pos[1] + 5)   # Bottom right
            ]
            pygame.draw.polygon(self.screen, color, flame_points)
            
            # Add a glow effect for active flames
            if active_flames[i]:
                for offset in range(5, 0, -1):
                    alpha = 50 - offset * 10
                    if alpha > 0:
                        # Create a surface for the glow
                        glow_surface = pygame.Surface((30, 30), pygame.SRCALPHA)
                        glow_color = (*color, alpha)
                        glow_points = [
                            (15, 5 - offset),  # Top with offset
                            (5 - offset, 25 + offset),  # Bottom left with offset
                            (25 + offset, 25 + offset)  # Bottom right with offset
                        ]
                        pygame.draw.polygon(glow_surface, glow_color, glow_points)
                        self.screen.blit(glow_surface, (flame_pos[0] - 15, flame_pos[1] - 15))
    
    def render_clock_hands(self, center, hour_angle, minute_angle, second_angle):
        """Render the clock hands"""
        # Hour hand
        hour_x = center[0] + 150 * math.sin(math.radians(hour_angle))
        hour_y = center[1] - 150 * math.cos(math.radians(hour_angle))
        pygame.draw.line(self.screen, COLORS["WHITE"], center, (hour_x, hour_y), 6)
        
        # Minute hand
        minute_x = center[0] + 220 * math.sin(math.radians(minute_angle))
        minute_y = center[1] - 220 * math.cos(math.radians(minute_angle))
        pygame.draw.line(self.screen, COLORS["WHITE"], center, (minute_x, minute_y), 4)
        
        # Second hand
        second_x = center[0] + 240 * math.sin(math.radians(second_angle))
        second_y = center[1] - 240 * math.cos(math.radians(second_angle))
        pygame.draw.line(self.screen, COLORS["GOLD"], center, (second_x, second_y), 2)
        
        # Draw center circle
        pygame.draw.circle(self.screen, COLORS["WHITE"], center, 10)
        pygame.draw.circle(self.screen, COLORS["GOLD"], center, 5)
    
    def render_center_decoration(self, center, current_time):
        """Render the central zodiac decoration"""
        # Update rotation angle
        self.rotation_angle += 0.1
        if self.rotation_angle >= 360:
            self.rotation_angle = 0
            
        # Create layered circular patterns
        for i in range(5):
            radius = 80 - i * 12
            # Create a pulsing effect based on current time
            pulse = math.sin(time.time() * 2) * 10
            adjusted_radius = max(10, radius + pulse)
            
            # Draw decorative circle
            pygame.draw.circle(self.screen, COLORS["GOLD"], center, adjusted_radius, 1)
            
            # Draw radiating lines from center
            for j in range(12):
                angle = math.radians(j * 30 + self.rotation_angle)
                line_start = (
                    center[0] + (adjusted_radius - 10) * math.sin(angle),
                    center[1] - (adjusted_radius - 10) * math.cos(angle)
                )
                line_end = (
                    center[0] + adjusted_radius * math.sin(angle),
                    center[1] - adjusted_radius * math.cos(angle)
                )
                pygame.draw.line(self.screen, COLORS["GOLD"], line_start, line_end, 1)
        
        # Draw central star pattern
        points = []
        for i in range(12):
            angle = math.radians(i * 30 + self.rotation_angle / 2)
            radius = 40 if i % 2 == 0 else 20
            points.append((
                center[0] + radius * math.sin(angle),
                center[1] - radius * math.cos(angle)
            ))
        
        if len(points) >= 3:  # Need at least 3 points to draw a polygon
            pygame.draw.polygon(self.screen, COLORS["GOLD"], points, 1)
    
    def apply_leo_effect(self, center, zodiac_radius):
        """Apply special effect when the hour hand points to Leo"""
        # Find Leo's position
        leo_angle = math.radians(150)  # Leo's angle in degrees
        leo_pos = (
            int(center[0] + zodiac_radius * math.sin(leo_angle)),
            int(center[1] - zodiac_radius * math.cos(leo_angle))
        )
        
        # Create pulsating glow effect
        if self.leo_glow_increasing:
            self.leo_glow_alpha += 2
            if self.leo_glow_alpha >= 200:
                self.leo_glow_increasing = False
        else:
            self.leo_glow_alpha -= 2
            if self.leo_glow_alpha <= 50:
                self.leo_glow_increasing = True
        
        # Draw glow effect
        glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        glow_color = (*COLORS["GOLD"], self.leo_glow_alpha)
        pygame.draw.circle(glow_surface, glow_color, (50, 50), 30)
        self.screen.blit(glow_surface, (leo_pos[0] - 50, leo_pos[1] - 50))
        
        # Draw animated border
        for i in range(8):
            angle_offset = (time.time() * 100) % 360
            angle = math.radians((i * 45 + angle_offset) % 360)
            border_point = (
                leo_pos[0] + 35 * math.cos(angle),
                leo_pos[1] + 35 * math.sin(angle)
            )
            pygame.draw.circle(self.screen, COLORS["GOLD"], border_point, 3)