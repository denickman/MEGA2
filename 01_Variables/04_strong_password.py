result = []

while True:
    password = input("enter new password: ")

    checks = {
        "length_ok": len(password) >= 3,
        "has_digit": any(i.isdigit() for i in password),
        "has_upper": any(i.isupper() for i in password),
    }

    print(checks)

    if all(checks.values()): # checks.values() возвращает все значения словаря (без ключей) а all() проверяет, что они все True.
        print("Strong password")
        break
    else:
        print("Weak password. Problems:")
        for name, passed in checks.items():
            if not passed:
                print(f"  - {name} failed")