def input_int(prompt: str) -> int:
    """Запросить у пользователя целое число с обработкой ошибок."""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Ошибка: введите корректное целое число.")