# Smart Calendar Meeting Scheduler

A sophisticated calendar application that finds optimal meeting times for groups of people based on their availability and intelligent scoring criteria.

## Features

### Core Functionality
- **Availability Finding**: Identifies all available time slots when all participants are free
- **Smart Recommendations**: Scores and ranks time slots based on multiple criteria
- **Flexible Duration**: Supports any meeting duration
- **Working Hours**: Respects 07:00-19:00 working day constraints

### Intelligent Scoring System
The system evaluates each available time slot based on:

1. **Time of Day (25%)**: Morning slots score higher (peak productivity)
2. **Lunch Proximity (20%)**: Avoids lunch time (12:00-13:30)
3. **Slot Length (20%)**: Prefers longer slots (more flexibility)
4. **Position in Day (20%)**: Earlier slots leave more time for follow-up
5. **End of Day Buffer (15%)**: Avoids meetings ending too late

## Architecture

### Clean Architecture with SOLID Principles

```
io_comp/
├── models/                      # Domain Layer
│   ├── time_slot.py            # Immutable time interval
│   ├── event.py                # Calendar event
│   ├── meeting_preferences.py  # User preferences
│   └── scored_slot.py          # Scored recommendation
│
├── repositories/                # Data Layer
│   └── calendar_repository.py  # CSV data access with caching
│
├── services/                    # Business Logic Layer
│   ├── availability_service.py # Core availability algorithm
│   ├── recommendation_service.py # Main service facade
│   └── scoring/                # Scoring system
│       ├── base_scorer.py      # Abstract base class
│       ├── time_of_day_scorer.py
│       ├── lunch_scorer.py
│       ├── slot_length_scorer.py
│       ├── position_scorer.py
│       ├── end_of_day_scorer.py
│       └── composite_scorer.py # Combines all criteria
│
├── utils/                       # Utilities
│   ├── time_utils.py           # Time operations
│   └── formatters.py           # Output formatting
│
└── app.py                       # Entry point
```

### Design Patterns Used
- **Repository Pattern**: Separates data access from business logic
- **Strategy Pattern**: Pluggable scoring criteria
- **Composite Pattern**: Combines multiple scorers
- **Facade Pattern**: Simple interface to complex subsystem
- **Immutable Objects**: Thread-safe, predictable behavior

## Algorithm

### Availability Finding (O(n log n))
1. Load events for all participants
2. Extract time slots from events
3. Sort slots by start time
4. Merge overlapping/adjacent slots
5. Find gaps between merged slots
6. Filter gaps by minimum duration

### Scoring
Each available slot receives a weighted score (0-100) based on the five criteria above.

## Usage

### Basic Usage (Required API)
```python
from datetime import timedelta
from io_comp.app import find_available_slots

# Find available slots
person_list = ["Alice", "Jack"]
duration = timedelta(minutes=60)
slots = find_available_slots(person_list, duration)

# Returns: [time(7, 0), time(9, 40), time(14, 0), time(17, 0)]
```

### Advanced Usage (Smart Recommendations)
```python
from pathlib import Path
from datetime import timedelta
from io_comp.repositories.calendar_repository import CalendarRepository
from io_comp.services.recommendation_service import RecommendationService
from io_comp.utils.formatters import ResultFormatter

# Setup
csv_path = Path("resources/calendar.csv")
repository = CalendarRepository(csv_path)
service = RecommendationService(repository)
formatter = ResultFormatter()

# Find best slots
person_list = ["Alice", "Jack"]
duration = timedelta(minutes=60)
results = service.find_best_slots(person_list, duration, top_n=3)

# Display
output = formatter.format_scored_slots(results)
print(output)
```

### Running the Demo
```bash
py -m io_comp.app
```

## Testing

### Run All Tests
```bash
py -m pytest tests/ -v
```

### Test Coverage
- **Unit Tests**: TimeSlot, Event models
- **Service Tests**: Availability finding, scoring logic
- **Integration Tests**: End-to-end workflow
- **Edge Cases**: No availability, tight fits, overlapping events

### Example Test Results
```
11 tests passed in 0.26s
- TimeSlot validation and operations
- Availability finding (including README example)
- Scoring and recommendations
- Full integration workflow
```

## Example Output

```
============================================================
Smart Calendar Meeting Scheduler
============================================================

Example: Finding meeting time for Alice & Jack (60 minutes)

Best Meeting Times:

[BEST] #1: 07:00-08:00 (Score: 90/100 - Excellent)
   [Time of Day] + Early morning - high energy
   [Lunch Proximity] + Not during lunch time
   [Slot Length] ~ Tight fit (60 min)
   [Position in Day] + Early in day - plenty of time after
   [End of Day Buffer] + Ends with time to spare

[BEST] #2: 09:40-13:00 (Score: 85/100 - Excellent)
   [Time of Day] + Morning - productive time
   [Lunch Proximity] ~ Partially overlaps lunch time
   [Slot Length] + Long slot (200 min) - very flexible
   [Position in Day] + Early in day - plenty of time after
   [End of Day Buffer] + Ends with time to spare

[BEST] #3: 14:00-16:00 (Score: 80/100 - Excellent)
   [Time of Day] + Early afternoon
   [Lunch Proximity] + Not during lunch time
   [Slot Length] + Long slot (120 min) - very flexible
   [Position in Day] ~ Mid-afternoon
   [End of Day Buffer] + Ends with time to spare
```

## CSV Format

```csv
Person name,Event subject,Event start time,Event end time
Alice,"Morning meeting",08:00,09:30
Alice,"Lunch with Jack",13:00,14:00
```

## Extensibility

### Adding New Scoring Criteria
```python
from io_comp.services.scoring.base_scorer import BaseScorer

class CustomScorer(BaseScorer):
    @property
    def weight(self) -> float:
        return 0.1  # 10% of total score
    
    @property
    def name(self) -> str:
        return "Custom Criterion"
    
    def score(self, slot, duration, preferences):
        # Your logic here
        return score, reason
```

### Future Enhancements
- Multi-day support
- Room allocation
- Priority-based scheduling
- Conflict resolution suggestions
- Integration with external calendars

## Requirements

- Python 3.7+
- pytest (for testing)

## Key Decisions

1. **Immutable Models**: TimeSlot and Event are frozen dataclasses for thread-safety
2. **Weighted Scoring**: Allows fine-tuning of criteria importance
3. **Caching**: Repository caches loaded events to avoid repeated file reads
4. **Separation of Concerns**: Clear boundaries between layers
5. **Testability**: Each component can be tested independently

## Performance

- **Time Complexity**: O(n log n) for availability finding (dominated by sorting)
- **Space Complexity**: O(n) for storing events and slots
- **Caching**: O(1) lookup for repeated person queries

## Author

Created as part of Comp.io coding evaluation.
