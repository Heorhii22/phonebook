import pytest
from pathlib import Path
from phonebook.cli import main


def test_add_and_list(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = str(tmp_path / "contacts.json")
    assert main(["--file", path, "add", "Anna", "08009006570"]) == 0
    assert main(["--file", path, "list"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Added Anna\nAnna: 08009006570\n"


def test_count_contacts(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = str(tmp_path / "contacts.json")
    main(["--file", path, "add", "Anna", "08009006570"])
    assert main(["--file", path, "count"]) == 0
    captured = capsys.readouterr()
    assert "Contacts: 1" in captured.out


def test_get_empty_phonebook(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "contacts.json"
    assert main(["--file", str(path), "list"]) == 0
    
    captured = capsys.readouterr()
    assert "Phonebook is empty" in captured.out


@pytest.mark.parametrize("name, phone",
                         [pytest.param("Anna", "abc", id="letters in phone"),
                         pytest.param("Anna", "050 002823", id="space in phone"),
                         pytest.param("Anna", "+3809474728", id="plus in phone"),
                         pytest.param("", "0590208201", id="empty name"),
                         pytest.param("Anna", "", id="empty phone")],)
def test_invalid_data_fails(tmp_path: Path,
                            capsys: pytest.CaptureFixture[str],
                            name: str,
                            phone: str,) -> None:
    path = tmp_path / "contacts.json"
    exit_code = main(["--file", str(path), "add", name, phone])
    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Error" in captured.err
    assert captured.out == ""
    assert not path.exists()


def test_find_contact(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = str(tmp_path / "contacts.json")
    main(["--file", path, "add", "Anna", "08009006570"])
    assert main(["--file", path, "find", "Anna"]) == 0
    captured = capsys.readouterr()
    assert captured.out == "Added Anna\n08009006570\n"


def test_find_by_not_existing_contact_name_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = str(tmp_path / "contacts.json")
    main(["--file", path, "add", "Anna", "08002387472"])
    exit_code = main(["--file", path, "find", "James"])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Error" in captured.err
    assert captured.out == "Added Anna\n"


def test_delete(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = str(tmp_path / "contacts.json")
    main(["--file", path, "add", "Anna", "08009006570"])
    assert main(["--file", path, "delete", "Anna"]) == 0
    assert main(["--file", path, "find", "Anna"]) == 1
    captured = capsys.readouterr()
    assert captured.out == "Added Anna\nDeleted Anna\n"
    assert "Error" in captured.err


def test_delete_non_existed_contact_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = str(tmp_path / "contacts.json")
    main(["--file", path, "add", "Derryl", "0904746812"])
    exit_code = main(["--file", path, "delete", "Anna"])
    assert exit_code == 1

    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_corrupted_file_fails(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path = tmp_path / "contacts.json"
    path.write_text("{corrupted file")
    exit_code = main(["--file", str(path), "add", "Anna", "09038413"])
    assert exit_code == 1
    
    captured = capsys.readouterr()
    assert "Error" in captured.err


def test_no_command_exits_with_code_2(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    path = tmp_path / "contacts.json"

    with pytest.raises(SystemExit) as info:
        main(["--file", str(path)])

    captured = capsys.readouterr()
    assert info.value.code == 2
    assert "usage" in captured.err




