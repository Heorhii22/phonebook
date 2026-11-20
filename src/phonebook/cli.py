import sys
import argparse
from pathlib import Path

from phonebook.errors import PhonebookError, StorageError
from phonebook.storage import load_contacts, save_contacts
from phonebook.service import add_contact, find_contact, delete_contact

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="phonebook")
    parser.add_argument("--file", type=Path, default=Path("contacts.json"))
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Save contact")
    add_parser.add_argument("name")
    add_parser.add_argument("phone")

    search_parser = subparsers.add_parser("find", help="Phonebook search")
    search_parser.add_argument("name")

    remove_parser = subparsers.add_parser("delete", help="Delete contact by name")
    remove_parser.add_argument("name")

    subparsers.add_parser("count", help="Count contacts in phonebook")
    subparsers.add_parser("list", help="Show all contacts")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        contacts = load_contacts(args.file)

    except StorageError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    if args.command == "list":
        if not contacts:
            print("No contacts")
            
        else:
            sorted_contacts = dict(sorted(contacts.items()))
            for name, phone in sorted_contacts.items():
                print(f"{name}: {phone}")

    elif args.command == "count":
        print(f"Contacts: {len(contacts)}")

    elif args.command == "add":
        try:
            add_contact(contacts, args.name, args.phone)
            save_contacts(args.file, contacts)
            print(f"Added {args.name}")

        except ValueError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1

    elif args.command == "find":
        try:
            phone = find_contact(contacts, args.name)
            print(phone)

        except PhonebookError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1

    elif args.command == "delete":
        try:
            delete_contact(contacts, args.name)
            save_contacts(args.file, contacts)
            print(f"Deleted {args.name}")

        except PhonebookError as error:
            print(f"Error: {error}", file=sys.stderr)
            return 1
    
    return 0




