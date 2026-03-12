"""Event model representing a calendar event"""

from dataclasses import dataclass
from .time_slot import TimeSlot


@dataclass(frozen=True)
class Event:
    """
    Represents a calendar event for a person.
    
    Immutable to ensure data integrity.
    """
    person: str
    subject: str
    time_slot: TimeSlot
    
    def __str__(self) -> str:
        """Format as 'Person: Subject (HH:MM-HH:MM)'"""
        return f"{self.person}: {self.subject} ({self.time_slot})"
