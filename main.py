from storage import load_data, save_data
from students import add_student, find_student
from projects import add_project, get_student_projects
from utils import input_int

STUDENTS_FILE = "data/students.json"
PROJECTS_FILE = "data/projects.json"

def main() -> None:
    """Точка запуска приложения."""
    students = load_data(STUDENTS_FILE)
    projects = load_data(PROJECTS_FILE)

    while True:
        print("\n=== Сервис портфолио студентов ===")
        print("1. Добавить студента")
        print("2. Найти студента")
        print("3. Добавить проект в портфолио")
        print("4. Показать проекты студента")
        print("0. Выход")

        choice = input_int("Выберите действие: ")

        if choice == 1:
            name = input("Имя студента: ")
            age = input_int("Возраст: ")
            add_student(students, name, age)
            save_data(STUDENTS_FILE, students)
            print("Студент добавлен.")
        elif choice == 2:
            query = input("Введите имя для поиска: ")
            found = find_student(students, query)
            for s in found:
                print(f"[{s['id']}] {s['name']} (Возраст: {s['age']})")
        elif choice == 3:
            student_id = input_int("ID студента: ")
            title = input("Название проекта: ")
            add_project(projects, student_id, title)
            save_data(PROJECTS_FILE, projects)
            print("Проект добавлен.")
        elif choice == 4:
            student_id = input_int("ID студента: ")
            student_projects = get_student_projects(projects, student_id)
            for p in student_projects:
                print(f"- {p['title']} [{p['status']}]")
        elif choice == 0:
            break

if __name__ == "__main__":
    main()