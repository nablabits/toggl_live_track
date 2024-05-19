import os
from datetime import datetime, timezone

import requests

DEEP_WORK_TAG = "Deep Work"
DASH_TAGS = (
    "dash10", "dash20", "dash30", "dash60", "dash90"
)
BURST_TAG = "burst"


def get_data():
    """Connect to toggl API to fetch the ongoing time."""
    API_TOKEN = os.getenv("API_TOKEN")
    WORKSPACE_ID = os.getenv("WORKSPACE_ID")
    USER_AGENT = os.getenv("USER_AGENT")
    auth = (API_TOKEN, "api_token")
    params = {
        "user_agent": USER_AGENT,
        "workspace_id": WORKSPACE_ID,
    }
    url = "https://api.track.toggl.com/api/v9/me/time_entries/current"
    response = requests.get(url, params=params, auth=auth)
    json = response.json()
    return json


def elapsed(start):
    """Compute the elapsed time since the start hour."""
    dt = datetime.fromisoformat(start)
    delta = datetime.now(tz=timezone.utc) - dt
    hours = delta.seconds / 3600
    hour_part = int(hours)
    minute_part = int(60 * (hours - hour_part))
    return hour_part, minute_part


def shorten_string(input_string, max_length=50):
    if len(input_string) <= max_length:
        return input_string

    # Calculate the length of the portion to keep from the start and end.
    keep_length = (max_length - 3) // 2

    # Extract the start and end portions of the string
    start_part = input_string[:keep_length]
    end_part = input_string[-keep_length:]

    # Combine the start, ellipsis, and end parts
    shortened_string = f"{start_part} [...] {end_part}"
    return shortened_string


def run():
    """Main entry point."""
    data = get_data()
    if not data:
        print("· ⚠️  No tracking time")
        return
    start = data["start"]
    description = data.get("description", "No description")

    # Shorten it
    description = shorten_string(description)

    # Calculate elapsed time
    hour_part, minute_part = elapsed(start)

    # add a leading 0 for the first minutes of an hour
    if minute_part < 10:
        minute_part = f"0{minute_part}"

    # Classify the entry as deep work
    tags = data.get("tags", list())
    display = f"·  {description}: {hour_part}h {minute_part}'"
    if DEEP_WORK_TAG in tags:
        display += " [🎯 DEEP]"
    if BURST_TAG in tags:
        display += " [🔥 BURST]"
    for dash_tag in DASH_TAGS:
        if dash_tag in tags:
            display += f" [💫 {dash_tag}]".upper()
    print(display)


if __name__ == "__main__":
    run()
