import json
import os
from typing import List
from models import Student, Project
from datetime import date
from models import Achievement, Document


def load_students(filename: str) -> List[Student]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Student.from_data(item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_students(filename: str, students: List[Student]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    data = [
        {"id": s.id, "name": s.name, "gpa": s.gpa, "skills": s.skills} for s in students
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_projects(filename: str, students: List[Student]) -> List[Project]:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            projects = []
            for item in data:
                # Восстанавливаем связь с объектом Student
                student = next(
                    (s for s in students if s.id == item["student_id"]), None
                )
                if student:
                    projects.append(
                        Project(item["id"], item["title"], student, item["status"])
                    )
            return projects
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_projects(filename: str, projects: List[Project]) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    # При сохранении извлекаем ID студента
    data = [
        {"id": p.id, "title": p.title, "status": p.status, "student_id": p.student.id}
        for p in projects
    ]
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_achievements(filename: str, students: list) -> list:
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
            
    achievements = []
    for item in data:
        student = next((s for s in students if s.id == item["student_id"]), None)
        if student:
            # Преобразуем строку обратно в дату
            issue_date = date.fromisoformat(item["issue_date"])
            achievements.append(Achievement(item["id"], item["title"], issue_date, student, item["category"]))
    return achievements

def save_achievements(filename: str, achievements: list) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        data = [
            {
                "id": a.id,
                "title": a.title,
                "issue_date": a.issue_date.isoformat(), # Сохраняем дату как строку YYYY-MM-DD
                "student_id": a.student.id,
                "category": a.category
            }
            for a in achievements
        ]
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_documents(filename: str, students: list) -> list:
    if not os.path.exists(filename):
        return []
    with open(filename, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return []
            
    documents = []
    for item in data:
        student = next((s for s in students if s.id == item["student_id"]), None)
        if student:
            documents.append(Document(item["id"], item["title"], item["file_path"], student))
    return documents

def save_documents(filename: str, documents: list) -> None:
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        data = [
            {
                "id": d.id,
                "title": d.title,
                "file_path": d.file_path,
                "student_id": d.owner.id
            }
            for d in documents
        ]
        json.dump(data, f, ensure_ascii=False, indent=4)