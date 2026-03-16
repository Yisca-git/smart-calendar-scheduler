"""Domain-specific exceptions for the calendar application"""


class CalendarException(Exception):
    """Base exception for all calendar domain errors"""


class CalendarFileNotFoundError(CalendarException):
    """Raised when the calendar CSV file does not exist"""


class InvalidCalendarFormatError(CalendarException):
    """Raised when the CSV file has an invalid format"""


class InvalidTimeFormatError(CalendarException):
    """Raised when a time string cannot be parsed"""


class InvalidTimeSlotError(CalendarException):
    """Raised when a time slot has invalid start/end times"""
