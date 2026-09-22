from models.student import Student
from datetime import date

class Achievement:
    """Достижение студента (олимпиада, хакатон, сертификат)."""

    def __init__(
        self,
        achievement_id: int,
        title: str,
        issue_date: date,
        student: Student,
        category: str = "Общее"
    ) -> None:
        """Создать объект достижения."""
        self.id = achievement_id
        self.title = title
        self.issue_date = issue_date
        self.student = student  # Композиция: храним объект Student
        self.category = category

    def is_recent(self, current_year: int) -> bool:
        """Проверить, получено ли достижение в указанном году."""
        return self.issue_date.year == current_year

    def __str__(self) -> str:
        """Вернуть строковое представление достижения."""
        return f"[{self.category}] Достижение '{self.title}' (Студент: {self.student.name})"