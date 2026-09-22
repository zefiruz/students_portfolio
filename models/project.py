from models.student import Student


class Project:
    """Учебный или профессиональный проект в портфолио."""

    def __init__(
        self,
        project_id: int,
        title: str,
        student: Student,
        status: str = "В разработке",
    ) -> None:
        self.id = project_id
        self.title = title
        self.student = student
        self.status = status

    def get_status_info(self) -> str:
        """Определение текущего статуса проекта."""
        return f"Статус проекта '{self.title}': {self.status}"

    def update_status(self, new_status: str) -> None:
        """Изменение статуса проекта."""
        valid_statuses = ["В разработке", "Завершен", "Планируется"]
        if new_status in valid_statuses:
            self.status = new_status
        else:
            print(
                f"Недопустимый статус. Доступные статусы: {', '.join(valid_statuses)}"
            )

    def __str__(self) -> str:
        return f"Проект '{self.title}' [{self.status}] (Автор: {self.student.name})"
