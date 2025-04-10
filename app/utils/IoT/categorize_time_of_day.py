def categorize_time_of_day(hour: int) -> str:
    if 5 <= hour < 9:
        return 'morning'
    elif 9 <= hour < 12:
        return 'afternoon'
    elif 12 <= hour < 17:
        return 'evening'
    elif 17 <= hour < 21:
        return 'early_night'
    else:
        return 'late_night'
