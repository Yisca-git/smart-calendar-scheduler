# 🗓️ Smart Calendar Scheduler

An intelligent meeting scheduler that finds optimal time slots based on availability and smart scoring criteria.

**Created as part of Comp.io coding evaluation.**

---

## ✨ Features

### Core Functionality
- **Availability Finding**: Identifies all available time slots when all participants are free
- **Smart Recommendations**: Scores and ranks time slots based on multiple criteria
- **Flexible Duration**: Supports any meeting duration
- **Working Hours**: Respects 07:00-19:00 working day constraints

### Intelligent Scoring System
The system evaluates each available time slot based on five weighted criteria:

1. **Time of Day (25%)**: Morning slots score higher (peak productivity)
2. **Lunch Proximity (20%)**: Avoids lunch time (12:00-13:30)
3. **Slot Length (20%)**: Prefers longer slots (more flexibility)
4. **Position in Day (20%)**: Earlier slots leave more time for follow-up
5. **End of Day Buffer (15%)**: Avoids meetings ending too late

---

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- pytest (for testing)

### Installation

```bash
# Clone the repository
git clone https://github.com/Yisca-git/smart-calendar-scheduler.git
cd smart-calendar-scheduler

# Install dependencies
pip install -r requirements.txt
```

### Running the Application

```bash
# Run the demo
py -m io_comp.app
```

### Running Tests

```bash
# Run all tests
py -m pytest tests/ -v

# Run with coverage
py -m pytest tests/ -v --cov=io_comp
```

---

## 📊 Example Output

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

---

## 🏗️ Architecture

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

---

## 🔍 Core Algorithm

### Availability Finding Algorithm (O(n log n))

1. **Load events** for all participants from CSV
2. **Extract time slots** from events (busy times)
3. **Sort slots** by start time
4. **Merge overlapping/adjacent** slots into continuous busy periods
5. **Find gaps** between busy periods within working hours (07:00-19:00)
6. **Filter gaps** that are large enough for the requested duration

### Scoring Algorithm

Each available slot receives a weighted score (0-100) based on 5 criteria:
- Time of Day (25%), Lunch Proximity (20%), Slot Length (20%), Position in Day (20%), End of Day Buffer (15%)

---

## 💻 Usage

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

---

## 🧪 Testing

### Test Coverage

The project includes comprehensive tests covering:

- **Unit Tests**: TimeSlot, Event models
- **Service Tests**: Availability finding, scoring logic
- **Integration Tests**: End-to-end workflow
- **Edge Cases**: No availability, tight fits, overlapping events

### Test Results

```
============================= test session starts =============================
collected 11 items

tests/test_app.py::TestTimeSlot::test_valid_time_slot PASSED           [  9%]
tests/test_app.py::TestTimeSlot::test_invalid_time_slot PASSED         [ 18%]
tests/test_app.py::TestTimeSlot::test_duration_calculation PASSED      [ 27%]
tests/test_app.py::TestTimeSlot::test_overlaps PASSED                  [ 36%]
tests/test_app.py::TestTimeSlot::test_merge PASSED                     [ 45%]
tests/test_app.py::TestAvailabilityService::test_find_available_slots_example_from_readme PASSED [ 54%]
tests/test_app.py::TestAvailabilityService::test_no_common_availability PASSED [ 63%]
tests/test_app.py::TestAvailabilityService::test_merge_overlapping_slots PASSED [ 72%]
tests/test_app.py::TestRecommendationService::test_find_best_slots_returns_scored_results PASSED [ 81%]
tests/test_app.py::TestRecommendationService::test_morning_slots_score_higher PASSED [ 90%]
tests/test_app.py::TestIntegration::test_full_workflow PASSED          [100%]

============================== 11 passed in 0.26s ==============================
```

---

## 📈 Algorithm Complexity

### Availability Finding
- **Sorting**: O(n log n)
- **Merging overlapping slots**: O(n)
- **Finding gaps**: O(n)
- **Total**: O(n log n) - Optimal!

### Scoring
- **Per slot**: O(k) where k = number of criteria (5)
- **All slots**: O(n × k)

---

## 🎯 Key Design Decisions

1. **Immutable Models**: TimeSlot and Event are frozen dataclasses for thread-safety
2. **Weighted Scoring**: Allows fine-tuning of criteria importance
3. **Caching**: Repository caches loaded events to avoid repeated file reads
4. **Separation of Concerns**: Clear boundaries between layers
5. **Testability**: Each component can be tested independently

---

## 🔧 CSV Format

```csv
Person name,Event subject,Event start time,Event end time
Alice,"Morning meeting",08:00,09:30
Alice,"Lunch with Jack",13:00,14:00
Jack,"Morning meeting",08:00,08:50
```

---

## 🚀 Extensibility

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
- Integration with external calendars (Google Calendar, Outlook)
- Time zone support
- Recurring meetings

---

## 📚 Project Structure

```
python-project/
├── io_comp/                    # Main package
│   ├── models/                 # Domain models
│   ├── repositories/           # Data access
│   ├── services/               # Business logic
│   ├── utils/                  # Utilities
│   └── app.py                  # Entry point
├── resources/                  # Data files
│   └── calendar.csv
├── tests/                      # Test suite
│   └── test_app.py
├── requirements.txt            # Dependencies
└── README.md                   # This file
```

---

## 🛠️ Tech Stack

- **Language**: Python 3.7+
- **Testing**: pytest
- **Architecture**: Clean Architecture, SOLID principles
- **Design Patterns**: Repository, Strategy, Composite, Facade

---

## 📝 Requirements Met

This project fulfills all requirements from the Comp.io coding evaluation:

✅ Find available time slots for multiple persons  
✅ Support custom event duration  
✅ Respect working hours (07:00-19:00)  
✅ Object-oriented design with SOLID principles  
✅ Meaningful naming conventions  
✅ Comprehensive test coverage (2-3+ important tests)  
✅ Clean, maintainable, and extensible code  

**Bonus**: Smart scoring system for optimal meeting time recommendations

---

## 👤 Author

Created as part of **Comp.io coding evaluation**.

---

## 📄 License

This project was created for educational and evaluation purposes.

---

## 🙏 Acknowledgments

- Comp.io for the interesting coding challenge
- The challenge provided an excellent opportunity to demonstrate clean architecture and thoughtful design

---

## 📞 Contact

For questions or feedback about this implementation, please reach out through the evaluation process.
