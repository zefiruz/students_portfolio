from django.urls import path
from . import views

app_name = "achievements"

urlpatterns = [
    path("", views.achievements_list, name="list"),
    path("<int:achievement_id>/", views.achievement_detail, name="detail"),
]
