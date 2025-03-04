from math import log2, ceil

x = "IF_WE_CANNOT_DO_AS_WE_WOULD_WE_SHOULD_DO_AS_WE_CAN"
x2 = 'if_we_cannot_do_as_we_would_we_should_do_as_we_cancan_you_can_a_can_as_a_canner_can_can_a_can?'


def binary(char):
    bytes_data = char.encode('utf-8')

    # Преобразуем каждый байт в бинарный код
    binary_code = ' '.join(format(byte, '08b') for byte in bytes_data)

    return binary_code


def LZW(x):
    print(f"Шаг\t Словарь\t Номер слова\t Кодовые слова\t Затраты(бит)")
    lastbin = ''
    # Задание переменных для алгоритма
    n = len(x)  # Длинна словаря
    X = set(char for char in x)  # Алфавит символов
    c = []  # Алфавит слов
    N = 0  # Номер символа в последовательности
    step = 1  # Счетчик шагов для вывода в таблице
    bit_sum = 0  # Счетчик затраченных бит

    while N < n:
        # Условие, что символ в алфавите слов
        if x[N] in c and len(c) > 0:
            cnt = 1  # Счетчик встреченных символов слов в последовательности
            j = x[N]  # Кэш обработчика

            # Цикл перебирающий последовательность на наличие слов из алфавита
            while (N + cnt != n and j in c):
                j += x[N + cnt]
                cnt += 1
                l = len(j) - 1

            if (len(j) == 1):
                num = c[:-1].index(j) + 1
                binN = bin(c[:-1].index(j) + 1)[2:]
                bini = (ceil(log2((len(c)))) - len(binN)) * '0' + binN
            else:
                if c[-1] != j[:-1]:
                    num = c[:-1].index(j[:-1]) + 1
                    binN = bin(c[:-1].index(j[:-1]) + 1)[2:]
                    bini = (ceil(log2((len(c)))) - len(binN)) * '0' + binN
                else:
                    num = c.index(j[:-1]) + 1
                    if (len(j[:-1]) == 1):
                        bini = ceil(log2((len(c)))) * '0' + binary(j[:-1])
                    else:
                        bini = ceil(log2((len(c)))) * '0' + lastbin
        else:
            num = 0
            j = x[N]
            if N == 0 or len(j) == 1:
                l = 1
            if N == 0:
                bini = binary(x[N])
            else:
                bini = ceil(log2((len(c)))) * '0' + binary(x[N])

        lastbin = bini
        N += l
        c.append(j)
        print(f" {step:<5} {c[step - 1]:<9} {num:>6} {bini:>20} {len(bini):>10}")
        bit_sum += len(bini)
        step += 1

    print(f"Итого{bit_sum:>50}")
    # print(c)


LZW(x2)
