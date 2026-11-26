import json
from pathlib import Path

from phonebook.errors import StorageError


def load_contacts(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    try:
        with open(path, encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as error:
        raise StorageError(f"File {path} is corrupted") from error

    if not isinstance(data, dict):
        raise StorageError(f"File {path} must contain an object")
    return data

def save_contacts(path: Path, contacts: dict[str, str]) -> None:
    """Save data tool on add, delete or update"""
    with open(path, "w", encoding="utf-8") as file:
        json.dump(contacts, file, ensure_ascii=False, indent=2)