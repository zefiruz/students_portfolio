from django.shortcuts import render
from storage import load_achievements, load_documents, load_students


def achievements_list(request):
    students = load_students("data/students.json")
    documents = load_documents("data/documents.json", students)
    achievements = load_achievements(
        "data/achievements.json", students, documents
    )
    return render(
        request,
        "achievements/achievement_list.html",
        {"achievements": achievements},
    )


def achievement_detail(request, achievement_id):
    students = load_students("data/students.json")
    documents = load_documents("data/documents.json", students)
    achievements = load_achievements(
        "data/achievements.json", students, documents
    )
    ach = next((a for a in achievements if a.id == achievement_id), None)

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
