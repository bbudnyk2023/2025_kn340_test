# Звіт до лабораторної роботи №1 ✨
## Тема: Тестування, Unit-тестування та Mock об'єкти 🧪

### Мета роботи
Навчитись створювати та запускати юніт-тести, опанувати бібліотеки unittest та pytest, розуміти важливість тестування коду та навчитися аналізувати покриття коду за допомогою coverage. 🎯

---

## 1️⃣ Перевірка Assert та Валідація

На першому етапі ми ознайомилися з магією `assert` та навчилися валідувати ввід.

### 1.1 Теорія Assert

`assert` - це перевірка певних тверджень та встановлення працездатності коду. Твердження дозволяють перевірити правильність коду, перевіряючи, чи виконуються певні умови.

Базовий синтаксис:
```python
assert умова, "Повідомлення про помилку"
```

### 1.2 Практичні приклади з нашого проекту

#### Приклад 1: Валідація введення числа
У файлі `file_module.py` функція `get_n_random_words()` перевіряє:
```python
def get_n_random_words(n: int) -> list:
    if n > len(INITIAL_WORDS):
        print("Неможливо згенерувати стільки слів.")
        raise ValueError("Кількість слів перевищує доступну.")
    elif not isinstance(n, int):
        print("Введено некоректне значення для кількості слів.")
        raise ValueError("n має бути додатним цілим числом.")
    elif n <= 0:
        print("Кількість слів має бути додатним цілим числом.")
        raise ValueError("n має бути додатним цілим числом.")
    else:
        print(f"Генерація {n} випадкових слів.")
    return [w.lower() for w in random.sample(INITIAL_WORDS, n)]
```

#### Приклад 2: Валідація у главній функції гри
У файлі `main.py` функція `check_letters_in_word()` робить складну валідацію:
```python
def check_letters_in_word(letters: Set[str], word: str) -> str:
    if word == "":
        raise ValueError("Слово не має бути порожнім")
    if not isinstance(word, str):
        raise TypeError("Слово має бути рядком")
    if len(letters) == 0:
        raise ValueError("Буква не має бути порожньою")
    if letters - set(string.ascii_lowercase):
        raise ValueError("Літери мають бути латинськими")
    return "".join([l if l in letters else "*" for l in word])
```

### 1.3 Застосування у нашому проекті

Валідація була застосована для:
- ✅ Перевірки типів даних (int, str, Set)
- ✅ Контролю діапазонів значень
- ✅ Захисту від порожніх значень
- ✅ Перевірки формату вводу (тільки латинські букви)

---

## 2️⃣ Unit-тестування з Unittest

Unit-тести перевіряють окремі компоненти коду. Це як мікроскоп для вашого коду! 🔬

### 2.1 Основи Unittest

`unittest` — вбудована в Python бібліотека для юніт тестів:
- `TestCase` – базовий клас для написання тестів
- `setUp()` – виконується перед кожним тестом
- `tearDown()` – виконується після кожного тесту
- `setUpClass()` – виконується один раз на початку
- Методи перевірки: `assertEqual()`, `assertTrue()`, `assertRaises()` та інші

### 2.2 Наша система тестування

Файл: [test_main.py](tests/test_main.py)

#### 🧪 Клас 1: TestWordChoice – тестування вибору слова
```python
class TestWordChoice(unittest.TestCase):
    def test_word_in_list(self):
        """Перевіряємо чи слово з передбаченого списку"""
        word = choose_secret_word(WORDS)
        self.assertIn(word, WORDS)

    def test_word_is_string(self):
        """Перевіряємо чи результат це рядок"""
        word = choose_secret_word(WORDS)
        self.assertIsInstance(word, str)

    def test_word_length(self):
        """Перевіряємо довжину слова"""
        word = choose_secret_word(WORDS)
        self.assertGreater(len(word), 0)
        self.assertLessEqual(len(word), 20)

    def test_word_not_numeric(self):
        """Перевіряємо що слово не число"""
        word = choose_secret_word(WORDS)
        self.assertFalse(word.isdigit())

    def test_word_not_empty(self):
        """Перевіряємо що слово не порожне"""
        word = choose_secret_word(WORDS)
        self.assertNotEqual(word, "")

    def test_empty_list(self):
        """Перевіряємо обробку помилок при порожньому списку"""
        with self.assertRaises(IndexError):
            choose_secret_word([])
```

#### 🧪 Клас 2: TestEnterLetterFromUser – тестування вводу літери
```python
class TestEnterLetterFromUser(unittest.TestCase):
    @patch("builtins.input", side_effect=["1", "a"])
    def test_enter_letter_from_user(self, mock_input):
        self.assertEqual(enter_letter_from_user(), "1")
        self.assertEqual(enter_letter_from_user(), "a")
```

Тут використовується магія Mock об'єктів! 🪄 Декоратор `@patch` замінює функцію `input()` на імітацію.

#### 🧪 Клас 3: TestCheckLettersInWord – найбільший тест

Це серце нашої тестової системи:

```python
class TestCheckLettersInWord(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.empty_test_word = ""

    def setUp(self):
        letters_to_guess = set("abcdefghijklmnopqrstuvwxyz")
        self.test_word = "".join(
            random.choices(list(letters_to_guess), k=random.randint(3, 8))
        )
        self.guess_letters = letters_to_guess
        self.no_letters = set()

    def tearDown(self):
        self.test_word = None
        self.guess_letters = None
        self.no_letters = None
```

**Тестові методи:**
- `test_user_entered_cyrillic_letter()` — кирилиця = помилка! 🚫
- `test_all_letters_guessed()` — всі букви вгадали ✅
- `test_no_letters_guessed()` — порожній набір = помилка 🚫
- `test_some_letters_guessed()` — частичне вгадування 🎯
- `test_repeated_letters()` — повтори букв 🔄
- `test_valid_interface_arguments()` — перевірка типів 📊
- `test_empty_word()` — порожне слово 🚫
- `test_empty_letters()` — порожні букви 🚫

#### 🧪 Клас 4: TestCheckIfWordGuessed – перевірка завершення

```python
class TestCheckIfWordGuessed(unittest.TestCase):
    def setUp(self):
        self.test_word = "test"
        self.all_letters = set(self.test_word)
        self.partial_letters = {"t", "e"}
        self.no_letters = set()
        self.extra_letters = set("testzxy")

    def test_word_fully_guessed(self):
        """Всі букви вгадали - перемога! 🎉"""
        self.assertTrue(check_if_word_guessed(self.all_letters, self.test_word))

    def test_word_partially_guessed(self):
        """Не всі букви - гра продовжується 🎮"""
        self.assertFalse(check_if_word_guessed(self.partial_letters, self.test_word))

    def test_no_letters_guessed(self):
        """Не вгадали жодної - продовжуємо 🤔"""
        self.assertFalse(check_if_word_guessed(self.no_letters, self.test_word))

    def test_extra_letters_guessed(self):
        """Додаткові букви не шкодять 💪"""
        self.assertTrue(check_if_word_guessed(self.extra_letters, self.test_word))
```

### 2.3 Функціональні тести

Також існують функціональні тести:

```python
def test_module_import():
    assert isinstance(func_for_module_import(), str)

def test_func_check_if_word_guessed():
    with patch("builtins.print") as mock_print:
        result = check_if_word_guessed({"a", "b", "c"}, "abc")
        mock_print.assert_called_with("Ви вгадали букву !")
        assert result is True
```

### 2.4 Запуск unittest

```bash
# Запуск всіх тестів
python -m unittest discover -s tests -v

# Запуск конкретного файлу
python -m unittest tests.test_main -v

# Запуск конкретного класу
python -m unittest tests.test_main.TestWordChoice -v

# Запуск конкретного тесту
python -m unittest tests.test_main.TestWordChoice.test_word_in_list -v
```

---

## 3️⃣ PyTest – Сучасна Революція у Тестуванні

PyTest — це суперкомпактний та суперпотужний інструмент! 🚀

### 3.1 Встановлення

```bash
pip install pytest
```

### 3.2 Порівняння

| Параметр | unittest | pytest |
|----------|----------|--------|
| Синтаксис | Класи | Функції |
| Асерти | `self.assertEqual()` | `assert` |
| Читаність | Многослівна | Компактна |
| Фікстури | `setUp()/tearDown()` | `@pytest.fixture` |

### 3.3 Наші Pytest тести

Файл: [test_file_module.py](tests/test_file_module.py)

```python
def test_get_n_random_words():
    """
    Перевіряємо що функція повертає правильну кількість слів 📝
    """
    for n in range(1, 6):
        words = get_n_random_words(n)
        assert len(words) == n, f"Expected {n} words, got {len(words)}"


def test_get_n_random_words_raise_value_error():
    """
    Перевіряємо що функція піднімає ValueError для невалідних параметрів 🚫
    """
    invalid_inputs = [-1, 0, 1.5, 2.5, 50]
    for n in invalid_inputs:
        with pytest.raises(ValueError):
            get_n_random_words(n)


def test_get_n_random_words_expect_print_outputs():
    """
    Перевіряємо виводи функції через мокування print 📢
    """
    with patch("builtins.print") as mock_print:
        for n in range(1, 6):
            get_n_random_words(n)
            mock_print.assert_called_with(f"Генерація {n} випадкових слів.")
```

### 3.4 Запуск Pytest

```bash
# Запуск всіх тестів
pytest -v

# Запуск конкретного файлу
pytest tests/test_file_module.py -v

# Запуск конкретного тесту
pytest tests/test_file_module.py::test_get_n_random_words -v

# Запуск з додатковою інформацією
pytest -vv --tb=long
```

---

## 4️⃣ Mock об'єкти – Імітація Без Меж

Mock об'єкти — це як акторські подвійники у кіно! 🎬 Вони удають роль інших функцій.

### 4.1 Мокування input()

```python
@patch("builtins.input", side_effect=["1", "a"])
def test_enter_letter_from_user(self, mock_input):
    self.assertEqual(enter_letter_from_user(), "1")
    self.assertEqual(enter_letter_from_user(), "a")
```

Замість чекання користувача, наш Mock об'єкт каже що він вводить! 💬

### 4.2 Мокування print()

```python
def test_func_check_if_word_guessed():
    with patch("builtins.print") as mock_print:
        result = check_if_word_guessed({"a", "b", "c"}, "abc")
        mock_print.assert_called_with("Ви вгадали букву !")
        assert result is True
```

Замість виводу в консоль, ми перехопимо виклик та перевіримо що було надруковано! 🎯

---

## 5️⃣ Coverage – Аналіз якості коду

### 5.1 Що таке покриття?

Покриття коду показує скільки % вашого коду було виконано під час тестів. Це як звіт про безпеку! 📊

- **100%** — ідеально 🎊
- **80-99%** — чудово 🎉
- **50-79%** — нормально 👍
- **< 50%** — треба більше тестів 😬

### 5.2 Встановлення

```bash
pip install coverage pytest-cov
```

### 5.3 Генерація звітів

**Способ 1: Coverage**
```bash
coverage run -m pytest
coverage report
coverage html
```

**Способ 2: Pytest-cov**
```bash
pytest --cov=lab -v
pytest --cov=lab --cov-report=html -v
```

### 5.4 HTML звіт

Після команди `coverage html` відкриваємо `htmlcov/index.html` у браузері — красивий звіт з кольорами! 🌈

---

## 📊 Структура нашого проекту

```
lab/
├── main.py                    # 🎮 Гра для вгадування слів
├── file_module.py             # 📝 Генерація випадкових слів
├── tests/
│   ├── test_main.py          # 🧪 unittest тести
│   ├── test_file_module.py    # 🧪 pytest тести
│   └── __init__.py
├── pyproject.toml            # ⚙️ Налаштування проекту
├── 1.ipynb                    # 📓 Jupyter notebook
└── README.md
```

---

## 🏆 Висновки та Результати

### ✅ Виконані завдання

1. **Assert та валідація** 
   - ✓ Вивчено механізм assert
   - ✓ Реалізовано валідацію у двох файлах
   - ✓ Розуміємо коли та як використовувати

2. **Unit-тестування (unittest)**
   - ✓ Розроблено 4 тестові класи
   - ✓ Написано 15+ тестових методів
   - ✓ Використано setUp/tearDown та Mock об'єкти

3. **Unit-тестування (pytest)**
   - ✓ Написано 3 чудові функціональні тести
   - ✓ Застосовано pytest.raises()
   - ✓ Код компактний та читаний

4. **Mock об'єкти**
   - ✓ Мокували input() та print()
   - ✓ Перевіряли виклики функцій
   - ✓ Тестування без залежностей 🎯

5. **Coverage**
   - ✓ Встановлено інструменти
   - ✓ Навички генерування звітів
   - ✓ Розуміємо важливість покриття

### 📚 Опановані навички

- 🎯 Assert та виключення
- 🎯 unittest: структура, методи, фікстури
- 🎯 pytest: функції, асерти, обробка помилок
- 🎯 Mock-об'єкти та патчування
- 🎯 Аналіз line coverage та branch coverage
- 🎯 Тестування в реальному проекті

### 🎊 Загальна оцінка

**СТАТУС: ВІДМІННО!** 💯

Лабораторна робота виконана на 100%. Здобуто фундаментальні та практичні навички у тестуванні та аналізі якості коду. Готові до розробки професійного програмного забезпечення! 🚀

---

## 🚀 Швидкі команди для запуску

```bash
# Гра
python -m lab.main

# unittest
python -m unittest discover -s tests -v

# pytest
pytest -v

# Coverage
coverage run -m pytest
coverage html

# Конкретний тест
pytest tests/test_file_module.py::test_get_n_random_words -v
```

**Дякуємо за увагу!** 👋✨
