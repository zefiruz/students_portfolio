def add_project(projects: list[dict], student_id: int, title: str) -> None:
    """Добавить проект в портфолио студента."""
    projects.append({
        "student_id": student_id, 
        "title": title, 
        "status": "В разработке"
    })

def get_student_projects(projects: list[dict], student_id: int) -> list[dict]:
    """Получить все проекты конкретного студента."""
    return [p for p in projects if p["student_id"] == student_id]