import re

def get_video_duration(file_path):
    duration_pattern = re.compile(r"DURATION\s+:\s+(\d{2}:\d{2}:\d{2}\.\d+)")
    with open(file_path, 'r') as file:
        for line in file:
            match = duration_pattern.search(line)
            if match:
                return match.group(1)  # Return the first matching group, which is the duration
    return None  # Return None if no duration is found

def get_latest_time(file_path):
    time_pattern = re.compile(r"time=(\d{2}:\d{2}:\d{2}\.\d+)")
    latest_time = None
    with open(file_path, 'r') as file:
        for line in file:
            match = time_pattern.search(line)
            if match:
                latest_time = match.group(1)  # Update latest_time with the most recent match
    return latest_time  # Return the latest time found


if __name__ == "__main__":
    # Example usage
    # file_path = 'progress_output.txt'
    # duration = get_video_duration(file_path)
    # print(f"Duration: {duration}")

    file_path = 'progress_output.txt'
    latest_time = get_latest_time(file_path)
    print(f"Latest Time: {latest_time}")