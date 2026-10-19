from django.shortcuts import render
from storage import load_projects, load_students


def students_list(request):
    students = load_students("data/students.json")
    return render(
        request,
        "students/student_list.html",
        {"students": students},
    )


def student_detail(request, student_id):
    students = load_students("data/students.json")
    student = next((s for s in students if s.id == student_id), None)

    if student is None:
        return render(
            request,
            "students/student_detail.html",
            {"student": None},
            status=404,
        )

    all_projects = load_projects("data/projects.json", students)
    student_projects = [p for p in all_projects if p.student.id == student.id]
    rating = student.calculate_rating(len(student_projects))
    completion = student.check_profile_completion()

    context = {
        "student": student,
        "skills_list": student.skills,
        "completion": completion,
        "rating": rating,
        "projects": student_projects,
        "achievements": [],
    }
    return render(request, "students/student_detail.html", context)
