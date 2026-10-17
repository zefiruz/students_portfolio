from django.http import HttpResponse
from homepage.views import page
from storage import load_achievements, load_documents, load_students


def achievements_list(request):
    students = load_students("data/students.json")
    documents = load_documents("data/documents.json", students)
    achievements = load_achievements(
        "data/achievements.json", students, documents)

    items = ""
    for ach in achievements:
        doc_badge = "📎 С документом" if ach.document else "Без подтверждения"
        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/achievements/{ach.id}/">{ach.title}</a>
            <span class="badge bg-secondary">{doc_badge}</span>
        </li>"""

    if not items:
        items = '<li class="list-group-item text-muted">Нет достижений</li>'

    content = f"""
    <h1>Достижения студентов</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Достижения", content))


def achievement_detail(request, achievement_id):
    students = load_students("data/students.json")
    documents = load_documents("data/documents.json", students)
    achievements = load_achievements(
        "data/achievements.json", students, documents
    )

    ach = next((a for a in achievements if a.id == achievement_id), None)

    if ach is None:
        content = """
        <h1 class="text-danger">Достижение не найдено</h1>
        <a href="/achievements/" class="btn btn-outline-secondary">
            К списку достижений
        </a>
        """
        return HttpResponse(page("Не найдено", content), status=404)

    # Форматируем дату в ДД-ММ-ГГГГ
    formatted_date = ach.issue_date.strftime("%d-%m-%Y")

    document_html = (
        '<p class="text-muted">Подтверждающий документ не прикреплен.</p>'
    )
    if ach.document:
        document_html = f"""
        <div class="alert alert-success">
            <strong>Подтверждено:</strong> {ach.document.title}
            (Файл: {ach.document.file_path})
        </div>
        """

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">[{ach.category}] {ach.title}</h5>
            <p class="card-text"><strong>Дата:</strong> {formatted_date}</p>
            <p class="card-text">
                <strong>Студент:</strong>
                <a href="/students/{ach.student.id}/">{ach.student.name}</a>
            </p>
            {document_html}
            <a href="/achievements/" class="btn btn-outline-secondary">
                К списку достижений
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(ach.title, content), status=200)
