from django.shortcuts import render
from db.database import get_connection


def index(request):
    return render(request, "homepage/index.html")


def page_not_found(request, exception):
    return render(request, "404.html", status=404)


def statistics(request):
    """Сводная статистика по данным SQLite."""
    conn = get_connection()

    # 1. Общие агрегатные показатели
    summary = conn.execute(
        """
        SELECT
            COUNT(*) AS total_students,
            ROUND(AVG(gpa), 2) AS avg_gpa,
            MAX(gpa) AS max_gpa
        FROM students;
        """
    ).fetchone()

    # 2. Количество проектов по студентам (LEFT JOIN + GROUP BY)
    student_projects = conn.execute(
        """
        SELECT
            s.name,
            COUNT(p.id) AS p_count
        FROM students s
        LEFT JOIN projects p ON s.id = p.student_id
        GROUP BY s.id, s.name
        ORDER BY p_count DESC;
        """
    ).fetchall()

    # 3. Количество наград по категориям (GROUP BY)
    categories = conn.execute(
        """
        SELECT
            category,
            COUNT(*) AS c_count
        FROM achievements
        GROUP BY category
        ORDER BY c_count DESC;
        """
    ).fetchall()

    conn.close()

    context = {
        "summary": summary,
        "student_projects": student_projects,
        "categories": categories,
    }
    return render(request, "homepage/statistics.html", context)