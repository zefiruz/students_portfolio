from django.shortcuts import render
from db.database import get_connection
from models.student import Student


def students_list(request):
    conn = get_connection()
    students = conn.execute(
        """
        SELECT id, name, gpa, skills
        FROM students
        ORDER BY gpa DESC;
        """
    ).fetchall()
    conn.close()
    return render(
        request,
        "students/student_list.html",
        {"students": students},
    )


def student_detail(request, student_id):
    conn = get_connection()
    student = conn.execute(
        "SELECT id, name, gpa, skills FROM students WHERE id = ?;",
        (student_id,),
    ).fetchone()

    if student is None:
        conn.close()
        return render(
            request,
            "students/student_detail.html",
            {"student": None},
            status=404,
        )

    # Проекты студента через параметризованный SQL
    projects = conn.execute(
        "SELECT id, title, status FROM projects WHERE student_id = ?;",
        (student_id,),
    ).fetchall()

    # Достижения студента с документами через JOIN
    achievements = conn.execute(
        """
        SELECT
            a.id, a.title, a.issue_date, a.category,
            d.title AS doc_title, d.file_path AS doc_file
        FROM achievements a
        LEFT JOIN documents d ON a.document_id = d.id
        WHERE a.student_id = ?
        ORDER BY a.issue_date DESC;
        """,
        (student_id,),
    ).fetchall()
    conn.close()

    skills_list = [
        s.strip()
        for s in student["skills"].split(",")
        if s.strip()
    ]

    student_obj = Student(
        student_id=student["id"],
        name=student["name"],
        gpa=student["gpa"],
        skills=skills_list,
    )
    completion = student_obj.check_profile_completion()
    rating = student_obj.calculate_rating(projects_count=len(projects))

    context = {
        "student": student,
        "skills_list": skills_list,
        "completion": completion,
        "rating": rating,
        "projects": projects,
        "achievements": achievements,
    }
    return render(request, "students/student_detail.html", context)


def student_search(request):
    """Поиск студентов по минимальному GPA (параметризованный запрос)."""
    min_gpa = request.GET.get("min_gpa")
    students = []

    if min_gpa:
        try:
            val = float(min_gpa)
            conn = get_connection()
            students = conn.execute(
                """
                SELECT id, name, gpa, skills
                FROM students
                WHERE gpa >= ?
                ORDER BY gpa DESC;
                """,
                (val,),
            ).fetchall()
            conn.close()
        except ValueError:
            pass

    return render(
        request,
        "students/student_search.html",
        {"students": students, "min_gpa": min_gpa},
    )
