import time
import re
from datetime import datetime, timedelta
import math
from models.zodiac_sign import ZodiacSign

class ClockLogic:
    def __init__(self, timezone_manager):
        self.timezone_manager = timezone_manager
        self.custom_time = None
        self.active_flames = [True] * 12  # All flames start active
        self.last_hour = -1
        self.initialize_zodiac_signs()
        self.leo_angle = 150  # Leo's position in degrees
        
    def initialize_zodiac_signs(self):
        """Create a circular doubly linked list of zodiac signs"""
        signs_data = [
            ("Aries", "assets/zodiac/aries.png", 30),
            ("Taurus", "assets/zodiac/taurus.png", 60),
            ("Gemini", "assets/zodiac/gemini.png", 90),
            ("Cancer", "assets/zodiac/cancer.png", 120),
            ("Leo", "assets/zodiac/leo.png", 150),
            ("Virgo", "assets/zodiac/virgo.png", 180),
            ("Libra", "assets/zodiac/libra.png", 210),
            ("Scorpio", "assets/zodiac/scorpio.png", 240),
            ("Sagittarius", "assets/zodiac/sagittarius.png", 270),
            ("Capricorn", "assets/zodiac/capricorn.png", 300),
            ("Aquarius", "assets/zodiac/aquarius.png", 330),
            ("Pisces", "assets/zodiac/pisces.png", 0)
        ]
        
        # Create signs
        self.signs = []
        for name, path, angle in signs_data:
            self.signs.append(ZodiacSign(name, path, angle))
        
        # Link them in a circular doubly linked list
        for i in range(len(self.signs)):
            self.signs[i].prev = self.signs[(i-1) % len(self.signs)]
            self.signs[i].next = self.signs[(i+1) % len(self.signs)]
            
        # Set head of the list
        self.head_sign = self.signs[0]
    
    def update(self):
        """Update clock state based on current time"""
        current_time = self.get_current_time()
        current_hour = current_time.hour % 12
        
        # Update flame status each hour
        if current_hour != self.last_hour and self.last_hour != -1:
            # Turn off flame for the previous hour
            self.active_flames[self.last_hour] = False
            
            # Reset flames if all are off
            if not any(self.active_flames):
                self.active_flames = [True] * 12
        
        self.last_hour = current_hour
    
    def get_current_time(self):
        """Get the current time, considering custom time if set"""
        if self.custom_time:
            return self.custom_time
        return datetime.now(self.timezone_manager.get_current_timezone_object())
    
    def set_custom_time(self, time_str):
        """Set a custom time from the input field (format: HH:MM:SS)"""
        # Validate time format with regex
        if re.match(r'^([01]\d|2[0-3]):([0-5]\d):([0-5]\d)$', time_str):
            hours, minutes, seconds = map(int, time_str.split(':'))
            
            # Use the current date with custom time
            now = datetime.now(self.timezone_manager.get_current_timezone_object())
            self.custom_time = now.replace(hour=hours, minute=minutes, second=seconds)
        else:
            # Invalid time format, show warning but don't change time
            print("Invalid time format")
    
    def get_hour_angle(self):
        """Get the hour hand angle in degrees"""
        current_time = self.get_current_time()
        hour = current_time.hour % 12
        minute = current_time.minute
        # Each hour is 30 degrees, plus a small increment for minutes
        return (hour * 30) + (minute * 0.5)
    
    def get_minute_angle(self):
        """Get the minute hand angle in degrees"""
        current_time = self.get_current_time()
        minute = current_time.minute
        second = current_time.second
        # Each minute is 6 degrees, plus a small increment for seconds
        return (minute * 6) + (second * 0.1)
    
    def get_second_angle(self):
        """Get the second hand angle in degrees"""
        current_time = self.get_current_time()
        second = current_time.second
        millisecond = current_time.microsecond / 1000000
        # Each second is 6 degrees, plus a small increment for milliseconds
        return (second * 6) + (millisecond * 6)
    
    def get_active_flames(self):
        """Return the current state of flames"""
        return self.active_flames
    
    def is_leo_active(self):
        """Check if the hour hand is pointing to Leo"""
        hour_angle = self.get_hour_angle()
        return abs(hour_angle - self.leo_angle) <= 8