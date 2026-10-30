import json
from datetime import datetime
from pathlib import Path
from typing import Any

# from memory import summarize_current_chat

# the filing cabinet: a data folder next to our code, where long-term memory lives
DATA_FOLDER = Path("data")

# facts about the user, like their name or where they live
FACTS_FILE = DATA_FOLDER / "facts.json"

# what the user likes, like Fahrenheit or the stocks they follow
PREFERENCES_FILE = DATA_FOLDER / "preferences.json"

# facts and preferences that changed: we keep the old value here, so we know what used to be true
OLD_FACTS_FILE = DATA_FOLDER / "old_facts.json"

# a short summary of the last chat
CHAT_SUMMARY_FILE = DATA_FOLDER / "chat_summary.json"

# how to do things, like the morning briefing, one file per routine, written in plain English
ROUTINES_FOLDER = Path("routines")


## utility methods
# we read a JSON file, or return the default if it doesn't exist yet
# (Any means it can be any type: a dict for facts, a list for old_facts)
def read_json(file: Path, default: Any) -> Any:
    if not file.exists():
        return default
    return json.loads(file.read_text())


# we make sure the data folder exists, then write the JSON file
def write_json(file: Path, data: Any) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(json.dumps(data, indent=2, ensure_ascii=False))


# this is a generic method to store a fact or preference; the file name is passed in
# facts and preferences are saved the same way,
# only the file name is different
# if an incoming value is different from the old one, we keep the old value in the history
# inside the old facts json file
def store(file: Path, memory_type: str, key: str, value: str) -> dict:
    saved = read_json(file, {})
    old_value = saved.get(key)

    # the value changed, for example the user moved: we keep the old value in the history
    if old_value and old_value != value:
        keep_old_value(memory_type, key, old_value, value)

    saved[key] = value
    write_json(file, saved)
    return {"saved": key, "value": value, "old_value": old_value}


# we save one fact about the user;
# the same key again replaces the old value
def store_facts(key: str, value: str) -> dict:
    return store(FACTS_FILE, "fact", key, value)


# we save one preference of the user;
# the same key again replaces the old value
def store_preferences(key: str, value: str) -> dict:
    return store(PREFERENCES_FILE, "preference", key, value)


# we read the facts about the user
# (nothing saved yet means an empty dict)
def load_facts() -> dict:
    return read_json(FACTS_FILE, {})


# we read the user's preferences
# (nothing saved yet means an empty dict)
def load_preferences() -> dict:
    return read_json(PREFERENCES_FILE, {})


# we read every routine in the routines folder
def load_routines() -> str:
    routines = ""
    for routine_file in sorted(ROUTINES_FOLDER.glob("*.md")):
        routines += routine_file.read_text() + "\n"
    return routines


# we save the summary of the chat that just ended,
# with the date (only the last chat, for now)
def store_chat_summary(summary: str) -> None:
    chat = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": summary,
    }
    write_json(CHAT_SUMMARY_FILE, chat)
    print("Saved this chat:", summary)


# we read the summary of the last chat
# (nothing saved yet means None)
def get_chat_summary() -> dict | None:
    return read_json(CHAT_SUMMARY_FILE, None)


# we add the old value to the history file, with the date it changed
def keep_old_value(memory_type: str, key: str, old_value: str, new_value: str) -> None:
    old_facts = read_json(OLD_FACTS_FILE, [])
    old_facts.append(
        {
            "type": memory_type,
            "key": key,
            "old_value": old_value,
            "new_value": new_value,
            "changed_on": datetime.now().strftime("%Y-%m-%d"),
        }
    )
    write_json(OLD_FACTS_FILE, old_facts)
