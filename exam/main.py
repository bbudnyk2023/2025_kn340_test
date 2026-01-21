def is_palindrome(text: str) -> bool:
    """
    Перевіряє, чи є рядок паліндромом.

    :param text: Вхідний рядок
    :return: True, якщо паліндром, інакше False
    """
    # Видаляємо пробіли та переводимо текст в нижній регістр
    normalized_text = ''.join(text.lower().split())
    # Порівнюємо рядок із його перевернутою версією
    return normalized_text == normalized_text[::-1]