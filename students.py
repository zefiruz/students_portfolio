def add_student(students: list[dict], name: str, age: int) -> None:
    """Добавить студента в список."""
    student_id = len(students) + 1
    students.append({"id": student_id, "name": name, "age": age})

def find_student(students: list[dict], query: str) -> list[dict]:
    """Найти студента по подстроке имени."""
    return [s for s in students if query.lower() in s["name"].lower()]