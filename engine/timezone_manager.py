import pytz
from datetime import datetime

class TimezoneManager:
    def __init__(self):
        self.timezones = [
            "Europe/Madrid",
            "Europe/Rome",
            "America/New_York", 
            "America/Sao_Paulo",
            "Asia/Tokyo",
            "America/Bogota"
        ]
        self.current_timezone_index = 0  # Empieza en Colombia
    
    def get_current_timezone(self):
        """Get the name of the current timezone"""
        return self.timezones[self.current_timezone_index]
    
    def get_current_timezone_object(self):
        """Get the pytz timezone object for the current timezone"""
        return pytz.timezone(self.timezones[self.current_timezone_index])
    
    def next_timezone(self):
        """Switch to the next timezone in the list"""
        self.current_timezone_index = (self.current_timezone_index + 1) % len(self.timezones)
    
    def prev_timezone(self):
        """Switch to the previous timezone in the list"""
        self.current_timezone_index = (self.current_timezone_index - 1) % len(self.timezones)