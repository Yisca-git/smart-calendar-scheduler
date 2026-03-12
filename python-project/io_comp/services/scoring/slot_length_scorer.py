"""Slot length scoring criterion"""

from datetime import timedelta
from typing import Tuple
from .base_scorer import BaseScorer
from ...models.time_slot import TimeSlot
from ...models.meeting_preferences import MeetingPreferences


class SlotLengthScorer(BaseScorer):
    """
    Scores time slots based on their length relative to required duration.
    
    Longer slots provide more flexibility.
    """
    
    @property
    def weight(self) -> float:
        return 0.20  # 20% of total score
    
    @property
    def name(self) -> str:
        return "Slot Length"
    
    def score(
        self, 
        slot: TimeSlot, 
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> Tuple[float, str]:
        """
        Score based on slot length.
        
        2x+ required duration: 1.0 - Very flexible
        1.5x-2x required: 0.75 - Good buffer
        1x-1.5x required: 0.5 - Tight fit
        """
        available_minutes = slot.duration_minutes()
        required_minutes = duration.total_seconds() / 60
        ratio = available_minutes / required_minutes
        
        if ratio >= 2.0:
            return 1.0, f"+ Long slot ({available_minutes:.0f} min) - very flexible"
        elif ratio >= 1.5:
            return 0.75, f"+ Good buffer ({available_minutes:.0f} min)"
        else:
            return 0.5, f"~ Tight fit ({available_minutes:.0f} min)"
