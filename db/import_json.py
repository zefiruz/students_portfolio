import json
from db.database import get_connection

STUDENTS_FILE = "data/students.json"
PROJECTS_FILE = "data/projects.json"
DOCUMENTS_FILE = "data/documents.json"
ACHIEVEMENTS_FILE = "data/achievements.json"
SCHEMA_FILE = "sql/schema.sql"


def load_json(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def init_db(conn):
    with open(SCHEMA_FILE, "r", encoding="utf-8") as f:
        conn.executescript(f.read())


def import_data(conn):
    # 1. Импорт студентов
    students = load_json(STUDENTS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO students (id, name, gpa, skills)
        VALUES (?, ?, ?, ?)
        """,
        [
            (
                s["id"],
                s["name"],
                float(s["gpa"]),
                ", ".join(s.get("skills", [])),
            )
            for s in students
        ],
    )

    # 2. Импорт документов
    documents = load_json(DOCUMENTS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO documents (id, title, file_path, student_id)
        VALUES (?, ?, ?, ?)
        """,
        [
            (d["id"], d["title"], d["file_path"], d["student_id"])
            for d in documents
        ],
    )

    # 3. Импорт проектов
    projects = load_json(PROJECTS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO projects (id, title, status, student_id)
        VALUES (?, ?, ?, ?)
        """,
        [
            (p["id"], p["title"], p["status"], p["student_id"])
            for p in projects
        ],
    )

    # 4. Импорт достижений
    achievements = load_json(ACHIEVEMENTS_FILE)
    conn.executemany(
        """
        INSERT OR REPLACE INTO achievements (
            id, title, issue_date, student_id, category, document_id
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        [
            (
                a["id"],
                a["title"],
                a["issue_date"],
                a["student_id"],
                a["category"],
                a.get("document_id"),
            )
            for a in achievements
        ],
    )


def main():
    conn = get_connection()
    try:
        init_db(conn)
        import_data(conn)
        conn.commit()
        print("База данных успешно создана и наполнена из JSON-файлов.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при импорте данных: {e}")
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()