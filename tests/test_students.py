from students import add_student, find_student

def test_add_student():
    students = []
    add_student(students, "Анна", 20)
    assert len(students) == 1
    assert students[0]["name"] == "Анна"

def test_find_student():
    students = [{"id": 1, "name": "Иван", "age": 21}]
    assert len(find_student(students, "ив")) == 1