"""
Unit tests for Comp calendar scheduler
"""

import pytest
from datetime import time, timedelta
from typing import List

from io_comp.models.time_slot import TimeSlot
from io_comp.models.event import Event
from io_comp.repositories.calendar_repository_base import CalendarRepositoryBase
from io_comp.services.availability_service import AvailabilityService
from io_comp.services.recommendation_service import RecommendationService


ALICE_EVENTS = [
    Event("Alice", "Morning meeting", TimeSlot(time(8, 0), time(9, 30))),
    Event("Alice", "Lunch with Jack", TimeSlot(time(13, 0), time(14, 0))),
    Event("Alice", "Yoga", TimeSlot(time(16, 0), time(17, 0))),
]

JACK_EVENTS = [
    Event("Jack", "Morning meeting", TimeSlot(time(8, 0), time(8, 50))),
    Event("Jack", "Sales call", TimeSlot(time(9, 0), time(9, 40))),
    Event("Jack", "Lunch with Alice", TimeSlot(time(13, 0), time(14, 0))),
    Event("Jack", "Yoga", TimeSlot(time(16, 0), time(17, 0))),
]

BOB_EVENTS = [
    Event("Bob", "Morning meeting", TimeSlot(time(8, 0), time(9, 30))),
    Event("Bob", "Morning meeting 2", TimeSlot(time(9, 30), time(9, 40))),
    Event("Bob", "Q3 review", TimeSlot(time(10, 0), time(11, 30))),
    Event("Bob", "Lunch and siesta", TimeSlot(time(13, 0), time(15, 0))),
    Event("Bob", "Yoga", TimeSlot(time(16, 0), time(17, 0))),
]

ALL_EVENTS = ALICE_EVENTS + JACK_EVENTS + BOB_EVENTS


class FakeCalendarRepository(CalendarRepositoryBase):
    """In-memory repository for testing"""

    def __init__(self, events: List[Event]):
        self._events = events

    def get_events_for_persons(self, persons: List[str]) -> List[Event]:
        return [e for e in self._events if e.person in persons]


@pytest.fixture
def repository():
    return FakeCalendarRepository(ALL_EVENTS)


@pytest.fixture
def availability_service(repository):
    return AvailabilityService(repository)


@pytest.fixture
def recommendation_service(repository):
    return RecommendationService(repository)


class TestTimeSlot:
    """Test TimeSlot model"""
    
    def test_valid_time_slot(self):
        """Test creating a valid time slot"""
        slot = TimeSlot(time(9, 0), time(10, 0))
        assert slot.start_time == time(9, 0)
        assert slot.end_time == time(10, 0)
    
    def test_invalid_time_slot(self):
        """Test that invalid time slot raises error"""
        from io_comp.utils.exceptions import InvalidTimeSlotError
        with pytest.raises(InvalidTimeSlotError):
            TimeSlot(time(10, 0), time(9, 0))
    
    def test_duration_calculation(self):
        """Test duration calculation"""
        slot = TimeSlot(time(9, 0), time(10, 30))
        assert slot.duration_minutes() == 90
    
    def test_overlaps(self):
        """Test overlap detection"""
        slot1 = TimeSlot(time(9, 0), time(10, 0))
        slot2 = TimeSlot(time(9, 30), time(10, 30))
        assert slot1.overlaps(slot2)
        assert slot2.overlaps(slot1)
    
    def test_merge(self):
        """Test merging overlapping slots"""
        slot1 = TimeSlot(time(9, 0), time(10, 0))
        slot2 = TimeSlot(time(9, 30), time(11, 0))
        merged = slot1.merge(slot2)
        assert merged.start_time == time(9, 0)
        assert merged.end_time == time(11, 0)


class TestAvailabilityService:
    """Test availability finding logic"""
    
    def test_find_available_slots_example_from_readme(self, availability_service):
        """Test the exact example from README: Alice & Jack, 60 minutes"""
        person_list = ["Alice", "Jack"]
        duration = timedelta(minutes=60)
        
        slots = availability_service.find_available_slots(person_list, duration)
        
        # Expected slots from README:
        # 07:00-07:00 (too short, filtered out)
        # 09:40-13:00 (valid)
        # 14:00-16:00 (valid)
        # 17:00-19:00 (valid)
        
        assert len(slots) >= 3
        
        # Check that we have the expected slots
        start_times = [slot.start_time for slot in slots]
        assert time(9, 40) in start_times
        assert time(14, 0) in start_times
        assert time(17, 0) in start_times
    
    def test_no_common_availability(self, availability_service):
        """Test when all persons are busy all day"""
        # Alice, Jack, and Bob together have very limited availability
        person_list = ["Alice", "Jack", "Bob"]
        duration = timedelta(minutes=180)  # 3 hours - too long
        
        slots = availability_service.find_available_slots(person_list, duration)
        
        # Should have very few or no slots for 3 hours
        assert len(slots) <= 1
    
    def test_merge_overlapping_slots(self, availability_service):
        """Test that overlapping slots are merged correctly"""
        slots = [
            TimeSlot(time(8, 0), time(9, 0)),
            TimeSlot(time(8, 30), time(10, 0)),
            TimeSlot(time(11, 0), time(12, 0))
        ]
        
        merged = availability_service._merge_overlapping_slots(slots)
        
        assert len(merged) == 2
        assert merged[0].start_time == time(8, 0)
        assert merged[0].end_time == time(10, 0)
        assert merged[1].start_time == time(11, 0)
        assert merged[1].end_time == time(12, 0)


class TestRecommendationService:
    """Test recommendation and scoring logic"""
    
    def test_find_best_slots_returns_scored_results(self, recommendation_service):
        """Test that best slots are scored and sorted"""
        person_list = ["Alice", "Jack"]
        duration = timedelta(minutes=60)
        
        results = recommendation_service.find_best_slots(person_list, duration, top_n=3)
        
        assert len(results) > 0
        assert len(results) <= 3
        
        # Check that results are sorted by score (descending)
        for i in range(len(results) - 1):
            assert results[i].score >= results[i + 1].score
        
        # Check that scores are in valid range
        for result in results:
            assert 0 <= result.score <= 100
            assert len(result.reasons) > 0
    
    def test_morning_slots_score_higher(self, recommendation_service):
        """Test that morning slots generally score higher than late afternoon"""
        person_list = ["Alice", "Jack"]
        duration = timedelta(minutes=60)
        
        results = recommendation_service.find_best_slots(person_list, duration, top_n=5)
        
        # Find morning and late afternoon slots
        morning_slots = [r for r in results if r.start_time.hour < 12]
        afternoon_slots = [r for r in results if r.start_time.hour >= 16]
        
        if morning_slots and afternoon_slots:
            avg_morning = sum(s.score for s in morning_slots) / len(morning_slots)
            avg_afternoon = sum(s.score for s in afternoon_slots) / len(afternoon_slots)
            assert avg_morning > avg_afternoon


class TestIntegration:
    """Integration tests"""

    def test_full_workflow(self, repository):
        """Test complete workflow from events to recommendations"""
        events = repository.get_events_for_persons(["Alice", "Jack"])
        assert len(events) > 0

        availability_service = AvailabilityService(repository)
        slots = availability_service.find_available_slots(
            ["Alice", "Jack"],
            timedelta(minutes=60)
        )
        assert len(slots) > 0

        recommendation_service = RecommendationService(repository)
        results = recommendation_service.find_best_slots(
            ["Alice", "Jack"],
            timedelta(minutes=60)
        )
        assert len(results) > 0
        assert results[0].score > 0
