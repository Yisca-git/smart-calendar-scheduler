"""End of day buffer scoring criterion"""

from datetime import time, datetime, date, timedelta
from typing import Tuple
from .base_scorer import BaseScorer
from ...models.time_slot import TimeSlot
from ...models.meeting_preferences import MeetingPreferences


class EndOfDayScorer(BaseScorer):
    """
    Scores time slots based on when the meeting would end.
    
    Meetings that end late in the day are less desirable.
    """
    
    @property
    def weight(self) -> float:
        return 0.15  # 15% of total score
    
    @property
    def name(self) -> str:
        return "End of Day Buffer"
    
    def score(
        self, 
        slot: TimeSlot, 
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> Tuple[float, str]:
        """
        Score based on meeting end time.
        
        Ends before 17:00: 1.0 - Good buffer
        Ends 17:00-18:00: 0.67 - Close to end
        Ends after 18:00: 0.33 - Very late
        """
        # Calculate when meeting would end
        meeting_end = self._add_duration(slot.start_time, duration)
        
        if meeting_end <= time(17, 0):
            return 1.0, "+ Ends with time to spare"
        elif meeting_end <= time(18, 0):
            return 0.67, "~ Ends close to work day end"
        else:
            return 0.33, "~ Ends very late"
    
    @staticmethod
    def _add_duration(start: time, duration: timedelta) -> time:
        """Add duration to time"""
        dt = datetime.combine(date.min, start) + duration
        return dt.time()
