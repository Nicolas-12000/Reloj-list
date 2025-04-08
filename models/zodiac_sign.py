import pygame
import math

class ZodiacSign:
    def __init__(self, name, image_path, angle):
        self.name = name
        self.angle = angle
        self.prev = None
        self.next = None
        
        # Cargar imagen con manejo de errores
        try:
            self.image = pygame.image.load(image_path)
        except Exception as e:
            print(f"Error cargando imagen para {self.name}: {str(e)}")
            # Crear imagen de respaldo
            self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
            pygame.draw.rect(self.image, (255, 0, 0), (0, 0, 50, 50), 2)
        
        # Escalado seguro independientemente de si se cargó la imagen
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        
    def get_position(self, center, radius):
        """Calculate position based on angle and radius"""
        x = center[0] + radius * math.cos(math.radians(self.angle))
        y = center[1] + radius * math.sin(math.radians(self.angle))
        return (x - self.rect.width // 2, y - self.rect.height // 2)
        
    def is_active(self, current_hour_angle):
        """Check if this sign is currently active based on hour hand angle"""
        angle_diff = min(
            abs(self.angle - current_hour_angle),
            360 - abs(self.angle - current_hour_angle)
        )
        return angle_diff <= 15  # Active if hour hand is within 15 degrees

    def is_leo(self):
        """Check if this sign is Leo"""
        return self.name == "Leo"