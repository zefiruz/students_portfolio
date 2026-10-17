from django.http import HttpResponse
from homepage.views import page
from storage import load_projects, load_students


def projects_list(request):
    students = load_students("data/students.json")
    projects = load_projects("data/projects.json", students)
    items = ""

    for project in projects:
        # Подбираем цвет бейджа в зависимости от статуса
        if project.status == "Завершен":
            badge_color = "bg-success"
        elif project.status == "В разработке":
            badge_color = "bg-primary"
        else:
            badge_color = "bg-secondary"

        items += f"""
        <li class="list-group-item d-flex justify-content-between">
            <a href="/projects/{project.id}/">{project.title}</a>
            <span class="badge {badge_color}">{project.status}</span>
        </li>
        """

    if not items:
        items = '<li class="list-group-item text-muted">Нет проектов</li>'

    content = f"""
    <h1>Проекты</h1>
    <ul class="list-group">{items}</ul>
    """
    return HttpResponse(page("Проекты", content))


def project_detail(request, project_id):
    students = load_students("data/students.json")
    projects = load_projects("data/projects.json", students)
    project = next((p for p in projects if p.id == project_id), None)

    if project is None:
        content = """
        <h1 class="text-danger">Проект не найден</h1>
        <a href="/projects/" class="btn btn-outline-secondary">
            К списку проектов
        </a>
        """
        return HttpResponse(page("Не найдено", content), status=404)

    # Используем метод get_status_info() объекта Project из ПР3
    status_info = (
        project.get_status_info()
        if hasattr(project, "get_status_info")
        else project.status
    )

    content = f"""
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{project.title}</h5>
            <p class="card-text">
                <strong>Статус:</strong> {status_info}
            </p>
            <p class="card-text">
                <strong>Автор:</strong>
                <a href="/students/{project.student.id}/">
                    {project.student.name}
                </a>
            </p>
            <a href="/projects/" class="btn btn-outline-secondary">
                К списку проектов
            </a>
        </div>
    </div>
    """
    return HttpResponse(page(project.title, content), status=200)
