from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("students/", include("students.urls")),
    path("projects/", include("projects.urls")),
    path("achievements/", include("achievements.urls")),
]

handler404 = "homepage.views.page_not_found"
