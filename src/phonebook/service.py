from phonebook.errors import ContactNotFoundError


def add_contact(contacts: dict[str, str], name: str, phone: str) -> None:
    if not name:
        raise ValueError("Unacceptable contact name.")

    if not phone.isdigit():
        raise ValueError("Phone must contain only numbers!")

    contacts[name] = phone

def find_contact(contacts: dict[str, str], name: str) -> str:
    if name not in contacts:
        raise ContactNotFoundError(f"Unable to find contact by name {name}")
    
    searched_phone_num = contacts[name]

    return searched_phone_num

def delete_contact(contacts: dict[str, str], name: str) -> None:
    if name not in contacts:
        raise ContactNotFoundError(f"Unable to find contact by name {name}")

    del contacts[name]


def search_contact_by_part_name(contacts: dict[str, str], query: str) -> dict[str, str]:
    searched_contacts: dict[str, str] = {}

    if query.strip() == "":
        return searched_contacts

    for name, phone in contacts.items():
        if query.lower().strip() in name.lower():
            searched_contacts[name] = phone

    return searched_contacts


def update_contact_phone(contacts: dict[str, str], name: str, new_phone: str) -> None:
    if name not in contacts:
        raise ContactNotFoundError(f"Unable to find contact by name {name}")

    if not new_phone.isdigit():
        raise ValueError("Phone must contain only numbers!")

    contacts[name] = new_phone