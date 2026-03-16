"""Abstract base class for calendar repositories"""

from abc import ABC, abstractmethod
from typing import List
from ..models.event import Event


class CalendarRepositoryBase(ABC):
    """Abstract interface for calendar data access"""

    @abstractmethod
    def get_events_for_persons(self, persons: List[str]) -> List[Event]:
        """Get all events for a list of persons"""
        pass
