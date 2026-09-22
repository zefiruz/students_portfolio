from models import Student, Project, Achievement, Document
from datetime import date

# student

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
    # 4.0 * 10 + 2 * 15 = 40 + 30 = 70
    assert student.calculate_rating(projects_count=2) == 70.0
    # Проверка работы при 0 проектов: 4.0 * 10 + 0 = 40
    assert student.calculate_rating(projects_count=0) == 40.0

def test_student_str():
    student = Student(1, "Алексей", 4.8)
    assert str(student) == "Студент: Алексей (Средний балл: 4.8)"

def test_student_from_data():
    data = {
        "id": 10, 
        "name": "Елена", 
        "gpa": 4.9, 
        "skills": ["Go", "Docker"]
    }
    student = Student.from_data(data)
    assert student.id == 10
    assert student.name == "Елена"
    assert student.gpa == 4.9
    assert len(student.skills) == 2
    assert "Go" in student.skills


# project

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

def test_achievement_linking():
    student = Student(1, "Иван", 4.5)
    achieve = Achievement(1, "Победитель олимпиады", date(2026, 10, 5), student, "Олимпиада")
    
    assert achieve.student is student
    assert achieve.student.name == "Иван"

def test_achievement_is_recent():
    student = Student(1, "Иван", 4.5)
    achieve = Achievement(1, "Хакатон", date(2026, 5, 12), student, "IT")
    
    assert achieve.is_recent(2026) is True
    assert achieve.is_recent(2025) is False

def test_achievement_str():
    student = Student(1, "Иван", 4.5)
    achieve = Achievement(1, "Хакатон", date(2026, 5, 12), student, "IT")
    
    expected_str = "[IT] Достижение 'Хакатон' (Студент: Иван)"
    assert str(achieve) == expected_str

def test_document_linking():
    student = Student(1, "Мария", 4.0)
    doc = Document(1, "Скан паспорта", "passport.jpg", student)
    
    assert doc.owner is student
    assert doc.owner.name == "Мария"

def test_document_extension_parsing():
    student = Student(1, "Мария", 4.0)
    
    # Проверка стандартного расширения
    doc_pdf = Document(1, "Справка", "spravka.pdf", student)
    assert doc_pdf.extension == "pdf"
    
    # Проверка приведения к нижнему регистру
    doc_png = Document(2, "Скан", "scan.PNG", student)
    assert doc_png.extension == "png"
    
    # Проверка файла без расширения
    doc_none = Document(3, "Архив", "just_file", student)
    assert doc_none.extension == "неизвестно"

def test_document_str():
    student = Student(1, "Мария", 4.0)
    doc = Document(1, "Справка", "spravka.pdf", student)
    
    expected_str = "Документ: Справка (Формат: .pdf) — Владелец: Мария"
    assert str(doc) == expected_str