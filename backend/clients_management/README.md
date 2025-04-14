<div align="center">
    <h1>
        <b>Clients Management</b>
    </h1>
    <h3>
        Сервис менеджмента клиентов
    </h3>
    <img alt="GitHub Last Commit" src="https://img.shields.io/github/last-commit/alex6712/sport-monitor?logo=GitHub">
    <img alt="Tests Passed" src="https://github.com/alex6712/sport-monitor/actions/workflows/backend-tests.yml/badge.svg">
    <a href="https://github.com/psf/black">
        <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
    </a>
</div>

Код бакалаврской дипломной работы студентки НГТУ им. Р.Е. Алексеева, Камневой Анастасии Игоревны.

## Запуск решения

Корневая папка сервиса ``backend/clients_management``.

### Установка зависимостей

В корневой папке находятся файлы ``poetry.lock`` и ``pyproject.toml``, которые используются **Poetry** для менеджмента 
зависимостей, необходимых для работы сервиса.

Чтобы их установить используйте следующую команду:

```powershell
cd backend/clients_management
poetry install
```

Также в той папке находятся файл ``requirements.txt``,
поэтому также присутствует возможность установки зависимостей с помощью **pip**:

```powershell
pip install -r requirements.txt
```

### Запуск скрипта

Сервер запускается с помощью скрипта ``start.py`` в корневой папке проекта.

Чтобы запустить скрипт, используйте команду

```powershell
py start.py
```

находясь в корневой папке проекта.

Если зависимости были установлены с помощью poetry, и виртуальное окружение не было
активировано, то используйте следующий алгоритм:

1. Откройте **PowerShell** в корневой папке проекта с правами администратора.
2. Исполните команды
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   Invoke-Expression (poetry env activate)
   ```

Таким образом вы активируете виртуальное окружение проекта со всеми необходимыми зависимостями.

## Стек

Использовался фреймворк **FastAPI** для создания API, а также фреймворк **SQLAlchemy**
для связи с базой данных.

База данных использует диалект **PostgreSQL** (версия *SQL 17*), для её менеджмента использовался **pgAdmin 4**.

## Лицензия

[MIT License](https://github.com/alex6712/gi-characters-analyzer/blob/master/LICENSE.md)

## Автор

Камнева Анастасия Игоревна, ИРИТ, НГТУ, 2025 год.
