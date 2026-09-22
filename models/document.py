from models.student import Student

class Document:
    """Электронный документ (скан, справка, отчет), прикрепленный к профилю."""

    def __init__(
        self,
        document_id: int,
        title: str,
        file_path: str,
        owner: Student
    ) -> None:
        """Создать объект документа."""
        self.id = document_id
        self.title = title
        self.file_path = file_path
        self.owner = owner  # Композиция: храним объект Student

    @property
    def extension(self) -> str:
        """Возвращает расширение файла (например, pdf, png, docx)."""
        if "." in self.file_path:
            return self.file_path.split(".")[-1].lower()
        return "неизвестно"

    def __str__(self) -> str:
        """Вернуть строковое представление документа."""
        return f"Документ: {self.title} (Формат: .{self.extension}) — Владелец: {self.owner.name}"