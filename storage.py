import json
import os
from typing import List
from models import Student, Project

def load_students(filename: str) -> List[Student]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Student.from_data(item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_students(filename: str, students: List[Student]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [{"id": s.id, "name": s.name, "gpa": s.gpa, "skills": s.skills} for s in students]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_projects(filename: str, students: List[Student]) -> List[Project]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            projects = []
            for item in data:
                # Восстанавливаем связь с объектом Student
                student = next((s for s in students if s.id == item["student_id"]), None)
                if student:
                    projects.append(Project(item["id"], item["title"], student, item["status"]))
            return projects
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_projects(filename: str, projects: List[Project]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # При сохранении извлекаем ID студента
    data = [{"id": p.id, "title": p.title, "status": p.status, "student_id": p.student.id} for p in projects]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)