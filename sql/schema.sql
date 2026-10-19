-- sql/schema.sql
-- Сервис портфолио студентов: схема базы данных

CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    gpa REAL NOT NULL,
    skills TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    status TEXT NOT NULL,
    student_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
);

CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    file_path TEXT NOT NULL,
    student_id INTEGER NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students (id)
);

CREATE TABLE IF NOT EXISTS achievements (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    issue_date TEXT NOT NULL,
    student_id INTEGER NOT NULL,
    category TEXT NOT NULL,
    document_id INTEGER,
    FOREIGN KEY (student_id) REFERENCES students (id),
    FOREIGN KEY (document_id) REFERENCES documents (id)
);