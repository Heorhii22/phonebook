import pytest

from phonebook.models import Contact


@pytest.fixture
def contact() -> Contact:
    return Contact("Brian", "09038929134")
  


def test_data_saved_correctly(contact: Contact) -> None:
    assert contact.name == "Brian"
    assert contact.phone == "09038929134"


@pytest.mark.parametrize("name, phone, message",
                         [
                            pytest.param("", "09082042", "Name can not be empty", id="empty name"),
                            pytest.param("  ", "09082042", "Name can not be empty", id="name contains only spaces"),
                            pytest.param("James", "", "Phone should contain only numbers", id="empty phone"),
                            pytest.param("Louise", "ldsof", "Phone should contain only numbers", id="letters in phone",)
                         ])
def test_save_invalid_data_raise(name: str, phone: str, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        Contact(name, phone)


def test_to_dict_returns_correct_data(contact: Contact) -> None:
    assert contact.to_dict() == {"name": "Brian", "phone": "09038929134"}


def test_dict_roundtrip() -> None:
    data = {"name": "Anna", "phone": "0501234567"}

    contact = Contact.from_dict(data)  

    assert contact.to_dict() == data  


@pytest.mark.parametrize("data, message", 
                         [
                             ({"phone": "090823031"}, "Object must contain name and phone keys"),
                             ({"name": "Jared"}, "Object must contain name and phone keys"),
                             ({"name": "", "phone": "08920910833"}, "Name can not be empty"),
                         ])
def test_get_data_from_corrupted_dict_raises(data: dict[str, str], message: str) -> None:
    with pytest.raises(ValueError, match=message):
        Contact.from_dict(data)