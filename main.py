from models import Student, Project
from storage import load_students, save_students, load_projects, save_projects
from utils import input_int, input_float

STUDENTS_FILE = "data/students.json"
PROJECTS_FILE = "data/projects.json"


def main() -> None:
    students = load_students(STUDENTS_FILE)
    projects = load_projects(PROJECTS_FILE, students)

    while True:
        print("\n=== Сервис портфолио студентов ===")
        print("1. Добавить студента")
        print("2. Добавить навык студенту и проверить профиль")
        print("3. Добавить проект")
        print("4. Изменить и проверить статус проекта")
        print("5. Рассчитать рейтинг студента")
        print("6. Показать все данные")
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

                # Проверка полноты заполнения профиля студента.
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
                print(f"Доступные статусы: В разработке, Завершен, Планируется")
                new_status = input("Новый статус: ")
                project.update_status(new_status)
                # Определение текущего статуса проекта.
                print(project.get_status_info())
            else:
                print("Проект не найден.")

        elif choice == "5":
            student_id = input_int("ID студента: ")
            student = next((s for s in students if s.id == student_id), None)
            if student:
                # Считаем проекты именно этого студента
                student_projects_count = sum(
                    1 for p in projects if p.student.id == student.id
                )
                # Расчет предварительного рейтинга студента на основе количества проектов и среднего балла.
                rating = student.calculate_rating(student_projects_count)
                print(f"Предварительный рейтинг студента {student.name}: {rating}")
            else:
                print("Студент не найден.")

        elif choice == "6":
            print("\n--- Студенты ---")
            for s in students:
                print(s)
            print("\n--- Проекты ---")
            for p in projects:
                print(p)

        elif choice == "0":
            save_students(STUDENTS_FILE, students)
            save_projects(PROJECTS_FILE, projects)
            print("Данные сохранены. Выход.")
            break


if __name__ == "__main__":
    main()
