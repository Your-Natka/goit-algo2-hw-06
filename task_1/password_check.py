from task_1.bloom_filter import BloomFilter

def check_password_uniqueness(bloom: BloomFilter, passwords: list[str]) -> dict[str, str]:
    """Перевіряє унікальність паролів, використовуючи фільтр Блума"""
    results = {}
    for password in passwords:
        if not isinstance(password, str) or not password.strip():
            results[password] = "некоректний пароль"
            continue

        if password in bloom:
            results[password] = "вже використаний"
        else:
            bloom.add(password)
            results[password] = "унікальний"
    return results


if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Додавання існуючих паролів
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    # Перевірка нових паролів
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest", "", None]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    print("\nРезультати перевірки паролів:")
    for password, status in results.items():
        print(f"Пароль '{password}' — {status}.")
