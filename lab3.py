import random
import math
from typing import List, Tuple


def main():
    """
    Главная функция программы. Организует процесс:
    1. Генерации ключей RSA
    2. Шифрования введенного сообщения
    3. Дешифрования обратно
    4. Вывода результатов
    """
    try:
        # Генерируем ключи
        public_key, private_key = generate_keys()

        # Получаем сообщение от пользователя
        message = input("Введите сообщение для шифрования: ")

        # Шифруем сообщение открытым ключом
        ciphertext = encrypt(message, public_key)

        # Расшифровываем сообщение закрытым ключом
        decrypted_message = decrypt(ciphertext, private_key)

        # Выводим результаты
        print("Оригинальное сообщение:", message)
        print("Зашифрованное сообщение:", ", ".join(map(str, ciphertext)))
        print("Расшифрованное сообщение:", decrypted_message)
    except Exception as ex:
        print("Произошла ошибка:", str(ex))


def generate_prime(start: int = 100, end: int = 500) -> int:
    """
    Генерирует простое число в заданном диапазоне.
    :param start: Начало диапазона (по умолчанию 100)
    :param end: Конец диапазона (по умолчанию 500)
    :return: Случайное простое число из диапазона [start, end]
    """
    while True:
        num = random.randint(start, end)
        if is_prime(num):
            return num


def is_prime(number: int) -> bool:
    """
    Проверяет, является ли число простым.
    :param number: Число для проверки
    :return: True, если число простое, иначе False
    """
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True


def mod_inverse(a: int, m: int) -> int:
    """
    Вычисляет модульное обратное число с помощью расширенного алгоритма Евклида.
    :param a: Число, для которого ищем обратное
    :param m: Модуль
    :return: Обратное число a по модулю m
    """
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1


def generate_keys() -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Генерирует пару ключей RSA (открытый и закрытый).
    :return: Кортеж из двух кортежей: ((e, n), (d, n))
    """
    while True:
        try:
            # Генерируем два различных простых числа
            p = generate_prime()
            q = generate_prime()
            while p == q:  # Убедимся, что p и q разные
                q = generate_prime()

            # Вычисляем модуль и функцию Эйлера
            n = p * q
            phi_n = (p - 1) * (q - 1)

            # Выбираем открытую экспоненту e (взаимно простую с phi_n)
            e = 3
            while e < phi_n and math.gcd(e, phi_n) != 1:
                e += 2

            # Вычисляем секретную экспоненту d
            d = mod_inverse(e, phi_n)
            return (e, n), (d, n)
        except:
            continue  # В случае ошибки пробуем снова


def encrypt(message: str, public_key: Tuple[int, int]) -> List[int]:
    """
    Шифрует сообщение с помощью открытого ключа RSA.
    :param message: Сообщение для шифрования
    :param public_key: Открытый ключ (e, n)
    :return: Список зашифрованных чисел
    """
    e, n = public_key
    encrypted = []
    for c in message:
        # Шифруем каждый символ: c^e mod n
        encrypted.append(pow(ord(c), e, n))
    return encrypted


def decrypt(ciphertext: List[int], private_key: Tuple[int, int]) -> str:
    """
    Расшифровывает сообщение с помощью закрытого ключа RSA.
    :param ciphertext: Список зашифрованных чисел
    :param private_key: Закрытый ключ (d, n)
    :return: Расшифрованная строка
    """
    d, n = private_key
    decrypted = []
    for c in ciphertext:
        # Расшифровываем каждый символ: c^d mod n
        decrypted.append(chr(pow(c, d, n)))
    return ''.join(decrypted)


if __name__ == "__main__":
    main()
