import pytest
from Sergei_Mutant5 import PasswordGenerator
import re
import string
import os

generator = PasswordGenerator()

@pytest.mark.parametrize("length,use_upper,use_lower,use_digits,use_special", 
    [
        (12, True, True, True, True),
        (50, True, True, True, True),
        (8, False, False, True, False),
        (6, True, True, False, False),
    ]
)
def test_generate_password(length, use_upper, use_lower, use_digits, use_special): # 1 метод
    password = generator.generate_password(length, use_upper, use_lower, use_digits, use_special)
    assert len(password) == length    
    expected_chars = ""
    if use_upper:
        expected_chars += string.ascii_uppercase
        assert any(c in string.ascii_uppercase for c in password)
    if use_lower:
        expected_chars += string.ascii_lowercase
        assert any(c in string.ascii_lowercase for c in password)
    if use_digits:
        expected_chars += string.digits
        assert any(c in string.digits for c in password)
    if use_special:
        special_chars = "!@#$%^&*"
        expected_chars += special_chars
        assert any(c in special_chars for c in password)
    assert all(c in expected_chars for c in password)

def test_generate_password_errors(): # 1 метод - тесты на ошибки

    with pytest.raises(ValueError, match="Длина пароля должна быть не менее 6 символов"):
        generator.generate_password(5, True, True, True, True)
    
    with pytest.raises(ValueError, match="Должен быть выбран хотя бы один тип символов"):
        generator.generate_password(10, False, False, False, False)

@pytest.mark.parametrize("password,expected_strength",
    [
        ("SecurePass123!", "Сильный"),
        ("Password123", "Средний"),
        ("pass", "Слабый"),
        ("!@#$%^&*", "Слабый"),
        ("Aa1!", "Слабый"),  
        ("LongPasswordWithoutDigits", "Средний"),
        ("12345678", "Слабый"),
    ]
)
def test_check_password_strength(password, expected_strength): # 2 метод
    strength = generator.check_password_strength(password)
    print(password, expected_strength)
    assert strength == expected_strength

@pytest.mark.parametrize("password,min_length,require_upper,require_lower,require_digits,require_special,expected_valid,expected_errors_count",
    [
        ("StrongPass123!", 8, True, True, True, True, True, 0),
        ("weak", 8, True, True, True, True, False, 4),  # Слишком короткий, нет заглавных, цифр, спецсимволов
        ("GoodPassword", 6, False, True, True, False, False, 1),  # Нет цифр
        ("12345678", 8, False, False, True, False, True, 0),  # Только цифры
        ("ABCdef", 6, True, True, False, False, True, 0),  # Только буквы
    ]
)
def test_validate_password_policy(password, min_length, require_upper, require_lower, 
                                require_digits, require_special, expected_valid, expected_errors_count): # 3 метод
    is_valid, errors = generator.validate_password_policy(
        password, min_length, require_upper, require_lower, require_digits, require_special
    )
    assert is_valid == expected_valid
    assert len(errors) == expected_errors_count

@pytest.mark.parametrize("syllable_count,expected_length",
    [
        (4, 8),  # 4 слога × 2 символа = 8
        (2, 4),  # 2 слога × 2 символа = 4
        (6, 12), # 6 слогов × 2 символа = 12
    ]
)
def test_generate_pronounceable_password(syllable_count, expected_length): # 4 метод
    password = generator.generate_pronounceable_password(syllable_count)
    assert len(password) == expected_length

    assert password.isalpha()
    assert password.islower()  

@pytest.mark.parametrize("password,expected_entropy",
    [
        ("Aa1!", 70 * 4), 
        ("1234", 10 * 4),  
        ("AbCdEfGh", 52 * 8), 
        ("a1!", 36 * 3), 
    ]
)
def test_calculate_password_entropy(password, expected_entropy): # 5 метод
    entropy = generator.calculate_password_entropy(password)
    assert entropy == expected_entropy

def test_get_generation_stats(): # 6 метод
    generator.history.clear()
    generator.generated_count = 0
    
    generator.generate_password(8, True, True, True, True)
    generator.generate_password(10, True, True, True, True)
    generator.generate_password(8, True, True, True, True)
    generator.generate_pronounceable_password(4)
    
    stats = generator.get_generation_stats()
    
    assert stats['total_generated'] == 4
    assert stats['history_size'] == 4
    assert stats['most_common_length'] == 8  
    assert re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", stats['last_generation'])

def test_get_generation_stats_empty(): # 6 метод - пустая история
    generator.history.clear()
    generator.generated_count = 0
    
    stats = generator.get_generation_stats()
    
    assert stats['total_generated'] == 0
    assert stats['history_size'] == 0
    assert stats['most_common_length'] == 0

@pytest.mark.parametrize("password,filename",
    [
        ("TestPassword123", "test_passwords.txt"),
        ("AnotherPass!@#", "test_passwords.txt"),
    ]
)
def test_save_password_to_file(password, filename): # 7 метод
    # Удаляем файл если существует
    if os.path.exists(filename):
        os.remove(filename)
    
    # Сохраняем пароль
    result = generator.save_password_to_file(password, filename)
    assert result == True
    
    # Проверяем, что пароль записан в файл
    with open(filename, 'r') as f:
        content = f.read()
        assert password in content
    
    # Очищаем
    os.remove(filename)

def test_save_password_to_file_error(): # 7 метод - тест на ошибку

    result = generator.save_password_to_file("test", "/invalid/path/passwords.txt")
    assert result == False

@pytest.mark.parametrize("filename,passwords_to_save",
    [
        ("test_load.txt", ["pass1", "pass2", "pass3"]),
        ("empty_test.txt", []),
    ]
)
def test_load_passwords_from_file(filename, passwords_to_save): # 8 метод
    # Создаем тестовый файл
    with open(filename, 'w') as f:
        for pwd in passwords_to_save:
            f.write(pwd + '\n')
    
    # Загружаем пароли
    loaded_passwords = generator.load_passwords_from_file(filename)
    
    # Проверяем
    assert loaded_passwords == passwords_to_save
    
    # Очищаем
    os.remove(filename)

def test_load_passwords_from_file_nonexistent(): # 8 метод - несуществующий файл
    passwords = generator.load_passwords_from_file("nonexistent_file_12345.txt")
    assert passwords == []
