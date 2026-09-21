from models import Student, Project

def test_student_profile_completion():
    student = Student(1, "Иван", 4.5, skills=[])
    assert "пуст" in student.check_profile_completion()
    
    student.skills.extend(["Python", "Git", "SQL"])
    assert "отлично" in student.check_profile_completion()

def test_student_rating_calculation():
    student = Student(1, "Анна", 4.0)
    # GPA 4.0 * 10 + 2 проекта * 15 = 40 + 30 = 70
    assert student.calculate_rating(projects_count=2) == 70.0

def test_project_linking_and_status():
    student = Student(1, "Петр", 3.8)
    project = Project(1, "Telegram Бот", student)
    
    assert project.student is student
    assert project.status == "В разработке"
    
    project.update_status("Завершен")
    assert "Завершен" in project.get_status_info()