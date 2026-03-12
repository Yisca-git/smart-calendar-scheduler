"""Lunch time proximity scoring criterion"""

from datetime import time, timedelta
from typing import Tuple
from .base_scorer import BaseScorer
from ...models.time_slot import TimeSlot
from ...models.meeting_preferences import MeetingPreferences


class LunchScorer(BaseScorer):
    """
    Scores time slots based on proximity to lunch time.
    
    Meetings during lunch are generally less desirable.
    """
    
    LUNCH_START = time(12, 0)
    LUNCH_END = time(13, 30)
    
    @property
    def weight(self) -> float:
        return 0.20  # 20% of total score
    
    @property
    def name(self) -> str:
        return "Lunch Proximity"
    
    def score(
        self, 
        slot: TimeSlot, 
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> Tuple[float, str]:
        """
        Score based on lunch time proximity.
        
        Not during lunch: 1.0
        Partially overlaps: 0.5
        Fully during lunch: 0.0
        """
        lunch_slot = TimeSlot(self.LUNCH_START, self.LUNCH_END)
        
        if not slot.overlaps(lunch_slot):
            return 1.0, "+ Not during lunch time"
        
        # Check if partially or fully overlaps
        if slot.start_time >= self.LUNCH_START and slot.end_time <= self.LUNCH_END:
            return 0.0, "- During lunch time"
        else:
            return 0.5, "~ Partially overlaps lunch time"
