from typing import List

class Student:
    """Пользователь системы (Студент)."""
    
    def __init__(self, student_id: int, name: str, gpa: float, skills: List[str] = None) -> None:
        self.id = student_id
        self.name = name
        self.gpa = gpa
        self.skills = skills if skills else []

    def check_profile_completion(self) -> str:
        """Функция 1: Проверка полноты заполнения профиля студента."""
        if not self.skills:
            return "Профиль пуст: необходимо добавить хотя бы один навык."
        elif len(self.skills) < 3:
            return "Профиль заполнен частично (мало навыков)."
        return "Профиль отлично заполнен!"

    def calculate_rating(self, projects_count: int) -> float:
        """Функция 3: Расчет предварительного рейтинга студента."""
        # Формула: (GPA * 10) + (количество проектов * 15) / 10
        return (self.gpa * 10.0) + (projects_count * 15.0)

    def __str__(self) -> str:
        return f"Студент: {self.name} (Средний балл: {self.gpa})"

    @classmethod
    def from_data(cls, data: dict) -> "Student":
        """Создать объект студента из словаря JSON."""
        return cls(
            student_id=data["id"],
            name=data["name"],
            gpa=data["gpa"],
            skills=data.get("skills", [])
        )