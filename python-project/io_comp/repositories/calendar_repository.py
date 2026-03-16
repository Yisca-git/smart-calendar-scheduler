"""Calendar data repository"""

import csv
import logging
from pathlib import Path
from typing import List, Dict
from ..models.event import Event
from ..models.time_slot import TimeSlot
from ..utils.time_utils import TimeUtils
from ..utils.exceptions import CalendarFileNotFoundError, InvalidCalendarFormatError
from .calendar_repository_base import CalendarRepositoryBase

logger = logging.getLogger(__name__)


class CalendarRepository(CalendarRepositoryBase):
    """
    Repository for loading calendar data from CSV.
    
    Implements caching to avoid repeated file reads.
    """
    
    def __init__(self, csv_path: Path):
        """
        Initialize repository with CSV file path.
        
        Args:
            csv_path: Path to the calendar CSV file
        """
        self.csv_path = csv_path
        self._cache: Dict[str, List[Event]] = {}
        self._all_events: List[Event] = None
    
    def load_events(self) -> List[Event]:
        """
        Load all events from CSV file.
        
        Returns:
            List of all events
            
        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If CSV format is invalid
        """
        if self._all_events is not None:
            return self._all_events
        
        if not self.csv_path.exists():
            raise CalendarFileNotFoundError(f"Calendar file not found: {self.csv_path}")
        
        events = []
        
        with open(self.csv_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for line_num, row in enumerate(reader, 1):
                if len(row) != 4:
                    raise InvalidCalendarFormatError(
                        f"Invalid CSV format at line {line_num}: expected 4 columns, got {len(row)}"
                    )
                
                person, subject, start_str, end_str = row
                
                try:
                    start_time = TimeUtils.parse_time(start_str)
                    end_time = TimeUtils.parse_time(end_str)
                    time_slot = TimeSlot(start_time, end_time)
                    event = Event(person.strip(), subject.strip(), time_slot)
                    events.append(event)
                except (InvalidCalendarFormatError, Exception) as e:
                    raise InvalidCalendarFormatError(f"Invalid data at line {line_num}: {e}") from e
        
        self._all_events = events
        logger.info("Loaded %d events from %s", len(events), self.csv_path)
        return events
    
    def get_events_by_person(self, person: str) -> List[Event]:
        """
        Get all events for a specific person.
        
        Args:
            person: Person name
            
        Returns:
            List of events for that person
        """
        if person not in self._cache:
            all_events = self.load_events()
            self._cache[person] = [e for e in all_events if e.person == person]
        
        return self._cache[person]
    
    def get_events_for_persons(self, persons: List[str]) -> List[Event]:
        """
        Get all events for a list of persons.
        
        Args:
            persons: List of person names
            
        Returns:
            Combined list of events for all persons
        """
        events = []
        for person in persons:
            events.extend(self.get_events_by_person(person))
        return events
