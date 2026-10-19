-- sql/queries.sql
-- Набор SQL-запросов для индивидуального проекта «Сервис портфолио студентов»

-- ============================================================================
-- 1. ВЫБОРКА И СОРТИРОВКА (SELECT, ORDER BY)
-- ============================================================================

-- Запрос 1: Список всех студентов, отсортированных по среднему баллу (убывание)
SELECT id, name, gpa, skills
FROM students
ORDER BY gpa DESC;

-- Запрос 2: Список всех проектов, отсортированных по названию
SELECT id, title, status, student_id
FROM projects
ORDER BY title ASC;


-- ============================================================================
-- 2. ФИЛЬТРАЦИЯ ДАННЫХ (WHERE)
-- ============================================================================

-- Запрос 3: Студенты-отличники с GPA не менее 4.5
SELECT id, name, gpa
FROM students
WHERE gpa >= 4.5
ORDER BY gpa DESC;

-- Запрос 4: Завершенные проекты
SELECT id, title, student_id
FROM projects
WHERE status = 'Завершен'
ORDER BY title;


-- ============================================================================
-- 3. СОЕДИНЕНИЕ ТАБЛИЦ (JOIN)
-- ============================================================================

-- Запрос 5: Полная информация о проектах с именами их авторов
SELECT
    projects.id,
    projects.title AS project_title,
    projects.status,
    students.name AS student_name,
    students.gpa
FROM projects
JOIN students ON projects.student_id = students.id
ORDER BY projects.id;

-- Запрос 6: Достижения студентов с информацией о подтверждающих документах
SELECT
    achievements.id,
    achievements.title AS achievement_title,
    achievements.category,
    achievements.issue_date,
    students.name AS student_name,
    documents.title AS document_title,
    documents.file_path
FROM achievements
JOIN students ON achievements.student_id = students.id
LEFT JOIN documents ON achievements.document_id = documents.id
ORDER BY achievements.issue_date DESC;


-- ============================================================================
-- 4. АГРЕГАТНЫЕ ФУНКЦИИ (COUNT, AVG, MIN, MAX)
-- ============================================================================

-- Запрос 7: Общая статистика по успеваемости студентов
SELECT
    COUNT(*) AS total_students,
    ROUND(AVG(gpa), 2) AS average_gpa,
    MIN(gpa) AS min_gpa,
    MAX(gpa) AS max_gpa
FROM students;

-- Запрос 8: Количество активных проектов в разработке
SELECT COUNT(*) AS active_projects_count
FROM projects
WHERE status = 'В разработке';


-- ============================================================================
-- 5. ГРУППИРОВКА И ФИЛЬТРАЦИЯ ГРУПП (GROUP BY, HAVING)
-- ============================================================================

-- Запрос 9: Количество проектов у каждого студента (включая студентов без проектов)
SELECT
    students.id,
    students.name,
    COUNT(projects.id) AS projects_count
FROM students
LEFT JOIN projects ON students.id = projects.student_id
GROUP BY students.id, students.name
ORDER BY projects_count DESC;

-- Запрос 10: Категории достижений и количество наград в каждой категории
SELECT
    category,
    COUNT(*) AS achievements_count
FROM achievements
GROUP BY category
ORDER BY achievements_count DESC;

-- Запрос 11: Студенты, имеющие более 1 проекта (HAVING)
SELECT
    students.name,
    COUNT(projects.id) AS projects_count
FROM students
JOIN projects ON students.id = projects.student_id
GROUP BY students.id, students.name
HAVING COUNT(projects.id) >= 2;


-- ============================================================================
-- 6. ПОДЗАПРОСЫ (NOT IN)
-- ============================================================================

-- Запрос 12: Студенты, у которых пока нет ни одного зарегистрированного проекта
SELECT id, name, gpa
FROM students
WHERE id NOT IN (
    SELECT DISTINCT student_id FROM projects
);