import datetime

# Проверка полноты заполнения профиля студента
def check_profile_completion(name, age, skills_count):
    print(f"--- Проверка профиля студента: {name} ---")
    
    # Ветвления и простые типы данных
    if age < 16:
        return "Возраст студента слишком мал для публикации полного портфолио."
    
    if skills_count == 0:
        return "Профиль пуст: необходимо добавить хотя бы один навык."
    elif skills_count < 3:
        return "Профиль заполнен частично: рекомендуется добавить больше навыков для привлечения работодателей."
    else:
        return "Профиль отлично заполнен!"

# Определение текущего статуса проекта
def get_project_status(status_code_str):
    status_code = int(status_code_str)
    
    if status_code == 1:
        return "Статус проекта: В разработке"
    elif status_code == 2:
        return "Статус проекта: Завершен"
    elif status_code == 3:
        return "Статус проекта: Планируется"
    else:
        return "Статус проекта: Неизвестно"

# Расчет предварительного рейтинга студента
def calculate_student_rating(projects_count, average_grade_str):
    average_grade = float(average_grade_str)
    
    base_score = projects_count * 15
    total_rating = base_score + (average_grade * 10)
    
    if total_rating >= 100:
        return f"Рейтинг: {total_rating}. Отличный уровень"
    elif total_rating >= 60:
        return f"Рейтинг: {total_rating}. Хороший уровень"
    else:
        return f"Рейтинг: {total_rating}. Начальный уровень"

# Основной сценарий выполнения программы
def main():
    current_date = datetime.date.today()
    print(f"Система портфолио. Дата формирования отчета: {current_date}\n")

    student_name = "Алексей Смирнов"
    student_age = 20
    student_skills_count = 4
    
    project_status_input = "2"
    
    student_projects_count = 3
    student_gpa_input = "4.8"

    profile_result = check_profile_completion(student_name, student_age, student_skills_count)
    print(profile_result)
    print("-" * 40)

    project_result = get_project_status(project_status_input)
    print(project_result)
    print("-" * 40)

    rating_result = calculate_student_rating(student_projects_count, student_gpa_input)
    print(rating_result)

# Точка входа
if __name__ == "__main__":
    main()