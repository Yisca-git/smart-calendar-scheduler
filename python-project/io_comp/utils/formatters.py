"""Result formatting utilities"""

from typing import List
from ..models.scored_slot import ScoredSlot


class ResultFormatter:
    """Format results for display"""
    
    @staticmethod
    def format_scored_slots(scored_slots: List[ScoredSlot]) -> str:
        """
        Format a list of scored slots for display.
        
        Args:
            scored_slots: List of scored slots (should be sorted by score)
            
        Returns:
            Formatted string ready for display
        """
        if not scored_slots:
            return "No available time slots found"
        
        lines = ["Best Meeting Times:\n"]
        
        for i, slot in enumerate(scored_slots, 1):
            medal = slot.get_medal()
            rating = slot.get_rating()
            
            lines.append(
                f"{medal} #{i}: {slot.start_time.strftime('%H:%M')}-"
                f"{slot.end_time.strftime('%H:%M')} "
                f"(Score: {slot.score:.0f}/100 - {rating})"
            )
            
            for reason in slot.reasons:
                lines.append(f"   {reason}")
            lines.append("")
        
        return "\n".join(lines)
