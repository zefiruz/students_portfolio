from datetime import date
from typing import Optional

from models.document import Document
from models.student import Student


class Achievement:
    """Достижение студента (олимпиада, хакатон, публикация)."""

    def __init__(
        self,
        achievement_id: int,
        title: str,
        issue_date: date,
        student: Student,
        category: str = "Общее",
        document: Optional[Document] = None,
    ) -> None:
        self.id = achievement_id
        self.title = title
        self.issue_date = issue_date
        self.student = student
        self.category = category
        self.document = document

    def is_recent(self, current_year: int) -> bool:
        """Проверить, получено ли достижение в указанном году."""
        return self.issue_date.year == current_year

    def __str__(self) -> str:
        """Строковое представление достижения."""
        base_str = (
            f"[{self.category}] Достижение '{self.title}' "
            f"(Студент: {self.student.name})"
        )
        if self.document:
            base_str += f" [Подтверждено файлом: {self.document.file_path}]"
        return base_str
