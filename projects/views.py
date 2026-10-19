from django.shortcuts import render
from storage import load_projects, load_students


def projects_list(request):
    students = load_students("data/students.json")
    projects = load_projects("data/projects.json", students)
    return render(
        request,
        "projects/project_list.html",
        {"projects": projects},
    )


def project_detail(request, project_id):
    students = load_students("data/students.json")
    projects = load_projects("data/projects.json", students)
    project = next((p for p in projects if p.id == project_id), None)

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
