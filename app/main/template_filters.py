"""Custom template filters for the main blueprint."""

from datetime import datetime, timedelta

from .views import main_bp

@main_bp.app_template_filter('date_from_iso')
def date_from_iso(iso: datetime) -> str:
    """Converts date to a string in the format DDD, DD MMM"""

    return (iso + timedelta(hours=8)).strftime('%a, %d %b')

@main_bp.app_template_filter('time_from_iso')
def time_from_iso(iso: datetime) -> str:
    """Converts time to a string in the format HH:MM:SS"""

    return (iso + timedelta(hours=8)).strftime('%H:%M:%S')
