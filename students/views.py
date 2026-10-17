from django.http import HttpResponse
from homepage.views import page
from storage import load_projects, load_students


def students_list(request):
    students = load_students("data/students.json")
    items = ""
    for student in students:
        items += f"""
        <li class="list-group-item">
            <a href="/students/{student.id}/">{student.name}</a>
            (GPA: {student.gpa})
        </li>
        """

    if not items:
        items = '<li class="list-group-item text-muted">Нет студентов</li>'

    content = f"""
    <h1>Студенты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Студенты", content))


def student_detail(request, student_id):
    students = load_students("data/students.json")
    student = next((s for s in students if s.id == student_id), None)

    if student is None:
        content = """
        <h1 class="text-danger">Студент не найден</h1>
        <a href="/students/" class="btn btn-outline-secondary">
            К списку студентов
        </a>
        """
        return HttpResponse(page("Не найдено", content), status=404)

    # Загружаем проекты для подсчета рейтинга студента по логике ПР3
    all_projects = load_projects("data/projects.json", students)
    student_projects = [p for p in all_projects if p.student.id == student.id]
    rating = student.calculate_rating(len(student_projects))

    skills = ", ".join(student.skills) if student.skills else "Нет навыков"
    completion = student.check_profile_completion()

    # Формируем мини-список проектов студента
    projects_items = ""
    for p in student_projects:
        projects_items += f"<li>{p.title} [{p.status}]</li>"
    if not projects_items:
        projects_items = "<li>Нет проектов</li>"

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{student.name}</h5>
            <p class="card-text"><strong>GPA:</strong> {student.gpa}</p>
            <p class="card-text"><strong>Навыки:</strong> {skills}</p>
            <p class="card-text">
                <strong>Профиль:</strong>
                <span class="badge bg-info">{completion}</span>
            </p>
            <p class="card-text">
                <strong>Предварительный рейтинг:</strong> {rating}
            </p>
            <h6>Проекты:</h6>
            <ul>{projects_items}</ul>
            <a href="/students/" class="btn btn-outline-secondary">
                К списку студентов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(student.name, content), status=200)
