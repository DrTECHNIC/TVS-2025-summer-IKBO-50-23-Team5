import random
import string
import hashlib
import math
from datetime import datetime


class PasswordGenerator:
    def __init__(self):
        self.history = []
        self.generated_count = 0

    def generate_password(self, length=12, use_upper=True, use_lower=True,
                          use_digits=True, use_special=True):
        """1. Генерирует пароль по заданным параметрам"""
        if length < 6:
            raise ValueError("Длина пароля должна быть не менее 6 символов")
        chars = ""
        if use_upper:
            chars += string.ascii_uppercase
        if use_lower:
            chars += string.ascii_lowercase
        if use_digits:
            chars += string.digits
        if use_special:
            chars += "!@#$%^&*"
        if not chars:
            raise ValueError("Должен быть выбран хотя бы один тип символов")
        password = ''.join(random.choices(chars, k=length))
        self.history.append(password)
        self.generated_count += 1
        return password

    def check_password_strength(self, password):
        """2. Проверяет сложность пароля - С ОШИБКОЙ"""
        score = 0
        if len(password) >= 8: score += 1
        if any(c.isupper() for c in password): score += 1
        if any(c.islower() for c in password): score += 1
        if any(c.isdigit() for c in password): score += 1
        if any(c in "!@#$%^&*" for c in password): score += 1
        if score >= 4:
            return "Сильный"
        elif score >= 2:
            return "Средний"
        else:
            return "Слабый"

    def validate_password_policy(self, password, min_length=8, require_upper=True,
                                 require_lower=True, require_digits=True, require_special=True):
        """3. Проверяет соответствие пароля политике безопасности"""
        errors = []
        if len(password) < min_length:
            errors.append(f"Пароль должен быть не менее {min_length} символов")
        if require_upper and not any(c.isupper() for c in password):
            errors.append("Пароль должен содержать заглавные буквы")
        if require_lower and not any(c.islower() for c in password):
            errors.append("Пароль должен содержать строчные буквы")
        if require_digits and not any(c.isdigit() for c in password):
            errors.append("Пароль должен содержать цифры")
        if require_special and not any(c in "!@#$%^&*" for c in password):
            errors.append("Пароль должен содержать специальные символы")
        return len(errors) == 0, errors

    def generate_pronounceable_password(self, syllable_count=4):
        """4. Генерирует произносимый пароль"""
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        password = ""
        for i in range(syllable_count):
            if i % 2 == 0:
                password += random.choice(vowels)
                password += random.choice(consonants)
            else:
                password += random.choice(vowels)
                password += random.choice(consonants)

        self.history.append(password)
        self.generated_count += 1
        return password

    def calculate_password_entropy(self, password):
        """5. Вычисляет энтропию пароля"""
        char_set_size = 0
        if any(c.islower() for c in password): char_set_size += 26
        if any(c.isupper() for c in password): char_set_size += 26
        if any(c.isdigit() for c in password): char_set_size += 10
        if any(c in "!@#$%^&*" for c in password): char_set_size += 8
        entropy = len(password) * char_set_size
        return entropy

    def get_generation_stats(self):
        """6. Возвращает статистику генерации"""
        most_common_length = 0
        if self.history:
            lengths = [len(pwd) for pwd in self.history]
            most_common_length = max(set(lengths), key=lengths.count)
        return {
            'total_generated': self.generated_count,
            'history_size': len(self.history),
            'last_generation': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'most_common_length': most_common_length
        }

    def save_password_to_file(self, password, filename="passwords.txt"):
        """7. Сохраняет пароль в файл"""
        try:
            with open(filename, 'a') as f:
                f.write(password + '\n')
            return True
        except Exception as e:
            return False

    def load_passwords_from_file(self, filename="passwords.txt"):
        """8. Загружает пароли из файла"""
        try:
            with open(filename, 'r') as f:
                return [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return []
