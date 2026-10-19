from django.shortcuts import render
from db.database import get_connection


def projects_list(request):
    conn = get_connection()
    projects = conn.execute(
        """
        SELECT
            p.id,
            p.title,
            p.status,
            s.id AS student_id,
            s.name AS student_name
        FROM projects p
        JOIN students s ON p.student_id = s.id
        ORDER BY p.title;
        """
    ).fetchall()
    conn.close()
    return render(
        request,
        "projects/project_list.html",
        {"projects": projects},
    )


def project_detail(request, project_id):
    conn = get_connection()
    project = conn.execute(
        """
        SELECT
            p.id,
            p.title,
            p.status,
            s.id AS student_id,
            s.name AS student_name
        FROM projects p
        JOIN students s ON p.student_id = s.id
        WHERE p.id = ?;
        """,
        (project_id,),
    ).fetchone()
    conn.close()

    if project is None:
        return render(
            request,
            "projects/project_detail.html",
            {"project": None},
            status=404,
        )

    return render(
        request,
        "projects/project_detail.html",
        {"project": project},
    )