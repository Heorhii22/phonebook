from pathlib import Path

import pytest
from phonebook.errors import StorageError
from phonebook.storage import save_contacts, load_contacts


def test_save_and_load_contacts(tmp_path: Path) -> None:
    path = tmp_path / "contacts.json"
    contacts = {"Анна": "18004023", "Боб": "18904565"}

    save_contacts(path, contacts)
    
    assert load_contacts(path) == contacts

def test_load_missing_file_returns_empty_dict(tmp_path: Path) -> None:
    path = tmp_path / "contacts.json"

    assert load_contacts(path) == {}

def test_load_corrupted_file_raises(tmp_path: Path) -> None:
    path = tmp_path / "contacts.json"
    path.write_text("corrupted}", encoding="utf-8")

    with pytest.raises(StorageError, match="corrupted"):
        load_contacts(path)

def test_load_file_with_list_raises(tmp_path: Path) -> None:
    path = tmp_path / "contacts.json"
    path.write_text('["Anna", "0501234567"]', encoding="utf-8")

    with pytest.raises(StorageError, match="must contain an object"):
        load_contacts(path)