"""
Calendar Application - Entry Point

This application finds the best meeting times for a group of people
based on their calendar availability and intelligent scoring.
"""

from pathlib import Path
from datetime import timedelta
from typing import List

from .repositories.calendar_repository import CalendarRepository
from .services.recommendation_service import RecommendationService
from .utils.formatters import ResultFormatter


def find_available_slots(person_list: List[str], event_duration: timedelta) -> List:
    """
    Find available time slots for a list of persons.
    
    This is the main function as specified in the requirements.
    
    Args:
        person_list: List of person names who need to attend
        event_duration: Required duration for the meeting
        
    Returns:
        List of start times for available slots
    """
    csv_path = Path(__file__).parent.parent / "resources" / "calendar.csv"
    repository = CalendarRepository(csv_path)
    service = RecommendationService(repository)
    
    return service.find_available_slots(person_list, event_duration)


def main():
    """Main entry point demonstrating the calendar system"""
    
    print("\n" + "="*60)
    print("Smart Calendar Meeting Scheduler")
    print("="*60 + "\n")
    
    # Setup
    csv_path = Path(__file__).parent.parent / "resources" / "calendar.csv"
    repository = CalendarRepository(csv_path)
    service = RecommendationService(repository)
    formatter = ResultFormatter()
    
    # Example from README: Alice & Jack, 60 minutes
    print("Example: Finding meeting time for Alice & Jack (60 minutes)\n")
    
    person_list = ["Alice", "Jack"]
    duration = timedelta(minutes=60)
    
    # Find best slots with scoring
    results = service.find_best_slots(person_list, duration, top_n=3)
    
    # Display results
    output = formatter.format_scored_slots(results)
    print(output)
    
    print("\n" + "="*60)
    print("Calendar system ready!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
