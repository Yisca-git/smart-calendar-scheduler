"""Composite scorer combining all criteria"""

from typing import List
from datetime import timedelta
from .base_scorer import BaseScorer
from ...models.time_slot import TimeSlot
from ...models.meeting_preferences import MeetingPreferences
from ...models.scored_slot import ScoredSlot


class CompositeScorer:
    """
    Combines multiple scoring criteria into a single score.
    
    Validates that all weights sum to 1.0.
    """
    
    def __init__(self, scorers: List[BaseScorer]):
        """
        Initialize with a list of scorers.
        
        Args:
            scorers: List of scoring criteria
            
        Raises:
            ValueError: If weights don't sum to approximately 1.0
        """
        self.scorers = scorers
        
        # Validate weights
        total_weight = sum(s.weight for s in scorers)
        if not (0.99 <= total_weight <= 1.01):
            raise ValueError(
                f"Scorer weights must sum to 1.0, got {total_weight:.2f}"
            )
    
    def score_slot(
        self,
        slot: TimeSlot,
        duration: timedelta,
        preferences: MeetingPreferences
    ) -> ScoredSlot:
        """
        Calculate composite score for a time slot.
        
        Args:
            slot: Time slot to score
            duration: Required meeting duration
            preferences: User preferences
            
        Returns:
            ScoredSlot with total score (0-100) and reasons
        """
        total_score = 0.0
        reasons = []
        
        for scorer in self.scorers:
            weighted_score, reason = scorer.weighted_score(slot, duration, preferences)
            total_score += weighted_score
            reasons.append(f"[{scorer.name}] {reason}")
        
        # Convert to 0-100 scale
        final_score = total_score * 100
        
        return ScoredSlot(
            start_time=slot.start_time,
            end_time=slot.end_time,
            score=final_score,
            reasons=reasons
        )
