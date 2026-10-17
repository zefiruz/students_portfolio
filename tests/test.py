from datetime import date

from models import Achievement, Document, Project, Student
from storage import (
    load_achievements,
    load_documents,
    load_projects,
    load_students,
    save_achievements,
    save_documents,
    save_projects,
    save_students,
)


# ==========================================
# 1. ТЕСТЫ ДЛЯ СУЩНОСТИ STUDENT
# ==========================================


def test_student_profile_completion_empty():
    student = Student(1, "Иван", 4.5, skills=[])
    assert "пуст" in student.check_profile_completion()


def test_student_profile_completion_partial():
    student = Student(2, "Мария", 4.0, skills=["Python", "SQL"])
    assert "частично" in student.check_profile_completion()


def test_student_profile_completion_full():
    student = Student(3, "Олег", 3.5, skills=["Python", "Git", "SQL"])
    assert "отлично" in student.check_profile_completion()


def test_student_rating_calculation():
    student = Student(1, "Анна", 4.0)
    # 4.0 * 10 + 2 * 15 = 40 + 30 = 70.0
    assert student.calculate_rating(projects_count=2) == 70.0
    # Проверка работы при 0 проектов: 4.0 * 10 + 0 = 40.0
    assert student.calculate_rating(projects_count=0) == 40.0


def test_student_str():
    student = Student(1, "Алексей", 4.8)
    assert str(student) == "Студент: Алексей (Средний балл: 4.8)"


def test_student_from_data():
    data = {
        "id": 10,
        "name": "Елена",
        "gpa": 4.9,
        "skills": ["Go", "Docker"],
    }
    student = Student.from_data(data)
    assert student.id == 10
    assert student.name == "Елена"
    assert student.gpa == 4.9
    assert len(student.skills) == 2
    assert "Go" in student.skills


# ==========================================
# 2. ТЕСТЫ ДЛЯ СУЩНОСТИ PROJECT
# ==========================================


def test_project_linking():
    student = Student(1, "Петр", 3.8)
    project = Project(100, "Telegram Бот", student)

    assert project.student is student
    assert project.student.name == "Петр"
    assert project.student.gpa == 3.8


def test_project_status_update_valid():
    student = Student(1, "Петр", 3.8)
    project = Project(1, "Telegram Бот", student)

    assert project.status == "В разработке"
    project.update_status("Завершен")
    assert project.status == "Завершен"
    assert "Завершен" in project.get_status_info()


def test_project_status_update_invalid():
    student = Student(1, "Петр", 3.8)
    project = Project(1, "Telegram Бот", student)

    project.update_status("Сломался")
    assert project.status == "В разработке"


def test_project_str():
    student = Student(1, "Илья", 4.2)
    project = Project(1, "API Сервис", student, "Планируется")

    expected_str = "Проект 'API Сервис' [Планируется] (Автор: Илья)"
    assert str(project) == expected_str


# ==========================================
# 3. ТЕСТЫ ДЛЯ СУЩНОСТИ DOCUMENT
# ==========================================


def test_document_linking():
    student = Student(1, "Мария", 4.0)
    doc = Document(1, "Скан паспорта", "passport.jpg", student)

    assert doc.owner is student
    assert doc.owner.name == "Мария"


def test_document_extension_parsing():
    student = Student(1, "Мария", 4.0)

    # Стандартное расширение
    doc_pdf = Document(1, "Справка", "spravka.pdf", student)
    assert doc_pdf.extension == "pdf"

    # Приведение регистра к нижнему
    doc_png = Document(2, "Скан", "scan.PNG", student)
    assert doc_png.extension == "png"

    # Двойное расширение (берется последний сегмент)
    doc_archive = Document(3, "Бэкап", "data.tar.gz", student)
    assert doc_archive.extension == "gz"

    # Файл без точки в имени
    doc_none = Document(4, "Архив", "just_file", student)
    assert doc_none.extension == "неизвестно"


def test_document_str():
    student = Student(1, "Мария", 4.0)
    doc = Document(1, "Справка", "spravka.pdf", student)

    expected_str = "Документ: Справка (Формат: .pdf) — Владелец: Мария"
    assert str(doc) == expected_str


# ==========================================
# 4. ТЕСТЫ ДЛЯ СУЩНОСТИ ACHIEVEMENT
# ==========================================


def test_achievement_linking_student():
    student = Student(1, "Иван", 4.5)
    achieve = Achievement(
        1, "Победитель олимпиады", date(2026, 10, 5), student, "Олимпиада"
    )

    assert achieve.student is student
    assert achieve.student.name == "Иван"
    assert achieve.document is None


def test_achievement_linking_document():
    student = Student(1, "Иван", 4.5)
    doc = Document(10, "Диплом", "diploma.pdf", student)
    achieve = Achievement(
        1,
        "Хакатон 2026",
        date(2026, 5, 12),
        student,
        "IT",
        document=doc,
    )

    assert achieve.document is doc
    assert achieve.document.file_path == "diploma.pdf"
    assert achieve.document.owner is student


def test_achievement_is_recent():
    student = Student(1, "Иван", 4.5)
    achieve = Achievement(1, "Хакатон", date(2026, 5, 12), student, "IT")

    assert achieve.is_recent(2026) is True
    assert achieve.is_recent(2025) is False


def test_achievement_str_without_document():
    student = Student(1, "Иван", 4.5)
    achieve = Achievement(1, "Хакатон", date(2026, 5, 12), student, "IT")

    expected_str = "[IT] Достижение 'Хакатон' (Студент: Иван)"
    assert str(achieve) == expected_str


def test_achievement_str_with_document():
    student = Student(1, "Иван", 4.5)
    doc = Document(1, "Сертификат", "cert.pdf", student)
    achieve = Achievement(
        1,
        "Хакатон",
        date(2026, 5, 12),
        student,
        "IT",
        document=doc,
    )

    expected_str = (
        "[IT] Достижение 'Хакатон' (Студент: Иван) "
        "[Подтверждено файлом: cert.pdf]"
    )
    assert str(achieve) == expected_str


# ==========================================
# 5. ТЕСТЫ ДЛЯ МОДУЛЯ STORAGE (JSON)
# ==========================================


def test_storage_students_save_and_load(tmp_path):
    filepath = str(tmp_path / "students.json")
    original = [
        Student(1, "Анна", 4.8, ["Python", "Django"]),
        Student(2, "Борис", 3.9, ["SQL"]),
    ]

    save_students(filepath, original)
    loaded = load_students(filepath)

    assert len(loaded) == 2
    assert loaded[0].id == 1
    assert loaded[0].name == "Анна"
    assert loaded[0].gpa == 4.8
    assert loaded[0].skills == ["Python", "Django"]
    assert loaded[1].name == "Борис"


def test_storage_projects_save_and_load(tmp_path):
    filepath = str(tmp_path / "projects.json")
    student = Student(1, "Анна", 4.8)
    original = [
        Project(1, "Портфолио", student, "В разработке"),
    ]

    save_projects(filepath, original)
    # При загрузке восстанавливается ссылка на объект Student
    loaded = load_projects(filepath, [student])

    assert len(loaded) == 1
    assert loaded[0].title == "Портфолио"
    assert loaded[0].student is student
    assert loaded[0].student.name == "Анна"


def test_storage_documents_save_and_load(tmp_path):
    filepath = str(tmp_path / "documents.json")
    student = Student(1, "Ольга", 4.2)
    original = [
        Document(1, "Справка", "spravka.pdf", student),
    ]

    save_documents(filepath, original)
    # При загрузке восстанавливается владелец owner
    loaded = load_documents(filepath, [student])

    assert len(loaded) == 1
    assert loaded[0].title == "Справка"
    assert loaded[0].owner is student
    assert loaded[0].extension == "pdf"


def test_storage_achievements_save_and_load_with_relations(tmp_path):
    filepath = str(tmp_path / "achievements.json")
    student = Student(1, "Максим", 4.9)
    doc = Document(10, "Грамота", "award.png", student)

    original = [
        Achievement(
            1,
            "1 место",
            date(2026, 3, 15),
            student,
            "Наука",
            document=doc,
        ),
        Achievement(
            2,
            "Участие",
            date(2026, 4, 1),
            student,
            "Спорт",
            document=None,
        ),
    ]

    save_achievements(filepath, original)
    # При загрузке восстанавливаются связи со Student и Document
    loaded = load_achievements(filepath, [student], [doc])

    assert len(loaded) == 2

    # Первое достижение связано с документом
    assert loaded[0].id == 1
    assert loaded[0].student is student
    assert loaded[0].document is doc
    assert loaded[0].document.file_path == "award.png"

    # Второе достижение без документа
    assert loaded[1].id == 2
    assert loaded[1].student is student
    assert loaded[1].document is None


def test_storage_missing_and_empty_files(tmp_path):
    missing_file = str(tmp_path / "nonexistent.json")

    assert load_students(missing_file) == []
    assert load_projects(missing_file, []) == []
    assert load_documents(missing_file, []) == []
    assert load_achievements(missing_file, [], []) == []
