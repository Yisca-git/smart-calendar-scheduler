"""Work day configuration constants"""

from datetime import time


class WorkDayConfig:
    START = time(7, 0)
    END = time(19, 0)

    EARLY_MORNING_END = time(9, 0)
    MORNING_END = time(12, 0)
    LUNCH_END = time(14, 0)
    EARLY_AFTERNOON_END = time(16, 0)

    END_OF_DAY_BUFFER = time(17, 0)
    END_OF_DAY_LATE = time(18, 0)
