"""Meeting preferences model"""

from dataclasses import dataclass


@dataclass
class MeetingPreferences:
    """
    Preferences for finding meeting times.
    
    These preferences affect the scoring of available time slots.
    """
    prefer_morning: bool = True
    avoid_lunch_time: bool = True
    prefer_longer_slots: bool = True
    minimize_fragmentation: bool = True
    
    @classmethod
    def default(cls) -> 'MeetingPreferences':
        """Create default preferences"""
        return cls()
