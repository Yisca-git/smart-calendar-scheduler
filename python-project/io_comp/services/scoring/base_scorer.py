"""Base scorer abstract class"""

from abc import ABC, abstractmethod
from typing import Tuple
from datetime import timedelta
from ...models.time_slot import TimeSlot
from ...models.meeting_preferences import MeetingPreferences


class BaseScorer(ABC):
    """
    Abstract base class for all scoring criteria.
    
    Each scorer evaluates a time slot based on a specific criterion
    and returns a score between 0 and 1.
    """
    
    @property
    @abstractmethod
    def weight(self) -> float:
        """
        Weight of this criterion (0-1).
        
        All weights should sum to 1.0 in the composite scorer.
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Name of this scoring criterion"""
        pass
    
    @abstractmethod
    def score(
        self, 
        slot: TimeSlot, 
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> Tuple[float, str]:
        """
        Calculate score for a time slot.
        
        Args:
            slot: Time slot to score
            duration: Required meeting duration
            preferences: User preferences
            
        Returns:
            Tuple of (score, reason) where:
            - score is between 0.0 and 1.0
            - reason is a human-readable explanation
        """
        pass
    
    def weighted_score(
        self, 
        slot: TimeSlot, 
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> Tuple[float, str]:
        """
        Calculate weighted score.
        
        Returns:
            Tuple of (weighted_score, reason)
        """
        score, reason = self.score(slot, duration, preferences)
        return score * self.weight, reason
