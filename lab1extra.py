import tkinter as tk
from tkinter import filedialog, messagebox
import heapq
import os
from collections import defaultdict, Counter

class HuffmanNode:
    def __init__(self, char, freq):
        """
        Узел дерева Хаффмана.
        :param char: Символ (если это лист дерева)
        :param freq: Частота появления символа
        """
        self.char = char  # Символ
        self.freq = freq  # Частота символа
        self.left = None  # Левый потомок
        self.right = None  # Правый потомок

    def __lt__(self, other):
        """
        Метод для сравнения узлов (нужен для приоритетной очереди heapq).
        Узел с меньшей частотой считается "меньше".
        """
        return self.freq < other.freq


def build_huffman_tree(freq_map):
    """
    Построение дерева Хаффмана на основе частот символов.
    :param freq_map: Словарь {символ: частота}
    :return: Корень дерева Хаффмана
    """
    # Создаём очередь с приоритетами (кучу) из узлов
    priority_queue = [HuffmanNode(char, freq) for char, freq in freq_map.items()]
    heapq.heapify(priority_queue)  # Превращаем список в кучу

    # Пока в куче больше одного узла, объединяем два узла с наименьшей частотой
    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)  # Достаем узел с минимальной частотой
        right = heapq.heappop(priority_queue)  # Второй минимальный узел

        # Создаем новый узел, частота которого - сумма частот двух узлов
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)  # Добавляем объединённый узел обратно в очередь

    # Возвращаем корень построенного дерева
    return priority_queue[0]


def build_codebook(root, code="", codebook=None):
    """
    Генерирует кодовую таблицу (mapping символов в их двоичные коды).
    :param root: Корень дерева Хаффмана
    :param code: Текущий код (по умолчанию пустая строка)
    :param codebook: Словарь {символ: код}
    :return: Заполненный словарь {символ: двоичный код}
    """
    if codebook is None:
        codebook = {}

    if root:
        if root.char is not None:  # Если это лист дерева
            codebook[root.char] = code  # Записываем код

        # Рекурсивно обходим дерево
        build_codebook(root.left, code + "0", codebook)  # Левый путь - добавляем "0"
        build_codebook(root.right, code + "1", codebook)  # Правый путь - добавляем "1"

    return codebook


def encode_file(input_file, output_file):
    """
    Кодирует файл по алгоритму Хаффмана и сохраняет результат в output_file.
    :param input_file: Путь к исходному файлу
    :param output_file: Путь к файлу для сохранения сжатых данных
    """
    with open(input_file, 'rb') as f:
        data = f.read()  # Читаем файл в бинарном режиме

    freq_map = Counter(data)  # Подсчитываем частоты символов
    root = build_huffman_tree(freq_map)  # Строим дерево Хаффмана
    codebook = build_codebook(root)  # Создаём таблицу кодирования

    encoded_data = ''.join(codebook[byte] for byte in data)  # Кодируем данные

    # Добавляем дополнение до кратности 8
    padding = 8 - len(encoded_data) % 8
    encoded_data += '0' * padding

    with open(output_file, 'wb') as f:
        # Сохраняем частоты символов для декодирования
        f.write(len(freq_map).to_bytes(2, byteorder='big'))
        for char, freq in freq_map.items():
            f.write(bytes([char]))
            f.write(freq.to_bytes(4, byteorder='big'))

        # Записываем дополнение и закодированные данные
        f.write(padding.to_bytes(1, byteorder='big'))
        f.write(int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder='big'))


def decode_file(input_file, output_file):
    """
    Декодирует файл, сжатый методом Хаффмана.
    :param input_file: Сжатый файл
    :param output_file: Файл для сохранения результата
    """
    with open(input_file, 'rb') as f:
        # Читаем частоты символов
        freq_map_size = int.from_bytes(f.read(2), byteorder='big')
        freq_map = {}
        for _ in range(freq_map_size):
            char = f.read(1)[0]
            freq = int.from_bytes(f.read(4), byteorder='big')
            freq_map[char] = freq

        root = build_huffman_tree(freq_map)  # Восстанавливаем дерево

        padding = int.from_bytes(f.read(1), byteorder='big')  # Читаем padding

        encoded_data = f.read()
        encoded_bits = ''.join(f'{byte:08b}' for byte in encoded_data)  # Переводим в биты

        # Убираем дополнение
        if padding > 0:
            encoded_bits = encoded_bits[:-padding]

        # Декодируем биты обратно в символы
        decoded_data = []
        current_node = root
        for bit in encoded_bits:
            current_node = current_node.left if bit == '0' else current_node.right

            if current_node.char is not None:
                decoded_data.append(current_node.char)
                current_node = root  # Начинаем заново с корня

        with open(output_file, 'wb') as f_out:
            f_out.write(bytes(decoded_data))


class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Archiver")

        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()

        tk.Label(root, text="Input File:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.input_file, width=50).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(root, text="Output File:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(root, textvariable=self.output_file, width=50).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)

        tk.Button(root, text="Compress", command=self.compress).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text="Decompress", command=self.decompress).grid(row=3, column=1, padx=5, pady=5)

    def browse_input(self):
        filename = filedialog.askopenfilename()
        self.input_file.set(filename)

    def browse_output(self):
        filename = filedialog.asksaveasfilename()
        self.output_file.set(filename)

    def compress(self):
        input_file = self.input_file.get()
        output_file = self.output_file.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please specify input and output files.")
            return

        try:
            encode_file(input_file, output_file)
            messagebox.showinfo("Success", "File compressed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decompress(self):
        input_file = self.input_file.get()
        output_file = self.output_file.get()

        if not input_file or not output_file:
            messagebox.showerror("Error", "Please specify input and output files.")
            return

        try:
            decode_file(input_file, output_file)
            messagebox.showinfo("Success", "File decompressed successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()