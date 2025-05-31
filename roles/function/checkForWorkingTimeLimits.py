from datetime import datetime, time
def checkWorkingTimeLimits(workingTimeLimit : str , workingDayLimit : list[int]) -> bool:
    """ check if the current time is within the working time limits and the current day is within the working day limits """
    # Get the current time and day
    current_time = datetime.now().time()
    current_day = datetime.now().weekday()

    # Parse the working time limits
    start_time_str, end_time_str = workingTimeLimit.split("-")
    start_time = datetime.strptime(start_time_str, "%H:%M").time()
    end_time = datetime.strptime(end_time_str, "%H:%M").time()
    
    # Check if the current day is within the working day limits
    if current_day not in workingDayLimit:
        return False
    
    # Check if the current time is within the working time limits
    if start_time <= current_time <= end_time:
        return True
    
    return False
