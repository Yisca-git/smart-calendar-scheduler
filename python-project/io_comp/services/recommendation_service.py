"""Service for recommending best meeting times"""

from typing import List
from datetime import timedelta
from ..models.meeting_preferences import MeetingPreferences
from ..models.scored_slot import ScoredSlot
from ..repositories.calendar_repository import CalendarRepository
from .availability_service import AvailabilityService
from .scoring.composite_scorer import CompositeScorer
from .scoring.time_of_day_scorer import TimeOfDayScorer
from .scoring.lunch_scorer import LunchScorer
from .scoring.slot_length_scorer import SlotLengthScorer
from .scoring.position_scorer import PositionScorer
from .scoring.end_of_day_scorer import EndOfDayScorer


class RecommendationService:
    """
    Service for finding and scoring the best meeting times.
    
    Combines availability finding with intelligent scoring.
    """
    
    def __init__(self, repository: CalendarRepository):
        """
        Initialize service with a calendar repository.
        
        Args:
            repository: Calendar data repository
        """
        self.availability_service = AvailabilityService(repository)
        self.scorer = self._create_scorer()
    
    def _create_scorer(self) -> CompositeScorer:
        """Create composite scorer with all criteria"""
        return CompositeScorer([
            TimeOfDayScorer(),
            LunchScorer(),
            SlotLengthScorer(),
            PositionScorer(),
            EndOfDayScorer()
        ])
    
    def find_best_slots(
        self,
        person_list: List[str],
        event_duration: timedelta,
        preferences: MeetingPreferences = None,
        top_n: int = 3
    ) -> List[ScoredSlot]:
        """
        Find the best meeting times for a list of persons.
        
        Args:
            person_list: List of person names who need to attend
            event_duration: Required duration for the meeting
            preferences: Meeting preferences (optional, uses defaults if None)
            top_n: Number of top results to return
            
        Returns:
            List of scored slots, sorted by score (best first)
        """
        if preferences is None:
            preferences = MeetingPreferences.default()
        
        # Find available slots
        available_slots = self.availability_service.find_available_slots(
            person_list, 
            event_duration
        )
        
        if not available_slots:
            return []
        
        # Score each slot
        scored_slots = [
            self.scorer.score_slot(slot, event_duration, preferences)
            for slot in available_slots
        ]
        
        # Sort by score (descending)
        scored_slots.sort(key=lambda s: s.score, reverse=True)
        
        # Return top N
        return scored_slots[:top_n]
    
    def find_available_slots(
        self,
        person_list: List[str],
        event_duration: timedelta
    ) -> List[timedelta]:
        """
        Basic function matching the required signature.
        
        This is the function specified in the requirements.
        Returns start times of available slots.
        
        Args:
            person_list: List of person names
            event_duration: Required duration
            
        Returns:
            List of start times (as time objects)
        """
        slots = self.availability_service.find_available_slots(
            person_list,
            event_duration
        )
        return [slot.start_time for slot in slots]
