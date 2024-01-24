import secrets


def generate_code():
    numbers = "123456789"
    return "".join(secrets.choice(numbers) for i in range(6))
