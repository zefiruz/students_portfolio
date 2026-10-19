# Сервис портфолио студентов

Учебное веб-приложение на Django для систематизации, хранения и демонстрации академических результатов, исследовательских проектов, подтверждающих документов и призовых достижений студентов.

Проект разработан поэтапно в рамках единого репозитория:
1. **ПР1–ПР3**: Консольное объектно-ориентированное приложение, сущности предметной области, файловое хранилище JSON и набор тестов `pytest`.
2. **ПР5**: Переход к веб-разработке на Django: создание проекта и приложений, двухуровневая маршрутизация URL, view-функции и обработка ошибки 404.
3. **ПР6**: Переход на систему шаблонов Django Template Language (DTL): базовый каркас `base.html`, наследование, подключаемые компоненты `{% include %}`, пространства имён `app_name`, фильтры и статические файлы (CSS, JS, логотип).

---

## 1. Используемые технологии

* **Язык программирования:** Python 3.11 / 3.13
* **Веб-фреймворк:** Django 5.2 (LTS)
* **Шаблонизация:** Django Template Language (DTL) — блочное наследование, `include`, фильтры и именованные маршруты
* **Фронтенд:** HTML5, CSS3, JavaScript (ES6), фреймворк Bootstrap 5.3 (CDN)
* **Хранение данных:** JSON-файлы (`data/students.json`, `data/projects.json`, `data/documents.json`, `data/achievements.json`)
* **Тестирование:** `pytest` (43 автоматизированных теста)
* **Контроль качества кода (PEP 8):** линтер `flake8`
* **Система контроля версий:** Git

---

## 2. Предметная область и сущности

В проекте реализованы 4 взаимосвязанные сущности предметной области:
* **Студент (`Student`)** — базовый субъект системы: уникальный идентификатор (`id`), имя (`name`), средний балл (`gpa`), перечень компетенций (`skills`). Методы: расчёт рейтинга активности `calculate_rating()`, проверка степени полноты профиля `check_profile_completion()`.
* **Проект (`Project`)** — разработка или научно-исследовательская работа студента: идентификатор (`id`), название (`title`), статус жизненного цикла (`status`: «В разработке», «Завершен», «Планируется»), автор (`student`, ссылка на объект `Student`). Методы: `update_status()`, `get_status_info()`.
* **Документ (`Document`)** — цифровой сертификат или скан-копия: идентификатор (`id`), наименование (`title`), путь к файлу (`file_path`), студент-владелец (`owner`, ссылка на объект `Student`). Свойство: расширение файла `extension`.
* **Достижение (`Achievement`)** — призовое место или победа: идентификатор (`id`), наименование (`title`), дата получения (`issue_date`), студент (`student`), категория (`category`), подтверждающий документ (`document` или `None`). Метод: `is_recent()`.

---

## 3. Веб-интерфейс и архитектура шаблонов (ПР6)

Генерация HTML-строк в Python-коде (`page()`) полностью удалена. Веб-интерфейс построен на архитектуре Django Template Language:

### Структура шаблонов
* **`templates/base.html`** — базовый каркас сайта с блоками `{% block title %}` и `{% block content %}`, подключением Bootstrap 5.3, собственного CSS, скрипта JavaScript и подключаемой навигации.
* **`templates/includes/navigation.html`** — вынесенный подключаемый шаблон навигационной панели. Ссылки формируются динамически тегом `{% url %}`.
* **`templates/404.html`** — стилизованная страница ошибки 404, вызываемая обработчиком `handler404`.
* **Включаемые шаблоны компонентов:**
  * `students/templates/students/includes/student_card.html` — карточка студента в списке.
  * `projects/templates/projects/includes/project_status.html` — цветовой бейдж статуса проекта.

### Маршруты и пространства имён (Namespaces)
* **`homepage` (`app_name = "homepage"`):**
  * `/` (`homepage:index`) — главная страница сервиса.
* **`students` (`app_name = "students"`):**
  * `/students/` (`students:list`) — реестр студентов.
  * `/students/<int:student_id>/` (`students:detail`) — детальный профиль студента с расчётом рейтинга.
* **`projects` (`app_name = "projects"`):**
  * `/projects/` (`projects:list`) — каталог проектов.
  * `/projects/<int:project_id>/` (`projects:detail`) — карточка проекта.
* **`achievements` (`app_name = "achievements"`):**
  * `/achievements/` (`achievements:list`) — список наград.
  * `/achievements/<int:achievement_id>/` (`achievements:detail`) — детальная страница достижения.

---

## 4. Статические файлы проекта

* **`homepage/static/homepage/css/style.css`** — кастомные стили карточек, логотипа и бейджей.
* **`homepage/static/homepage/js/main.js`** — динамический вывод актуального года в подвале.
* **`homepage/static/homepage/img/logo.png`** — логотип сервиса.

---

## 5. Структура проекта

```text
students_portfolio/
├── manage.py                          # Утилита управления Django
├── main.py                            # Консольная версия приложения (ПР1–ПР3)
├── storage.py                         # Модуль загрузки и сохранения JSON
├── utils.py                           # Вспомогательные функции ввода
├── requirements.txt                   # Зависимости окружения
├── pytest.ini                         # Конфигурация pytest
├── README.md                          # Документация проекта
│
├── portfolio_project/                 # Пакет конфигурации проекта
│   ├── __init__.py
│   ├── settings.py                    # Настройки (TEMPLATES, DIRS, i18n)
│   ├── urls.py                        # Корневой URLconf и handler404
│   ├── asgi.py
│   └── wsgi.py
│
├── data/                              # Хранилище данных JSON
│   ├── students.json
│   ├── projects.json
│   ├── documents.json
│   └── achievements.json
│
├── models/                            # Классы предметной области
│   ├── __init__.py
│   ├── student.py
│   ├── project.py
│   ├── document.py
│   └── achievement.py
│
├── templates/                         # Шаблоны уровня проекта
│   ├── base.html
│   ├── 404.html
│   └── includes/
│       └── navigation.html
│
├── homepage/                          # Приложение главной страницы
├── students/                          # Приложение студентов
├── projects/                          # Приложение проектов
├── achievements/                      # Приложение достижений
└── tests/                             # Автоматизированные тесты
```

---

## 6. Развертывание и запуск приложения

```bash
# Активация окружения
source venv/Scripts/activate

# Установка зависимостей
pip install -r requirements.txt

# Запуск сервера разработки
python manage.py runserver
```
Веб-интерфейс доступен по адресу: http://127.0.0.1:8000/.

---

## 7. Тестирование и контроль качества кода

```bash
# Системная проверка Django
python manage.py check

# Запуск автоматизированных тестов (43 passed)
pytest -v

# Проверка стиля кода по стандарту PEP 8 (0 ошибок)
flake8 . --extend-exclude=venv
```