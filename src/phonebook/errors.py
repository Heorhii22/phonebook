class PhonebookError(Exception):
    "Application base error"

class StorageError(PhonebookError):
    ...

class ContactNotFoundError(PhonebookError):
    ...