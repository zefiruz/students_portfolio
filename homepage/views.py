from django.http import HttpResponse


def page(title, content):
    bootstrap = (
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3"
        "/dist/css/bootstrap.min.css"
    )
    return f"""<!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{title}</title>
        <link rel="stylesheet" href="{bootstrap}">
    </head>
    <body>
        <nav class="nav p-3 bg-light mb-4">
            <a class="nav-link" href="/">Главная</a>
            <a class="nav-link" href="/students/">Студенты</a>
            <a class="nav-link" href="/projects/">Проекты</a>
            <a class="nav-link" href="/achievements/">Достижения</a>
        </nav>
        <main class="container">{content}</main>
    </body>
    </html>"""


def index(request):
    content = """
    <h1 class="display-4">Сервис Портфолио</h1>
    <p class="lead">
        Система учета академических и профессиональных достижений студентов.
    </p>
    <a href="/students/" class="btn btn-primary me-2">Список студентов</a>
    <a href="/projects/" class="btn btn-secondary me-2">Все проекты</a>
    <a href="/achievements/" class="btn btn-info">Достижения</a>
    """
    return HttpResponse(page("Главная", content))


def page_not_found(request, exception):
    content = """
    <h1 class="text-danger">404 — Страница не найдена</h1>
    <p>Проверьте адрес или вернитесь на главную.</p>
    <a href="/" class="btn btn-outline-secondary">На главную</a>
    """
    return HttpResponse(page("404", content), status=404)