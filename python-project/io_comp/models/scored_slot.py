"""Scored slot model for recommendations"""

from dataclasses import dataclass
from datetime import time
from typing import List


@dataclass
class ScoredSlot:
    """
    A time slot with a quality score and reasoning.
    
    Used for recommending the best meeting times.
    """
    start_time: time
    end_time: time
    score: float  # 0-100
    reasons: List[str]
    
    def get_rating(self) -> str:
        """Get textual rating based on score"""
        if self.score >= 80:
            return "Excellent"
        if self.score >= 65:
            return "Good"
        if self.score >= 50:
            return "OK"
        return "Poor"
    
    def get_medal(self) -> str:
        """Get medal emoji based on score"""
        if self.score >= 80:
            return "[BEST]"
        if self.score >= 65:
            return "[GOOD]"
        if self.score >= 50:
            return "[OK]"
        return "[LOW]"
    
    def __str__(self) -> str:
        """Format as 'HH:MM-HH:MM (Score: XX)'"""
        return (f"{self.start_time.strftime('%H:%M')}-"
                f"{self.end_time.strftime('%H:%M')} "
                f"(Score: {self.score:.0f})")
