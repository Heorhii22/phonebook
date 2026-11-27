# phonebook

Консольная телефонная книга на Python. Контакты хранятся в JSON-файле.

## Возможности

| Команда | Что делает | Пример вывода |
| --- | --- | --- |
| `add NAME PHONE` | Добавить контакт (телефон — только цифры) | `Added Anna` |
| `find NAME` | Показать телефон контакта | `0931234567` |
| `update NAME PHONE` | Изменить телефон контакта | `Updated Anna` |
| `delete NAME` | Удалить контакт | `Deleted Anna` |
| `list` | Все контакты по алфавиту | `Anna: 0931234567` |
| `search TEXT` | Контакты, в имени которых есть `TEXT`, без учёта регистра | `Anna: 0931234567` |
| `count` | Количество контактов | `Contacts: 1` |

Опция `--file PATH` задаёт файл с контактами (по умолчанию `contacts.json` в текущей папке). Опцию пишут до команды:

```bash
python -m phonebook --file my_contacts.json list
```

Ошибки (контакт не найден, неверный телефон, испорченный файл) выводятся в `stderr`, программа завершается с кодом `1`. Неверные аргументы команды — код `2`.

## Как запустить

Нужен Python 3.12 или новее. Все команды — из корня проекта.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -m pip install -e .
```

Проверка:

```bash
python -m phonebook add Anna 0931234567
python -m phonebook list
```

## Тесты и проверка типов

```bash
python -m pytest
python -m mypy src tests
```

## Структура

```text
phonebook/
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── src/
│   └── phonebook/
│       ├── __init__.py
│       ├── __main__.py   # запуск через python -m phonebook
│       ├── cli.py        # разбор аргументов и вывод
│       ├── errors.py     # исключения программы
│       ├── models.py     # класс Contact
│       ├── service.py    # логика: добавить, найти, изменить, удалить, искать
│       └── storage.py    # чтение и запись JSON
└── tests/
    ├── test_cli.py
    ├── test_models.py
    ├── test_service.py
    └── test_storage.py
```