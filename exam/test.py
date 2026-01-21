import unittest
from main import is_palindrome

class TestIsPalindrome(unittest.TestCase):
    def test_palindromes(self):
        # Тестуємо правильні паліндроми
        self.assertTrue(is_palindrome("Racecar"))
        self.assertTrue(is_palindrome("A man a plan a canal Panama"))
        self.assertTrue(is_palindrome("Madam"))

    def test_non_palindromes(self):
        # Тестуємо слова, які не є паліндромами
        self.assertFalse(is_palindrome("Hello"))
        self.assertFalse(is_palindrome("World"))
        self.assertFalse(is_palindrome("Python"))

    def test_empty_string(self):
        # Тестуємо випадки з пустими рядками
        self.assertTrue(is_palindrome(""))  # Пустий рядок — це теж паліндром
        self.assertTrue(is_palindrome(" "))  # Рядок із пробілом — паліндром

if __name__ == "__main__":
    unittest.main()