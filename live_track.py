import os
from datetime import datetime, timezone

import requests

DEEP_WORK_TAG = "Deep Work"


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
    url = "https://api.track.toggl.com/api/v8/time_entries/current"
    response = requests.get(url, params=params, auth=auth)
    json = response.json()
    return json["data"]


def elapsed(start):
    """Compute the elapsed time since the start hour."""
    dt = datetime.fromisoformat(start)
    delta = datetime.now(tz=timezone.utc) - dt
    hours = delta.seconds / 3600
    hour_part = int(hours)
    minute_part = int(60 * (hours - hour_part))
    return hour_part, minute_part


def run():
    """Main entry point."""
    data = get_data()
    if not data:
        print("· ⚠️  No tracking time")
        return
    start = data["start"]
    description = data.get("description", "No description")

    # Calculate elapsed time
    hour_part, minute_part = elapsed(start)

    # add a leading 0 for the first minutes of an hour
    if minute_part < 10:
        minute_part = f"0{minute_part}"

    # Classify the entry as deep work
    tags = data.get("tags", list())
    if DEEP_WORK_TAG in tags:
        print(f"· [🎯 Focusing] {description}: {hour_part}h {minute_part}'")
    else:
        print(f"· ⌛ {description}: {hour_part}h {minute_part}'")


if __name__ == "__main__":
    run()
