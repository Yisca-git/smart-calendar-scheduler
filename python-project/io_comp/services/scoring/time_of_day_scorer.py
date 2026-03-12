"""Time of day scoring criterion"""

from datetime import timedelta
from typing import Tuple
from .base_scorer import BaseScorer
from ...models.time_slot import TimeSlot
from ...models.meeting_preferences import MeetingPreferences


class TimeOfDayScorer(BaseScorer):
    """
    Scores time slots based on time of day.
    
    Morning slots are generally preferred for productivity.
    """
    
    @property
    def weight(self) -> float:
        return 0.25  # 25% of total score
    
    @property
    def name(self) -> str:
        return "Time of Day"
    
    def score(
        self, 
        slot: TimeSlot, 
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> Tuple[float, str]:
        """
        Score based on time of day.
        
        Early morning (07:00-09:00): 1.0 - High energy
        Morning (09:00-12:00): 0.8 - Productive time
        Around lunch (12:00-14:00): 0.4 - Less ideal
        Early afternoon (14:00-16:00): 0.6 - Post-lunch
        Late afternoon (16:00-19:00): 0.2 - Low energy
        """
        hour = slot.start_time.hour
        
        if 7 <= hour < 9:
            return 1.0, "+ Early morning - high energy"
        elif 9 <= hour < 12:
            return 0.8, "+ Morning - productive time"
        elif 12 <= hour < 14:
            return 0.4, "~ Around lunch time"
        elif 14 <= hour < 16:
            return 0.6, "+ Early afternoon"
        else:  # 16-19
            return 0.2, "~ Late afternoon - low energy"
