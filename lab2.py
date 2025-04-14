import random
import math
from typing import List


def text_to_bits(text: str) -> List[int]:
    bits = []
    for byte in text.encode('utf-8'):
        binary = bin(byte)[2:].zfill(8)
        for bit in binary:
            bits.append(int(bit))
    return bits


def bits_to_text(bits: List[int]) -> str:
    bits = bits[:len(bits) - len(bits) % 8]
    bytes_list = []
    for i in range(0, len(bits), 8):
        byte_str = ''.join(map(str, bits[i:i + 8]))
        bytes_list.append(int(byte_str, 2))
    return bytes(bytes_list).decode('utf-8', errors='ignore')


def hamming_encode(data_bits: List[int]) -> List[int]:
    m = len(data_bits)
    r = 0
    while (2 ** r) < (m + r + 1):
        r += 1

    total_length = m + r
    hamming_code = [0] * total_length

    j = 0
    for i in range(1, total_length + 1):
        if (i & (i - 1)) == 0:
            continue
        hamming_code[i - 1] = data_bits[j]
        j += 1

    for i in range(r):
        parity_pos = (2 ** i) - 1
        parity_value = 0
        for k in range(parity_pos, total_length, 2 ** (i + 1)):
            for l in range(k, min(k + 2 ** i, total_length)):
                parity_value ^= hamming_code[l]
        hamming_code[parity_pos] = parity_value % 2

    return hamming_code


def hamming_decode(received_bits: List[int]) -> List[int]:
    total_length = len(received_bits)
    r = 0
    while (2 ** r) < total_length + 1:
        r += 1

    error_pos = 0

    for i in range(r):
        parity_pos = (2 ** i) - 1
        parity_value = 0
        for j in range(parity_pos, total_length, 2 ** (i + 1)):
            for k in range(j, min(j + 2 ** i, total_length)):
                parity_value ^= received_bits[k]
        if parity_value % 2 != 0:
            error_pos += (parity_pos + 1)

    if error_pos > 0:
        received_bits[error_pos - 1] ^= 1

    decoded_bits = []
    for i in range(1, total_length + 1):
        if (i & (i - 1)) == 0:
            continue
        decoded_bits.append(received_bits[i - 1])

    return decoded_bits


def main():
    text = input("Введите слово для кодирования: ")
    block_size = int(input("Введите длину блока (в битах): "))

    data_bits = text_to_bits(text)
    decoded_bits_accumulated = []

    for i in range(0, len(data_bits), block_size):
        block_bits = data_bits[i:i + block_size]
        print(f"\nБлок: {''.join(map(str, block_bits))}")

        encoded = hamming_encode(block_bits)
        print(f"Закодированная последовательность Хемминга: {''.join(map(str, encoded))}")

        received_bits = encoded.copy()
        error_index = random.randint(0, len(received_bits) - 1)
        received_bits[error_index] ^= 1
        print(
            f"Принятая последовательность (с ошибкой в позиции {error_index + 1}): {''.join(map(str, received_bits))}")

        # Вычисляем ошибочные контрольные биты
        parity_errors = []
        total_length = len(received_bits)
        r = 0
        while (2 ** r) < total_length + 1:
            r += 1

        error_pos = 0
        for bit_index in range(r):
            parity_pos = (2 ** bit_index) - 1
            parity_value = 0
            for j in range(parity_pos, total_length, 2 ** (bit_index + 1)):
                for k in range(j, min(j + 2 ** bit_index, total_length)):
                    parity_value ^= received_bits[k]
            if parity_value % 2 != 0:
                error_pos += (parity_pos + 1)
                parity_errors.append(parity_pos + 1)

        print(f"Ошибочные контрольные биты: {', '.join(map(str, parity_errors))}")

        decoded_bits = hamming_decode(received_bits)
        decoded_bits_accumulated.extend(decoded_bits)

    decoded_text = bits_to_text(decoded_bits_accumulated)
    print(f"\nПолностью декодированное слово: {decoded_text}")
    input()  # Чтобы консоль не закрывалась сразу


if __name__ == "__main__":
    main()