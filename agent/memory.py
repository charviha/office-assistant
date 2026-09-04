import json
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# File used for long-term memory
MEMORY_FILE = BASE_DIR / "data" / "memory.json"


def save_memory(memory_item):
    """
    Save an important piece of information to long-term memory.
    """

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load existing memories
    if MEMORY_FILE.exists():
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            memories = json.load(f)
    else:
        memories = []

    # Add new memory
    memories.append(memory_item)

    # Save updated memories
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memories, f, indent=2, ensure_ascii=False)


def load_memories():
    """
    Load all long-term memories.
    """

    if not MEMORY_FILE.exists():
        return []

    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def clear_memories():
    """
    Delete all long-term memories.
    """

    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()


class ShortTermMemory:
    """
    Stores the conversation history during the current session.
    """

    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({
            "role": role,
            "content": content
        })

    def get_messages(self):
        return self.messages

    def clear(self):
        self.messages = []
