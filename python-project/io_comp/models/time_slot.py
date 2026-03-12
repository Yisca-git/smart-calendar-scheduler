"""TimeSlot model representing a time interval"""

from dataclasses import dataclass
from datetime import time, datetime, date, timedelta
from typing import Optional


@dataclass(frozen=True)
class TimeSlot:
    """
    Represents a time interval with start and end times.
    
    Immutable to ensure thread-safety and predictability.
    """
    start_time: time
    end_time: time
    
    def __post_init__(self):
        """Validate that start time is before end time"""
        if self.start_time >= self.end_time:
            raise ValueError(
                f"Start time {self.start_time} must be before end time {self.end_time}"
            )
    
    def duration_minutes(self) -> int:
        """Calculate duration in minutes"""
        delta = datetime.combine(date.min, self.end_time) - \
                datetime.combine(date.min, self.start_time)
        return int(delta.total_seconds() / 60)
    
    def overlaps(self, other: 'TimeSlot') -> bool:
        """Check if this slot overlaps with another slot"""
        return self.start_time < other.end_time and other.start_time < self.end_time
    
    def is_adjacent(self, other: 'TimeSlot') -> bool:
        """Check if this slot is adjacent to another slot"""
        return self.end_time == other.start_time or other.end_time == self.start_time
    
    def merge(self, other: 'TimeSlot') -> 'TimeSlot':
        """
        Merge with another slot.
        
        Raises:
            ValueError: If slots don't overlap or aren't adjacent
        """
        if not (self.overlaps(other) or self.is_adjacent(other)):
            raise ValueError("Cannot merge non-overlapping and non-adjacent slots")
        
        return TimeSlot(
            min(self.start_time, other.start_time),
            max(self.end_time, other.end_time)
        )
    
    def contains_duration(self, duration: timedelta) -> bool:
        """Check if this slot can contain the given duration"""
        required_minutes = duration.total_seconds() / 60
        return self.duration_minutes() >= required_minutes
    
    def __str__(self) -> str:
        """Format as HH:MM-HH:MM"""
        return f"{self.start_time.strftime('%H:%M')}-{self.end_time.strftime('%H:%M')}"
