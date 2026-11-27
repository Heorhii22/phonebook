# phonebook

Учебная консольная телефонная книга: контакты хранятся в JSON-файле. Пакет в раскладке `src` с собственными исключениями, слоями (хранилище, логика, интерфейс) и тестами.

## Структура проекта

```text
.
├── .gitignore               # не отслеживаются: .venv, кэши, *.egg-info, файлы данных
├── README.md
├── pyproject.toml
├── requirements.txt
├── requirements-dev.txt
├── src/
│   └── phonebook/
│       ├── __init__.py
│       ├── __main__.py      # точка входа: python -m phonebook
│       ├── cli.py           # разбор команд и вывод
│       ├── errors.py        # собственные исключения
│       ├── models.py        # класс Contact: проверки, to_dict, from_dict
│       ├── service.py       # логика: добавить, найти, найти по части имени, изменить телефон, удалить
│       └── storage.py       # чтение и запись JSON
└── tests/
    ├── test_cli.py
    ├── test_models.py
    ├── test_service.py
    └── test_storage.py
```

## Как запустить

Все команды выполняются из корня проекта (там, где лежит `pyproject.toml`).

1. Создать виртуальное окружение и активировать его:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Установить зависимости для разработки:

```bash
python -m pip install -r requirements-dev.txt
```

3. Установить пакет `phonebook` в окружение в режиме разработки:

```bash
python -m pip install -e .
```

4. Как пользоваться программой:

```bash
python -m phonebook add Anna 0501234567
python -m phonebook find Anna
python -m phonebook search nna
python -m phonebook update Anna 0507654321
python -m phonebook list
python -m phonebook count
python -m phonebook delete Anna
```

`search` ищет по любой части имени без учёта регистра и печатает найденные контакты по алфавиту (`Имя: телефон`); если ничего не найдено, печатает `No contacts found`. `update` меняет телефон существующего контакта и печатает `Updated Anna`; для несуществующего имени или телефона не из цифр выводит ошибку и возвращает код `1`.

Если книга пуста, `list` печатает `No contacts yet`, а `count` — `Contacts: 0`.

Контакты сохраняются в `contacts.json` в текущей папке. Файлы данных (`contacts.json`, `broken.json`) указаны в `.gitignore` и в репозиторий не попадают. Другой файл можно указать опцией `--file`, её пишут **до** команды:

```bash
python -m phonebook --file other.json list
```

Коды выхода: `0` — успех, `1` — ошибка (неверный телефон, нет такого контакта, испорченный файл), `2` — неверные аргументы командной строки.

5. Запустить тесты и проверку типов:

```bash
python -m pytest -v
python -m mypy src tests
```

6. Выйти из виртуального окружения (если нужно):

```bash
deactivate
```