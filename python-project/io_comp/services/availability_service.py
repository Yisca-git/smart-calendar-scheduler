"""Service for finding available time slots"""

from typing import List
from datetime import time, timedelta
from ..models.time_slot import TimeSlot
from ..repositories.calendar_repository import CalendarRepository


class AvailabilityService:
    """
    Service for finding available time slots.
    
    Implements the core algorithm for finding gaps in schedules.
    """
    
    WORK_DAY_START = time(7, 0)
    WORK_DAY_END = time(19, 0)
    
    def __init__(self, repository: CalendarRepository):
        """
        Initialize service with a calendar repository.
        
        Args:
            repository: Calendar data repository
        """
        self.repository = repository
    
    def find_available_slots(
        self, 
        person_list: List[str], 
        event_duration: timedelta
    ) -> List[TimeSlot]:
        """
        Find all available time slots for a list of persons.
        
        Algorithm:
        1. Load events for all persons
        2. Extract time slots from events
        3. Merge overlapping/adjacent slots
        4. Find gaps between merged slots
        5. Filter gaps by minimum duration
        
        Args:
            person_list: List of person names who need to attend
            event_duration: Required duration for the meeting
            
        Returns:
            List of available time slots that fit the duration
        """
        # Load events for all persons
        events = self.repository.get_events_for_persons(person_list)
        
        # Extract time slots
        busy_slots = [event.time_slot for event in events]
        
        # Merge overlapping slots
        merged_busy = self._merge_overlapping_slots(busy_slots)
        
        # Find gaps
        free_slots = self._find_gaps(merged_busy)
        
        # Filter by duration
        return [slot for slot in free_slots if slot.contains_duration(event_duration)]
    
    def _merge_overlapping_slots(self, slots: List[TimeSlot]) -> List[TimeSlot]:
        """
        Merge overlapping or adjacent time slots.
        
        Args:
            slots: List of time slots to merge
            
        Returns:
            List of merged time slots (non-overlapping)
        """
        if not slots:
            return []
        
        # Sort by start time
        sorted_slots = sorted(slots, key=lambda s: s.start_time)
        
        merged = [sorted_slots[0]]
        
        for current in sorted_slots[1:]:
            last = merged[-1]
            
            if last.overlaps(current) or last.is_adjacent(current):
                # Merge with last slot
                merged[-1] = last.merge(current)
            else:
                # Add as new slot
                merged.append(current)
        
        return merged
    
    def _find_gaps(self, busy_slots: List[TimeSlot]) -> List[TimeSlot]:
        """
        Find gaps between busy slots within working hours.
        
        Args:
            busy_slots: List of busy time slots (should be merged and sorted)
            
        Returns:
            List of free time slots (gaps)
        """
        if not busy_slots:
            # Entire day is free
            return [TimeSlot(self.WORK_DAY_START, self.WORK_DAY_END)]
        
        gaps = []
        
        # Gap before first event
        first_slot = busy_slots[0]
        if self.WORK_DAY_START < first_slot.start_time:
            gaps.append(TimeSlot(self.WORK_DAY_START, first_slot.start_time))
        
        # Gaps between events
        for i in range(len(busy_slots) - 1):
            current_end = busy_slots[i].end_time
            next_start = busy_slots[i + 1].start_time
            
            if current_end < next_start:
                gaps.append(TimeSlot(current_end, next_start))
        
        # Gap after last event
        last_slot = busy_slots[-1]
        if last_slot.end_time < self.WORK_DAY_END:
            gaps.append(TimeSlot(last_slot.end_time, self.WORK_DAY_END))
        
        return gaps
