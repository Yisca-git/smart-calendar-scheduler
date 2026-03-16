"""Position in day scoring criterion"""

from datetime import timedelta
from typing import Tuple
from .base_scorer import BaseScorer
from ...models.time_slot import TimeSlot
from ...models.meeting_preferences import MeetingPreferences
from ...utils.work_day_config import WorkDayConfig


class PositionScorer(BaseScorer):
    """
    Scores time slots based on their position in the work day.
    
    Earlier slots leave more time for follow-up work.
    """
    
    @property
    def weight(self) -> float:
        return 0.20  # 20% of total score
    
    @property
    def name(self) -> str:
        return "Position in Day"
    
    def score(
        self, 
        slot: TimeSlot, 
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> Tuple[float, str]:
        """
        Score based on position in work day.
        
        First quarter (07:00-10:00): 1.0 - Plenty of time after
        Second quarter (10:00-13:00): 0.75 - Mid-morning
        Third quarter (13:00-16:00): 0.5 - Mid-afternoon
        Fourth quarter (16:00-19:00): 0.25 - Late in day
        """
        hour = slot.start_time.hour
        
        if hour < WorkDayConfig.EARLY_MORNING_END.hour:
            return 1.0, "+ Early in day - plenty of time after"
        elif hour < WorkDayConfig.MORNING_END.hour:
            return 0.75, "+ Mid-morning"
        elif hour < WorkDayConfig.EARLY_AFTERNOON_END.hour:
            return 0.5, "~ Mid-afternoon"
        else:
            return 0.25, "~ Late in day"
