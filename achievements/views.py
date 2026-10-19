from django.shortcuts import render
from db.database import get_connection


def achievements_list(request):
    conn = get_connection()
    achievements = conn.execute(
        """
        SELECT
            a.id,
            a.title,
            a.category,
            a.issue_date,
            s.name AS student_name,
            d.id AS doc_id
        FROM achievements a
        JOIN students s ON a.student_id = s.id
        LEFT JOIN documents d ON a.document_id = d.id
        ORDER BY a.issue_date DESC;
        """
    ).fetchall()
    conn.close()
    return render(
        request,
        "achievements/achievement_list.html",
        {"achievements": achievements},
    )


def achievement_detail(request, achievement_id):
    conn = get_connection()
    ach = conn.execute(
        """
        SELECT
            a.id,
            a.title,
            a.category,
            a.issue_date,
            s.id AS student_id,
            s.name AS student_name,
            d.title AS doc_title,
            d.file_path AS doc_file
        FROM achievements a
        JOIN students s ON a.student_id = s.id
        LEFT JOIN documents d ON a.document_id = d.id
        WHERE a.id = ?;
        """,
        (achievement_id,),
    ).fetchone()
    conn.close()

    if ach is None:
        return render(
            request,
            "achievements/achievement_detail.html",
            {"ach": None},
            status=404,
        )

    return render(
        request,
        "achievements/achievement_detail.html",
        {"ach": ach},
    )