"""Time utility functions"""

from datetime import time, datetime, date, timedelta


class TimeUtils:
    """Utility functions for time operations"""
    
    @staticmethod
    def parse_time(time_str: str) -> time:
        """
        Parse time string in HH:MM format.
        
        Args:
            time_str: Time string like "08:30"
            
        Returns:
            time object
            
        Raises:
            ValueError: If format is invalid
        """
        time_str = time_str.strip()
        try:
            hour, minute = map(int, time_str.split(':'))
            return time(hour, minute)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid time format: {time_str}. Expected HH:MM") from e
    
    @staticmethod
    def add_duration(start: time, duration: timedelta) -> time:
        """
        Add duration to a time.
        
        Args:
            start: Starting time
            duration: Duration to add
            
        Returns:
            Resulting time
        """
        dt = datetime.combine(date.min, start) + duration
        return dt.time()
    
    @staticmethod
    def format_time(t: time) -> str:
        """Format time as HH:MM"""
        return t.strftime('%H:%M')
