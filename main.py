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
from utils import input_float, input_int

STUDENTS_FILE = "data/students.json"
PROJECTS_FILE = "data/projects.json"
ACHIEVEMENTS_FILE = "data/achievements.json"
DOCUMENTS_FILE = "data/documents.json"


def main() -> None:
    students = load_students(STUDENTS_FILE)
    projects = load_projects(PROJECTS_FILE, students)
    documents = load_documents(DOCUMENTS_FILE, students)
    achievements = load_achievements(ACHIEVEMENTS_FILE, students, documents)

    while True:
        print("\n=== Сервис портфолио студентов ===")
        print("1. Добавить студента")
        print("2. Добавить навык студенту")
        print("3. Добавить проект")
        print("4. Изменить статус проекта")
        print("5. Рассчитать рейтинг студента")
        print("6. Показать все данные")
        print("7. Добавить достижение")
        print("8. Прикрепить новый документ")
        print("9. Привязать документ к существующему достижению")
        print("0. Выход и сохранение")

        choice = input("Выберите действие: ").strip()

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
                count = sum(1 for p in projects if p.student.id == student.id)
                rating = student.calculate_rating(count)
                print(
                    f"Предварительный рейтинг студента "
                    f"{student.name}: {rating}"
                )
            else:
                print("Студент не найден.")

        elif choice == "6":
            print("\n--- Студенты ---")
            for s in students:
                print(s)
            print("\n--- Проекты ---")
            for p in projects:
                print(p)
            print("\n--- Документы ---")
            for d in documents:
                print(d)
            print("\n--- Достижения ---")
            for a in achievements:
                print(a)

        elif choice == "7":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                title = input("Название достижения: ")
                category = input("Категория (например, IT, Спорт, Наука): ")
                date_str = input("Дата получения (ДД-ММ-ГГГГ): ")
                try:
                    issue_date = date.strptime(date_str, "%d-%m-%Y").date()
                    linked_doc = None
                    attach = input(
                        "Прикрепить существующий документ? (д/н): "
                    ).strip().lower()

                    if attach == "д":
                        doc_id = input_int("ID документа: ")
                        linked_doc = next(
                            (
                                d for d in documents
                                if d.id == doc_id and d.owner.id == student.id
                            ),
                            None,
                        )
                        if linked_doc:
                            print(f"Документ '{linked_doc.title}' прикреплен.")
                        else:
                            print(
                                "Документ не найден или принадлежит другому "
                                "студенту. Достижение создано без файла."
                            )

                    new_id = len(achievements) + 1
                    achievements.append(
                        Achievement(
                            new_id,
                            title,
                            issue_date,
                            student,
                            category,
                            document=linked_doc,
                        )
                    )
                    save_achievements(ACHIEVEMENTS_FILE, achievements)
                    print("Достижение добавлено.")
                except ValueError:
                    print(
                        "Ошибка: Неверный формат даты. Используйте ДД-ММ-ГГГГ."
                    )
            else:
                print("Студент не найден.")

        elif choice == "8":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                title = input("Название документа (Справка, Диплом): ")
                file_path = input("Имя файла (document.pdf): ")
                new_id = len(documents) + 1
                doc = Document(new_id, title, file_path, student)
                documents.append(doc)
                save_documents(DOCUMENTS_FILE, documents)
                print(f"Документ добавлен. Формат: .{doc.extension}")
            else:
                print("Студент не найден.")

        elif choice == "9":
            ach_id = input_int("ID достижения: ")
            ach = next((a for a in achievements if a.id == ach_id), None)
            if not ach:
                print("Достижение не найдено.")
            else:
                doc_id = input_int("ID документа: ")
                doc = next(
                    (
                        d for d in documents
                        if d.id == doc_id and d.owner.id == ach.student.id
                    ),
                    None,
                )
                if not doc:
                    print(
                        "Документ не найден или принадлежит другому студенту."
                    )
                else:
                    ach.document = doc
                    save_achievements(ACHIEVEMENTS_FILE, achievements)
                    print(
                        f"Документ '{doc.title}' успешно привязан "
                        f"к достижению '{ach.title}'."
                    )

        elif choice == "0":
            save_students(STUDENTS_FILE, students)
            save_projects(PROJECTS_FILE, projects)
            save_documents(DOCUMENTS_FILE, documents)
            save_achievements(ACHIEVEMENTS_FILE, achievements)
            print("Данные сохранены. Выход.")
            break


if __name__ == "__main__":
    main()
