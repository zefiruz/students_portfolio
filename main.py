from datetime import date
from models import Student, Project, Achievement, Document
from storage import (
    load_students, save_students, 
    load_projects, save_projects,
    load_achievements, save_achievements,
    load_documents, save_documents
)
from utils import input_int, input_float

STUDENTS_FILE = "data/students.json"
PROJECTS_FILE = "data/projects.json"
ACHIEVEMENTS_FILE = "data/achievements.json"
DOCUMENTS_FILE = "data/documents.json"

def main() -> None:
    # 1. Загрузка данных и восстановление связей объектов
    students = load_students(STUDENTS_FILE)
    projects = load_projects(PROJECTS_FILE, students)
    achievements = load_achievements(ACHIEVEMENTS_FILE, students)
    documents = load_documents(DOCUMENTS_FILE, students)

    while True:
        print("\n=== Сервис портфолио студентов ===")
        print("1. Добавить студента")
        print("2. Добавить навык студенту")
        print("3. Добавить проект")
        print("4. Изменить статус проекта")
        print("5. Рассчитать рейтинг студента")
        print("6. Показать все данные")
        print("7. Добавить достижение")
        print("8. Прикрепить документ")
        print("0. Выход и сохранение")

        choice = input("Выберите действие: ")

        if choice == "1":
            name = input("Имя студента: ")
            gpa = input_float("Средний балл (GPA): ")
            new_id = len(students) + 1
            students.append(Student(new_id, name, gpa))
            save_students(STUDENTS_FILE, students)
            print("Студент добавлен.")

        elif choice == "2":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                skill = input("Введите новый навык: ")
                student.skills.append(skill)
                save_students(STUDENTS_FILE, students)
                print(student.check_profile_completion())
            else:
                print("Студент не найден.")

        elif choice == "3":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                title = input("Название проекта: ")
                new_id = len(projects) + 1
                projects.append(Project(new_id, title, student))
                save_projects(PROJECTS_FILE, projects)
                print("Проект добавлен.")
            else:
                print("Студент не найден.")

        elif choice == "4":
            project_id = input_int("ID проекта: ")
            project = next((p for p in projects if p.id == project_id), None)
            if project:
                print("Доступные статусы: В разработке, Завершен, Планируется")
                new_status = input("Новый статус: ")
                project.update_status(new_status)
                save_projects(PROJECTS_FILE, projects)
                print(project.get_status_info())
            else:
                print("Проект не найден.")

        elif choice == "5":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                student_projects_count = sum(1 for p in projects if p.student.id == student.id)
                rating = student.calculate_rating(student_projects_count)
                print(f"Предварительный рейтинг студента {student.name}: {rating}")
            else:
                print("Студент не найден.")

        elif choice == "6":
            print("\n--- Студенты ---")
            for s in students: print(s)
            
            print("\n--- Проекты ---")
            for p in projects: print(p)
                
            print("\n--- Достижения ---")
            for a in achievements: print(a)
                
            print("\n--- Документы ---")
            for d in documents: print(d)

        elif choice == "7":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                title = input("Название достижения: ")
                category = input("Категория (например, IT, Спорт, Наука): ")
                date_str = input("Дата получения (ГГГГ-ММ-ДД): ")
                try:
                    issue_date = date.fromisoformat(date_str)
                    new_id = len(achievements) + 1
                    achievements.append(Achievement(new_id, title, issue_date, student, category))
                    save_achievements(ACHIEVEMENTS_FILE, achievements)
                    print("Достижение добавлено.")
                except ValueError:
                    print("Ошибка: Неверный формат даты. Используйте ГГГГ-ММ-ДД.")
            else:
                print("Студент не найден.")

        elif choice == "8":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                title = input("Название документа (например, Справка, Паспорт): ")
                file_path = input("Имя файла (например, document.pdf): ")
                new_id = len(documents) + 1
                doc = Document(new_id, title, file_path, student)
                documents.append(doc)
                save_documents(DOCUMENTS_FILE, documents)
                print(f"Документ добавлен. Формат определен как: .{doc.extension}")
            else:
                print("Студент не найден.")

        elif choice == "0":
            save_students(STUDENTS_FILE, students)
            save_projects(PROJECTS_FILE, projects)
            save_achievements(ACHIEVEMENTS_FILE, achievements)
            save_documents(DOCUMENTS_FILE, documents)
            print("Данные сохранены. Выход.")
            break

if __name__ == "__main__":
    main()