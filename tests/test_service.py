import pytest

from phonebook.errors import ContactNotFoundError
from phonebook.service import add_contact, find_contact, delete_contact


@pytest.fixture
def sample_contacts() -> dict[str, str]:
    return {"Anna": "08934847271", "Eduard": "0828020202"}


@pytest.mark.parametrize(("contacts, name, phone, expected"),
                         [
                             ({}, "Anna", "09008005643", {"Anna": "09008005643"}),
                             ({"Anna": "09008005643"}, "Bob", "08004035742", {"Anna": "09008005643",
                                                                               "Bob":"08004035742"})
                         ])
def test_add_contact(contacts: dict[str, str], 
                     name: str, 
                     phone: str, 
                     expected: dict[str, str]) -> None:
    
    add_contact(contacts, name, phone)

    assert contacts == expected


@pytest.mark.parametrize(("name", "phone", "message"),
                         [
                             ("", "0843018392", "Unacceptable contact name."),
                             ("Rachel", "vodiwvnwod", "only numbers"),
                             ("Rachel", "", "only numbers"),
                         ])
def test_add_contact_with_non_valid_data_raises(sample_contacts: dict[str, str], 
                                                name: str, 
                                                phone: str, 
                                                message: str) -> None:
    before = dict(sample_contacts)

    with pytest.raises(ValueError, match=message):
        add_contact(sample_contacts, name, phone)

    assert sample_contacts == before


def test_find_contact_by_name(sample_contacts: dict[str, str]) -> None:
    assert find_contact(sample_contacts, "Anna") == "08934847271"


def test_find_non_existed_contact_raises(sample_contacts: dict[str, str]) -> None:
    with pytest.raises(ContactNotFoundError, match="Unable to find contact"):
        find_contact(sample_contacts, "James")


def test_delete_contact(sample_contacts: dict[str, str]) -> None:
    delete_contact(sample_contacts, "Anna")
    assert "Anna" not in sample_contacts
    assert "Eduard" in sample_contacts


def test_delete_non_existed_contact_raises(sample_contacts: dict[str, str]) -> None:
    with pytest.raises(ContactNotFoundError, match="Unable to find contact"):
        delete_contact(sample_contacts, "James")